from perfil.models import Perfil
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv('API_KEY')

def format_preco(val):
    return f'R$ {val:.2f}'.replace('.',',')

def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_total(carrinho, frete):
    cart = sum(
        [item.get('preco_quantitativo_promocional') 
         if item.get('preco_quantitativo_promocional')
         else item.get('preco_quantitativo')
         for item in carrinho.values()]
        )
    frete = frete.replace(',','.')
    frete = float(frete)
    cart_total = cart + frete
    print(cart_total)
    return cart_total


def calcular_frete(request):
    if not request.user.is_authenticated:
        return {'frete': {'error': 'Usuário não autenticado'}}

    cep = Perfil.objects.filter(usuario=request.user).values_list('cep', flat=True).first()
    if not cep:
        return {'frete': {'error': 'CEP não disponível'}}

    try:
        frete_data = calcula_frete_service(cep)
        return {'frete': frete_data}
    except Exception as e:
        return {'frete': {'error': str(e)}}
    
def calcula_frete_service(cep_destino, cep_origem=71591335, peso=1000, altura=50, largura=40, profundidade=30):
        url = f'https://www.cepcerto.com/ws/json-frete/{cep_origem}/{cep_destino}/{peso}/{altura}/{largura}/{profundidade}/{api_key}/'
        response = requests.get(url)
        return json.loads(response.text)