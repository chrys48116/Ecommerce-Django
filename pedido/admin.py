from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]
    list_display = ('id', 'user', 'total', 'qtd_total', 'status')
    list_filter = ('status',)  # Adiciona um filtro de status na sidebar

admin.site.register(Pedido, PedidoAdmin)