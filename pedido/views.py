from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Pedido, ItemPedido
from produto.models import Variacao
from utils import utils

# Create your views here.

class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagar')
    
class SalvarPedido(View):
    tempalte_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Você precisa fazer o login')
            return redirect('criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_ids = [v for v in carrinho]
        bd_variacao = list(Variacao.objects.select_related('produto').filter(id__in=carrinho_ids))

        for variacao in bd_variacao:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_promocional']

            msg_error_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco'] = estoque * preco_unt
                carrinho[vid]['preco_promocional'] = estoque * preco_unt_promo

                msg_error_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho' \
                                    'Reduzimos a quantidade desses produtos.'

            if msg_error_estoque:
                messages.error(self.request, msg_error_estoque)

                self.request.session.save()
                return redirect('produto:cart')
            
        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_total(carrinho)

        pedido = Pedido(user=self.request.user,
                        total=valor_total_carrinho,
                        qtd_total=qtd_total_carrinho,
                        status='C')
        
        pedido.save()

        ItemPedido.objects.bulk_create(
            [ItemPedido(
                pedido=pedido,
                produto=v['produto_nome'],
                produto_id=v['produto_id'],
                variacao=v['variacao_nome'],
                variacao_id=v['variacao_id'],
                preco=v['preco_quantitativo'],
                promo=v['preco_quantitativo_promocional'],
                quantidade=v['quantidade'],
                imagem=v['imagem'],
            )for v in carrinho.values()]
        )

        # contexto = {
        #     'qtd_total_carrinho': qtd_total_carrinho,
        #     'valor_total_carrinho': valor_total_carrinho,
        # }
        
        del self.request.session['carrinho']
        return redirect('lista')

class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe')

class Lista(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Lista')