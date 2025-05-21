from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Equipamento, TipoEquipamento, FabricanteEquipamento
from apps.localidades.models import Polo, Cidade, Local, HistoricoMovimentacao
from collections import defaultdict
import json

def equipamentos(request):
    action = request.GET.get('action')
  
    if not action:
        equipamentos = Equipamento.objects.select_related('local', 'local__cidade', 'local__cidade__polo', 'tipo', 'fabricante').prefetch_related('historico_movimentacao')
        
        context = {
            'equipamentos': equipamentos,
        }
        
        return render(request, 'equipamentos.html', context)
    elif action == 'localidades':
        estrutura = defaultdict(dict)

        localidades = Local.objects.select_related('cidade__polo').values_list(
            'nome', 'cidade__nome', 'cidade__polo__nome'
        )

        if localidades:
            for local, cidade, polo in localidades:
                if cidade not in estrutura[polo]:
                    estrutura[polo][cidade] = []
                estrutura[polo][cidade].append(local)
        else:
            cidades = Cidade.objects.select_related('polo').values_list('nome', 'polo__nome')
            for cidade, polo in cidades:
                estrutura[polo][cidade] = []
            
        resultado = {polo: cidades_dict for polo, cidades_dict in estrutura.items()}
        
        context = {
            'localidades': json.dumps(resultado, ensure_ascii=False, indent=2),
        }
        
        return JsonResponse(context, safe=False)
        

def inserir_equipamento(request):
    if request.GET:
        # polo, _ = Polo.objects.get_or_create(nome=request.GET.get('polo'))
        polo, _ = Polo.objects.get_or_create(nome='Região Administrativa Belém II')
        
        # cidade, _ = Cidade.objects.get_or_create(nome=request.GET.get('cidade'), polo=polo)
        cidade, _ = Cidade.objects.get_or_create(nome='Ananindeua', polo=polo)
        
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
    

