from django.shortcuts import render
from django.http import JsonResponse
from apps.localidades.models import Polo, Cidade, Local
from apps.equipamentos.models import TipoEquipamento, FabricanteEquipamento

def home(request):
    return render(request, "home.html", context ={})

def api_datalists(request):
    # tipo_equipamentos = list(TipoEquipamento.objects.all().values())
    # frabricantes = list(FabricanteEquipamento.objects.all().values())

    filters = {}

    if request.GET.get('polo'):
        filters['cidade__polo__nome'] = request.GET['polo']

    if request.GET.get('cidade'):
        filters['cidade__nome'] = request.GET['cidade']
        
    if request.GET.get('local'):
        filters['nome'] = request.GET['local']
    
    
    locais = Local.objects.select_related().filter(**filters)
    
    salas = [local.nome for local in locais]
    cidades = [local.cidade.nome for local in locais]
    polos = [local.cidade.polo.nome for local in locais]
    
    print(salas, cidades, polos)


    tipo_equipamento = ['computador', 'monitor', 'impressora', 'scanner']
    fabricantes = ['hp', 'aoc', 'lenovo', 'samsung', 'infoway']
    
    context = {
        'locais': salas,
        'cidades': cidades,
        'polos': polos,
        'tipo_equipamentos': tipo_equipamento,
        'fabricantes': fabricantes,
        
    }
    
    return JsonResponse(context, safe=False)