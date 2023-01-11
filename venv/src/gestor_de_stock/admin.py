from django.contrib import admin
from .forms import StockCreateForm

# Register your models here.

from .models import Stock
from .models import Category

class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['categoria', 'nome_item','quantidade','quantidade_recebida','recebido_por', 'quantidade','quantidade_emitida','emitido_por','emitido_para','numero_telefone']
   form = StockCreateForm
   list_filter = ['categoria','recebido_por','emitido_por']
   search_fields = ['categoria', 'nome_item','emitido_por']




admin.site.register(Stock,StockCreateAdmin)
admin.site.register(Category)