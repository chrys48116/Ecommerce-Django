from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_preco(val):
    return utils.format_preco(val)

@register.filter
def cart_total_qtd(carrinho):
    return utils.cart_total_qtd(carrinho)

@register.filter
def cart_total(carrinho, frete):
    return utils.cart_total(carrinho, frete)