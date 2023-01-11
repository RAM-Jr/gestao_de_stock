from django.db import models

# Create your models here.

# categoria_opcoes = (
# 		('Mobiliario', 'Mobiliario'),
# 		('Equipamento TI', 'Equipamento TI'),
# 		('Vinho', 'Vinho'),
# 		('Carne', 'Carne'),
# 	)

class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	def __str__(self):
		return self.name

class Stock(models.Model):
	categoria = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	nome_item = models.CharField(max_length=50, blank=True, null=True)
	quantidade = models.IntegerField(default='0', blank=False, null=True)
	quantidade_recebida = models.IntegerField(default='0', blank=True, null=True)
	recebido_por = models.CharField(max_length=50, blank=True, null=True)
	quantidade_emitida = models.IntegerField(default='0', blank=True, null=True)
	emitido_por = models.CharField(max_length=50, blank=True, null=True)
	emitido_para = models.CharField(max_length=50, blank=True, null=True)
	numero_telefone = models.CharField(max_length=50, blank=True, null=True)
	registado_por = models.CharField(max_length=50, blank=True, null=True)
	nivel_de_encomenda = models.IntegerField(default='0', blank=True, null=True)
	ultima_actualização = models.DateTimeField(auto_now_add=False, auto_now=True)
	data_de_registo = models.DateTimeField(auto_now_add=True, auto_now=False)
	

	def __str__(self):
		return self.nome_item + ' (' + str(self.quantidade)+')'

class StockHistory(models.Model):
	categoria = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	nome_item = models.CharField(max_length=50, blank=True, null=True)
	quantidade = models.IntegerField(default='0', blank=True, null=True)
	quantidade_recebida = models.IntegerField(default='0', blank=True, null=True)
	recebido_por = models.CharField(max_length=50, blank=True, null=True)
	quantidade_emitida = models.IntegerField(default='0', blank=True, null=True)
	emitido_por = models.CharField(max_length=50, blank=True, null=True)
	emitido_para = models.CharField(max_length=50, blank=True, null=True)
	numero_telefone = models.CharField(max_length=50, blank=True, null=True)
	registado_por = models.CharField(max_length=50, blank=True, null=True)
	nivel_de_encomenda = models.IntegerField(default='0', blank=True, null=True)
	ultima_actualização = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	data_de_registo = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)