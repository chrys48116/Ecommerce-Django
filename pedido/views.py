from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Pedido, ItemPedido
from produto.models import Variacao
from utils import utils
import mercadopago
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string


# Create your views here.

class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('criar')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs

class Pagar(DispatchLoginRequiredMixin,  DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwargs = 'pk'
    context_object_name = 'pedido'


class ProcessarPagamento(View):
    def enviar_email(self, request, pedido):
        # user = request.user
        # email_cliente = user.email
        # #pedido = Pedido.objects.get(pk=self.kwargs['pk'])
        # assunto = f'Informações do Pedido #{pedido.id}'
        # mensagem = f'Detalhes do seu pedido:\n\n{pedido}'
        # email_de = 'chrys481@gmail.com'
        # email_para = [email_cliente]

        # send_mail(assunto, mensagem, email_de, email_para)

        assunto = f'Informações do Pedido #{pedido.id}'
        mensagem_html = render_to_string('../templates/pedido/pedido_email.html', {'pedido': pedido})
        user = request.user
        email_cliente = user.email
        email = EmailMessage(
            assunto,
            mensagem_html,
            'chrys481@gmail.com',
            [email_cliente]
        )
        email.content_subtype = 'html'  # Defina o tipo de conteúdo como HTML
        email.send()

    def post(self, request, *args, **kwargs):
        pedido = Pedido.objects.get(pk=self.kwargs['pk'])
        pedido.status = 'A'
        pedido.save()

        self.enviar_email(request, pedido)
    
        return redirect('produto:lista')
    
    def get(self, request, *args, **kwargs):
        print("estou em redirect")
        messages.success(request, 'Pagamento efetuado. Voce recebera um email com as informacoes sobre o seu pedido\
                 ou pode acessa-lo no botão "Meus pedidos".')
        return redirect('produto:lista')

    
class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')

        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns '\
                    'produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, '\
                    'verifique quais produtos foram afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )

                self.request.session.save()
                return redirect('produto:cart')

        valor_frete = utils.calcular_frete(self.request)
        valor_frete = valor_frete['frete']
        valor_frete = valor_frete['valorpac']
        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_total(carrinho, valor_frete)

        pedido = Pedido(
            user=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',)
        
        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    promo=v['preco_quantitativo'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']

        messages.success(self.request, 'Pedido gerado. Você pode ver todos os seus\
                 pedidos no botão "Meus pedidos".')
        return redirect(
            reverse(
                'pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'

class Listar(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/listar.html'
    paginate_by = 10
    ordering = ['-id']
