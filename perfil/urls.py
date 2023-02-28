from django.urls import path, include
from . import views

name_app = 'perfil'

urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('update/', views.Update.as_view(), name='update'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]