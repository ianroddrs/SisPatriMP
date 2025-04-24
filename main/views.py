from django.shortcuts import render
from django.http import JsonResponse
from apps.localidades.models import Polo, Cidade, Local
from apps.equipamentos.models import TipoEquipamento, FabricanteEquipamento

def home(request):
    return render(request, "home.html", context ={})

def api_datalists(request):
    # polos = list(Polo.objects.all().values())
    # cidades = list(Cidade.objects.all().values())
    # locais = list(Local.objects.all().values())
    # tipo_equipamentos = list(TipoEquipamento.objects.all().values())
    # frabricantes = list(FabricanteEquipamento.objects.all().values())
    polos = ['I', 'II', 'III']
    cidades = ['Ananindeua', 'Benevides','Marituba']
    locais = ['sala01', 'sala02', 'sala03']
    tipo_equipamento = ['computador', 'monitor', 'impressora', 'scanner']
    fabricantes = ['hp', 'aoc', 'lenovo', 'samsung', 'infoway']
    
    context = {
        'polos': polos,
        'cidades': cidades,
        'locais': locais,
        'tipo_equipamentos': tipo_equipamento,
        'fabricantes': fabricantes,
        
    }
    
    return JsonResponse(context, safe=False)