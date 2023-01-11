from django import forms
from .models import Stock, StockHistory

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['categoria', 'nome_item', 'quantidade']


    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError('Este campo deve ser preenchido!')

        #for instance in Stock.objects.all():
         # if instance.categoria == categoria:
          #  raise forms.ValidationError('A categoria ' + str(categoria) + ' ja foi registada')
        return categoria



    def clean_nome_item(self):
        item_name = self.cleaned_data.get('nome_item')
        if not item_name:
            raise forms.ValidationError('Este campo deve ser preenchido!')
        return item_name

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['categoria', 'nome_item']

class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    data_de_inicio = forms.DateTimeField(required=False)
    data_de_termino = forms.DateTimeField(required=False)
    class Meta:
        model = StockHistory
        fields = ['categoria', 'nome_item', 'data_de_inicio', 'data_de_termino']

class StockUpdateForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ['categoria', 'nome_item', 'quantidade']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantidade_emitida', 'emitido_para']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantidade_recebida']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['nivel_de_encomenda']