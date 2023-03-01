from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_preco(val):
    return utils.format_preco(val)