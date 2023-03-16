from django.urls import path, include
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.Detalhes.as_view(), name='detalhes'),
    path('addcart/', views.AddCart.as_view(), name='addcart'),
    path('removecart/', views.RemoveCart.as_view(), name='removecart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('resumocompra/', views.ResumoCompra.as_view(), name='resumocompra'),
    path('busca/', views.Busca.as_view(), name='busca'),
]
