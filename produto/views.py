from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse

# Create your views here.

class ListaProdutos(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse('ListaProdutos')

class Detalhes(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhes')

class AddCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AddCart')

class RemoveCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveCart')

class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')