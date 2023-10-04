from django.contrib import admin
from .models import Produto, Variacao, Categoria

# Register your models here.

class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_format_preco', 'get_format_preco_promo', 'categoria']
    list_editable = ['categoria']
    list_filter = ('categoria',)  
    inlines = [VariacaoInline]
    #raw_id_fields = ('categorias',)

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
