from django.urls import path
from . import views

name_app = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('listar/', views.Listar.as_view(), name='listar'),
    path('detalhe/<int:pk>', views.Detalhe.as_view(), name='detalhe'),
    path('processarpagamento/<int:pk>', views.ProcessarPagamento.as_view(), name='processarpagamento'),
]