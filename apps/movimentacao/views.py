from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta

from core.models import HistoricoMovimentacao, Equipamento, Local, User # Importe User

def movimentacoes(request):
    """
    View para listar o histórico de movimentações com filtros.
    """
    historico = HistoricoMovimentacao.objects.select_related(
        'equipamento',
        'local_origem',
        'local_destino',
        'usuario'
    ).order_by('-data_movimentacao') # Ordena do mais novo para o mais antigo

    # Filtros
    equipamento_search = request.GET.get('equipamento_search')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if equipamento_search:
        historico = historico.filter(
            Q(equipamento__nome_equipamento__icontains=equipamento_search) |
            Q(equipamento__patrimonio__icontains=equipamento_search)
        )
    
    if data_inicio:
        historico = historico.filter(data_movimentacao__gte=data_inicio)
    
    if data_fim:
        # Adiciona um dia para incluir a data final no filtro
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
        historico = historico.filter(data_movimentacao__lte=data_fim_obj + timedelta(days=1))

    # Dados para os selects dos modais
    equipamentos_disponiveis = Equipamento.objects.select_related('local').all().order_by('nome_equipamento')
    locais_disponiveis = Local.objects.select_related('cidade__regiao').all().order_by('nome')

    context = {
        'historico': historico,
        'equipamento_search': equipamento_search,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'equipamentos_disponiveis': equipamentos_disponiveis,
        'locais_disponiveis': locais_disponiveis,
    }
    return render(request, 'movimentacao.html', context)

@require_POST
def perform_movimentacao(request):
    """
    Realiza uma nova movimentação de equipamento, criando um novo registro no histórico.
    Atualiza também o local atual do equipamento.
    """
    try:
        equipamento_id = request.POST.get('equipamento')
        local_destino_id = request.POST.get('local_destino')
        observacao = request.POST.get('observacao', '')

        if not all([equipamento_id, local_destino_id]):
            messages.error(request, 'Equipamento e Local de Destino são obrigatórios.')
            return redirect('movimentacao')

        equipamento = get_object_or_404(Equipamento, pk=equipamento_id)
        local_destino = get_object_or_404(Local, pk=local_destino_id)
        local_origem = equipamento.local # O local atual do equipamento é a origem

        if local_origem == local_destino:
            messages.warning(request, 'O local de destino é o mesmo que o local de origem. Nenhuma movimentação registrada.')
            return redirect('movimentacao')

        # Atualiza o local do equipamento
        equipamento.local = local_destino
        equipamento.save()

        # Cria o registro no histórico de movimentação
        HistoricoMovimentacao.objects.create(
            equipamento=equipamento,
            local_origem=local_origem,
            local_destino=local_destino,
            observacao=observacao,
            usuario=request.user if request.user.is_authenticated else None
        )
        messages.success(request, f'Movimentação do equipamento "{equipamento.nome_equipamento}" para "{local_destino.nome}" registrada com sucesso!')

    except Exception as e:
        messages.error(request, f'Erro ao registrar movimentação: {e}')
    
    return redirect('movimentacao')

@require_POST
def update_movimentacao(request, pk):
    """
    Atualiza a observação de um registro de movimentação existente.
    Não permite alterar equipamento, origem ou destino de uma movimentação passada.
    """
    movimentacao = get_object_or_404(HistoricoMovimentacao, pk=pk)
    try:
        nova_observacao = request.POST.get('observacao', '')
        
        movimentacao.observacao = nova_observacao
        movimentacao.save()
        messages.success(request, 'Observação da movimentação atualizada com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao atualizar movimentação: {e}')
    
    return redirect('movimentacao')

@require_POST
def delete_movimentacao(request, pk):
    """
    Deleta um registro de movimentação do histórico.
    """
    movimentacao = get_object_or_404(HistoricoMovimentacao, pk=pk)
    equipamento_nome = movimentacao.equipamento.nome_equipamento
    try:
        movimentacao.delete()
        messages.success(request, f'Movimentação do equipamento "{equipamento_nome}" excluída com sucesso.')
    except Exception as e:
        messages.error(request, f'Não foi possível excluir a movimentação do equipamento "{equipamento_nome}". Erro: {e}')
    
    return redirect('movimentacao')

# APIs para preenchimento dinâmico de selects (AJAX)
def api_equipamentos_for_movimentacao(request):
    """
    Retorna uma lista de equipamentos com seu local atual para preenchimento de select.
    """
    equipamentos_data = Equipamento.objects.select_related('local', 'local__cidade').all().order_by('nome_equipamento')
    result = [
        {
            'id': eq.pk,
            'nome': eq.nome_equipamento,
            'patrimonio': eq.patrimonio,
            'local_atual': eq.local.nome if eq.local else 'N/A',
            'local_atual_id': eq.local.pk if eq.local else None,
        }
        for eq in equipamentos_data
    ]
    return JsonResponse(result, safe=False)

def api_locais_for_movimentacao(request):
    """
    Retorna uma lista de locais para preenchimento de select.
    """
    locais_data = Local.objects.select_related('cidade__regiao').all().order_by('nome')
    result = [
        {
            'id': local.pk,
            'nome': local.nome,
            'cidade': local.cidade.nome if local.cidade else 'N/A',
            'regiao': local.cidade.regiao.nome if local.cidade and local.cidade.regiao else 'N/A',
        }
        for local in locais_data
    ]
    return JsonResponse(result, safe=False)



