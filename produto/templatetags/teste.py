from django.views import View
from django.http import JsonResponse
from produto.services import CalculoFreteService
# from perfil.models import Perfil
# from django.shortcuts import render, redirect, reverse, get_object_or_404

# class CalculoFreteView(View):
#     def get(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect('criar')
        
#         cep = Perfil.objects.filter(usuario=self.request.user).values_list('cep', flat=True).first()

#         servico_frete = CalculoFreteService()
#         try:
#             frete_data = servico_frete.calcular_frete(cep)
#             return JsonResponse(frete_data)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)