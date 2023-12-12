import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')

class CalculoFreteService:
    def calcular_frete(self, cep_destino, cep_origem=71591335, peso=1000, altura=50, largura=40, profundidade=30):
        url = f'https://www.cepcerto.com/ws/json-frete/{cep_origem}/{cep_destino}/{peso}/{altura}/{largura}/{profundidade}/{api_key}/'
        response = requests.get(url)
        return json.loads(response.text)