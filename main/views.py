from django.shortcuts import render
from django.http import JsonResponse
from apps.localidades.models import Polo, Cidade, Local
from apps.equipamentos.models import TipoEquipamento, FabricanteEquipamento

def home(request):
    return render(request, "home.html", context ={})
    