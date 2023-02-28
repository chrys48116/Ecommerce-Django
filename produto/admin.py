from django.contrib import admin
from .models import Produto, Variacao

# Register your models here.

class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_format_preco', 'get_format_preco_promo']
    inlines = [VariacaoInline]

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
