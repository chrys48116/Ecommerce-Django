import requests
import json

class CalculoFreteService:
    def calcular_frete(self, cep_destino, cep_origem=71591335, peso=1000, altura=50, largura=40, profundidade=30):
        url = f'https://www.cepcerto.com/ws/json-frete/{cep_origem}/{cep_destino}/{peso}/{altura}/{largura}/{profundidade}/eafa7a13ac8c22a4bfdadc771d71a8015157e84f/'
        response = requests.get(url)
        return json.loads(response.text)