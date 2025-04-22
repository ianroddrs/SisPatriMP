from django.shortcuts import render
from django.http import JsonResponse
from apps.localidades.models import Polo, Cidade, Local

def home(request):
    return render(request, "home.html", context ={})

def api_localidades(request):
    # polos = list(Polo.objects.all().values())
    # cidades = list(Cidade.objects.all().values())
    # locais = list(Local.objects.all().values())
    polos = ['I', 'II', 'III']
    cidades = ['Ananindeua', 'Benevides','Marituba']
    locais = ['sala01', 'sala02', 'sala03']
    
    context = {
        'polos': polos,
        'cidades': cidades,
        'locais': locais
    }
    
    return JsonResponse(context, safe=False)