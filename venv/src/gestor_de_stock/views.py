from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
import csv
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
	title = 'Welcome: This is the Home Page'
	form = 'My form'
	context = {
		"title": title,
		'test':form
	}
	# return render(request, "home.html",context)
	return redirect('/list_items')

@login_required
def list_items(request):
	header = 'Lista de Produtos'
	form = StockSearchForm(request.POST or None)
	queryset = Stock.objects.all()
	context = {
		"header": header,
		"queryset": queryset,
		"form":form,
	}

	if request.method == 'POST':
		categoria = form['categoria'].value()
		queryset = Stock.objects.filter(
			nome_item__icontains=form['nome_item'].value(),
		)

		if (categoria != ''):
			queryset = queryset.filter(categoria_id=categoria)

		if form['export_to_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="Lista do Stock.csv"'
			writer = csv.writer(response)
			writer.writerow(['CATEGORIA', 'NOME DO PRODUTO', 'QUANTIDADE NO STOCK'])
			instance = queryset
			for stock in instance:
			 	writer.writerow([stock.categoria, stock.nome_item, stock.quantidade])
			return response

		context = {
			"form": form,
			"header": header,
			"queryset": queryset,
		}

	return render(request, "list_items.html",context)

@login_required
def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Adicionado com Sucesso')
		return redirect('/list_items')
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_items.html", context)

def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Actualizado com Sucesso')
			return redirect('/list_items')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)


def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Apagado com Sucesso')
		return redirect('/list_items')
	return render(request, 'delete_items.html')


def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)


def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantidade_recebida = 0
		instance.quantidade -= instance.quantidade_emitida
		messages.success(request, "Emitido com Sucesso. " + str(instance.quantidade) + " " + str(instance.nome_item) + "s restantes no Stock")
		instance.emitido_por = str(request.user)
		instance.save()

		return redirect('/stock_detail/'+str(instance.id))

	context = {
		"title": 'Issue ' + str(queryset.nome_item),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_items.html", context)



def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantidade_emitida = 0
		instance.quantidade += instance.quantidade_recebida
		instance.recebido_por = str(request.user)
		instance.save()
		messages.success(request, "Recebido com Sucesso. " + str(instance.quantidade) + " " + str(instance.nome_item)+"s contidos no Stock")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.nome_item),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)

def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Nivel de encomenda para " + str(instance.nome_item) + " foi actualizado para " + str(instance.nivel_de_encomenda))

		return redirect("/list_items")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)

@login_required
def list_history(request):
	header = 'Historico de Dados'
	queryset = StockHistory.objects.all()

	form = StockHistorySearchForm(request.POST or None)

	context = {
		"header": header,
		"queryset": queryset,
		"form":form,
	}

	if request.method == 'POST':
		categoria = form['categoria'].value()

		queryset = StockHistory.objects.filter(
								nome_item__icontains=form['nome_item'].value(),
								ultima_actualização__range=[
							form['data_de_inicio'].value(),
							form['data_de_termino'].value()
						]
								)

		if (categoria != ''):
			queryset = queryset.filter(categoria_id=categoria)


		if form['export_to_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="Historico do Stock.csv"'
			writer = csv.writer(response)
			writer.writerow(
				['CATEGORIA', 
				'NOME DO PRODUTO',
				'QUANTIDADE', 
				'QUANTIDADE EMITIDA', 
				'QUANTIDADE RECEBIDA', 
				'RECEBIDO POR', 
				'EMITIDO POR', 
				'ULTIMA ACTUALIZAÇÃO'])
			instance = queryset
			for stock in instance:
				writer.writerow(
				[stock.categoria, 
				stock.nome_item, 
				stock.quantidade, 
				stock.quantidade_emitida, 
				stock.quantidade_recebida, 
				stock.recebido_por, 
				stock.emitido_por, 
				stock.ultima_actualização])
			return response

		context = {
			"form": form,
			"header": header,
			"queryset": queryset,
		}
	return render(request, "list_history.html",context)