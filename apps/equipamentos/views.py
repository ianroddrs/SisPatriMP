from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Equipamento, TipoEquipamento, FabricanteEquipamento
from apps.localidades.models import Polo, Cidade, Local, HistoricoMovimentacao

def equipamentos(request):
    equipamentos = Equipamento.objects.select_related(
        'local', 'local__cidade', 'local__cidade__polo', 'tipo', 'fabricante'
    ).prefetch_related('historico_movimentacao')
    
    context = {
        'equipamentos': equipamentos
    }
    print(request)
    return render(request, 'equipamentos.html', context)

def inserir_equipamento(request):
    if request.GET:
        polo, _ = Polo.objects.get_or_create(nome=request.GET.get('polo'))
        
        cidade, _ = Cidade.objects.get_or_create(nome=request.GET.get('cidade'), polo=polo)
        
        local, _ = Local.objects.get_or_create(nome=request.GET.get('local'), cidade=cidade)
        
        tipo_equipamento, _ = TipoEquipamento.objects.get_or_create(tipo=request.GET.get('tipo_equipamento'))
        
        fabricante, _ = FabricanteEquipamento.objects.get_or_create(fabricante=request.GET.get('fabricante'))
        
        equipamento = Equipamento.objects.create(
            local=local,
            tipo=tipo_equipamento,
            fabricante=fabricante,
            nome_equipamento=request.GET.get('nome'),
            descricao=request.GET.get('descricao'),
            mac=request.GET.get('mac'),
            patrimonio=request.GET.get('patrimonio'),
            observacao=request.GET.get('observacao')
        )
        
        HistoricoMovimentacao.objects.create(
            equipamento=equipamento,
            local_origem=None,
            local_destino=local,
            observacao="Cadastro inicial"
        )
    
    return JsonResponse({})
    

