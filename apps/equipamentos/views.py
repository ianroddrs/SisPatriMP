from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages
import json

from core.models import Equipamento, TipoEquipamento, FabricanteEquipamento, Regioes, Cidade, Local, HistoricoMovimentacao

def equipamentos(request):
    """
    View para listar equipamentos e fornecer dados para os formulários.
    """
    equipamentos_list = Equipamento.objects.select_related(
        'local', 'local__cidade', 'local__cidade__regiao', 'tipo', 'fabricante'
    ).prefetch_related('historico_movimentacao').order_by('nome_equipamento')

    # Filtragem
    search_query = request.GET.get('q')
    if search_query:
        equipamentos_list = equipamentos_list.filter(
            Q(nome_equipamento__icontains=search_query) |
            Q(patrimonio__icontains=search_query) |
            Q(mac__icontains=search_query) |
            Q(local__nome__icontains=search_query) |
            Q(local__cidade__nome__icontains=search_query) |
            Q(tipo__tipo__icontains=search_query) |
            Q(fabricante__fabricante__icontains=search_query)
        )

    # Obter todos os tipos de equipamentos e fabricantes para os selects
    tipos_equipamento = TipoEquipamento.objects.all().order_by('tipo')
    fabricantes = FabricanteEquipamento.objects.all().order_by('fabricante')

    # Preparar cidades e regiões para o select dinâmico
    cidades_data = []
    regioes = Regioes.objects.all().order_by('nome')
    for regiao in regioes:
        cidades_da_regiao = Cidade.objects.filter(regiao=regiao).order_by('nome')
        cidades_data.append({
            'regiao': regiao.nome,
            'cidades': [{'id': cidade.id, 'nome': cidade.nome} for cidade in cidades_da_regiao]
        })

    context = {
        'equipamentos': equipamentos_list,
        'tipos_equipamento': tipos_equipamento,
        'fabricantes': fabricantes,
        'cidades_regiao': cidades_data, # Dicionário com regiões e cidades para o template
        'search_query': search_query,
    }
    return render(request, 'equipamentos.html', context)

@require_POST
def create_equipamento(request):
    """
    Cria um novo equipamento.
    """
    try:
        # Pega os dados do formulário
        local_id = request.POST.get('local')
        tipo_equipamento_nome = request.POST.get('tipo_equipamento')
        fabricante_nome = request.POST.get('fabricante')
        nome_equipamento = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        mac = request.POST.get('mac')
        patrimonio = request.POST.get('patrimonio')
        observacao = request.POST.get('observacao')

        # Valida campos obrigatórios
        if not all([local_id, tipo_equipamento_nome, fabricante_nome, nome_equipamento, patrimonio]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('equipamentos')

        # Obtém instâncias de FKs, criando se não existirem
        local = get_object_or_404(Local, pk=local_id)
        tipo_equipamento, _ = TipoEquipamento.objects.get_or_create(tipo=tipo_equipamento_nome)
        fabricante, _ = FabricanteEquipamento.objects.get_or_create(fabricante=fabricante_nome)

        # Cria o equipamento
        equipamento = Equipamento.objects.create(
            local=local,
            tipo=tipo_equipamento,
            fabricante=fabricante,
            nome_equipamento=nome_equipamento,
            descricao=descricao,
            mac=mac,
            patrimonio=patrimonio,
            observacao=observacao
        )

        # Registra no histórico de movimentação
        HistoricoMovimentacao.objects.create(
            equipamento=equipamento,
            local_origem=None, # No cadastro, a origem é nula
            local_destino=local,
            observacao="Cadastro inicial do equipamento",
            usuario=request.user if request.user.is_authenticated else None # Atribui o usuário logado
        )

        messages.success(request, f'Equipamento "{nome_equipamento}" cadastrado com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao cadastrar equipamento: {e}')
    
    return redirect('equipamentos')

@require_POST
def update_equipamento(request, pk):
    """
    Atualiza um equipamento existente.
    """
    equipamento = get_object_or_404(Equipamento, pk=pk)
    try:
        # Salva o local de origem para o histórico
        local_origem_antigo = equipamento.local

        # Pega os novos dados do formulário
        local_id = request.POST.get('local')
        tipo_equipamento_nome = request.POST.get('tipo_equipamento')
        fabricante_nome = request.POST.get('fabricante')
        nome_equipamento = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        mac = request.POST.get('mac')
        patrimonio = request.POST.get('patrimonio')
        observacao = request.POST.get('observacao')

        # Valida campos obrigatórios
        if not all([local_id, tipo_equipamento_nome, fabricante_nome, nome_equipamento, patrimonio]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('equipamentos')

        # Obtém instâncias de FKs, criando se não existirem
        novo_local = get_object_or_404(Local, pk=local_id)
        novo_tipo_equipamento, _ = TipoEquipamento.objects.get_or_create(tipo=tipo_equipamento_nome)
        novo_fabricante, _ = FabricanteEquipamento.objects.get_or_create(fabricante=fabricante_nome)

        # Atualiza os campos do equipamento
        equipamento.local = novo_local
        equipamento.tipo = novo_tipo_equipamento
        equipamento.fabricante = novo_fabricante
        equipamento.nome_equipamento = nome_equipamento
        equipamento.descricao = descricao
        equipamento.mac = mac
        equipamento.patrimonio = patrimonio
        equipamento.observacao = observacao
        equipamento.save()

        # Registra no histórico de movimentação apenas se o local mudou
        if local_origem_antigo != novo_local:
            HistoricoMovimentacao.objects.create(
                equipamento=equipamento,
                local_origem=local_origem_antigo,
                local_destino=novo_local,
                observacao=f"Movimentação do equipamento. Local alterado de '{local_origem_antigo.nome}' para '{novo_local.nome}'.",
                usuario=request.user if request.user.is_authenticated else None
            )
        
        messages.success(request, f'Equipamento "{nome_equipamento}" atualizado com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao atualizar equipamento: {e}')
    
    return redirect('equipamentos')

@require_POST
def delete_equipamento(request, pk):
    """
    Deleta um equipamento.
    """
    equipamento = get_object_or_404(Equipamento, pk=pk)
    nome_equipamento = equipamento.nome_equipamento
    try:
        equipamento.delete()
        messages.success(request, f'Equipamento "{nome_equipamento}" excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Não foi possível excluir o equipamento "{nome_equipamento}". Erro: {e}')
    
    return redirect('equipamentos')

# Views para AJAX/APIs (usadas pelo JS para preencher dropdowns)

def get_locais_por_cidade(request):
    """
    Retorna locais de uma cidade específica em formato JSON.
    """
    cidade_id = request.GET.get('cidade_id')
    locais = Local.objects.filter(cidade_id=cidade_id).order_by('nome').values('id', 'nome')
    return JsonResponse(list(locais), safe=False)

def get_tipos_equipamento(request):
    """
    Retorna todos os tipos de equipamento em formato JSON.
    """
    tipos = TipoEquipamento.objects.all().order_by('tipo').values('id', 'tipo')
    return JsonResponse(list(tipos), safe=False)

def get_fabricantes(request):
    """
    Retorna todos os fabricantes em formato JSON.
    """
    fabricantes = FabricanteEquipamento.objects.all().order_by('fabricante').values('id', 'fabricante')
    return JsonResponse(list(fabricantes), safe=False)

