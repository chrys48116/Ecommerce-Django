from django.contrib import admin
from .models import Produto, Variacao, Categoria
from django.db.models import Sum

# Register your models here.

class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_format_preco', 'get_format_preco_promo', 'categoria', 'get_estoque']
    list_editable = ['categoria']
    list_filter = ('categoria',)  
    inlines = [VariacaoInline]

    def get_estoque(self, obj):
        estoque_total = Variacao.objects.filter(produto=obj).aggregate(Sum('estoque'))['estoque__sum']
        return estoque_total

    get_estoque.short_description = 'Estoque Total'

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)