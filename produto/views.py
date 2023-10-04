from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View, generic
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from . import models
from perfil.models import Perfil
from pprint import pprint
from . import services
import time
from utils import utils

# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']

class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)
        
        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo)|
            Q(descricao_curta__icontains=termo)|
            Q(descricao_longa__icontains=termo) |
            Q(categoria__nome__icontains=termo)
        )
        self.request.session.save()
        return qs
    

class ListaProdutosCategoria(ListaProdutos):
    def get_context_data(self, **kwargs):
        print("Busca view get_context_data foi chamada")  # Debugging
        context = super().get_context_data(**kwargs)
        categorias = models.Categoria.objects.all()
        print(f'Categorias: {categorias}')  # Debugging
        context['categorias'] = categorias
        return context

class Detalhes(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AddCart(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_promocional = variacao.promo
        #categoria = produto.categoria
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_promocional * \
                quantidade_carrinho
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_promocional': preco_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_promocional,
                #'categoria': categoria,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)

class RemoveCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)
        
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)
        
        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(
            self.request, 
            f'{carrinho["produto_nome"]} {carrinho["variacao_nome"]} removido do seu carrinho'
            )
        
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)

class Cart(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
            }
        contexto.update(utils.calcular_frete(self.request))
        return render(self.request, 'produto/carrinho.html', contexto)
    
    # def calcular_frete(self):
    #     if not self.request.user.is_authenticated:
    #         return {'frete': {'error': 'Usuário não autenticado'}}

    #     cep = Perfil.objects.filter(usuario=self.request.user).values_list('cep', flat=True).first()
    #     if not cep:
    #         return {'frete': {'error': 'CEP não disponível'}}

    #     servico_frete = services.CalculoFreteService()
    #     try:
    #         frete_data = servico_frete.calcular_frete(cep)
    #         return {'frete': frete_data}
    #     except Exception as e:
    #         return {'frete': {'error': str(e)}}

class ResumoCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('criar')
        
        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(self.request, 'Usuario não tem perfil.')
            return redirect('criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio')
            return redirect('produto:lista')

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }
        contexto.update(utils.calcular_frete(self.request))
        return render(self.request, 'produto/resumo.html', contexto)
    
# class CalculoFreteView(View):
#     def get(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect('criar')
        
#         cep = Perfil.objects.filter(usuario=self.request.user).values_list('cep', flat=True).first()

#         servico_frete = services.CalculoFreteService()
#         try:
#             frete_data = servico_frete.calcular_frete(cep)
#             return JsonResponse(frete_data)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)