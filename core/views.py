from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
import datetime

from core.models import Equipamento, Local, HistoricoMovimentacao, TipoEquipamento, FabricanteEquipamento

def home(request):
    """
    View para o dashboard, coletando dados reais do banco de dados.
    """
    # --- KPIs (Key Performance Indicators) ---
    total_equipamentos = Equipamento.objects.count()
    total_locais = Local.objects.count()

    # Movimentações no último mês
    # Calcula a data de 30 dias atrás a partir de agora
    data_30_dias_atras = timezone.now() - datetime.timedelta(days=30)
    movimentacoes_ultimo_mes = HistoricoMovimentacao.objects.filter(
        data_movimentacao__gte=data_30_dias_atras
    ).count()

    # Itens em Alerta (exemplo: equipamentos sem observação ou com observação específica 'Alerta')
    # Esta é uma métrica de exemplo e pode ser ajustada conforme a definição de "alerta"
    # Aqui, consideramos que um equipamento está em alerta se a observação contiver a palavra "alerta"
    # ou se for nula (indicando que talvez precise de revisão).
    itens_em_alerta = Equipamento.objects.filter(
        Q(observacao__icontains='alerta') | Q(observacao__isnull=True) | Q(observacao__exact='')
    ).count()

    # --- Dados para os Gráficos ---

    # Gráfico 1: Equipamentos por Local (Top N locais)
    # Agrupa equipamentos por local e conta a quantidade. Limita aos 10 primeiros para clareza no gráfico.
    equipamentos_por_local = Equipamento.objects.values('local__nome') \
                                              .annotate(quantidade=Count('id')) \
                                              .order_by('-quantidade')[:10]
    labels_local = [item['local__nome'] for item in equipamentos_por_local]
    series_local = [item['quantidade'] for item in equipamentos_por_local]

    # Gráfico 2: Equipamentos por Tipo
    equipamentos_por_tipo = Equipamento.objects.values('tipo__tipo') \
                                               .annotate(quantidade=Count('id')) \
                                               .order_by('-quantidade')
    labels_tipo = [item['tipo__tipo'] for item in equipamentos_por_tipo]
    series_tipo = [item['quantidade'] for item in equipamentos_por_tipo]

    # Gráfico 3: Equipamentos por Fabricante (Top N fabricantes)
    equipamentos_por_fabricante = Equipamento.objects.values('fabricante__fabricante') \
                                                     .annotate(quantidade=Count('id')) \
                                                     .order_by('-quantidade')[:10]
    labels_fabricante = [item['fabricante__fabricante'] for item in equipamentos_por_fabricante]
    series_fabricante = [item['quantidade'] for item in equipamentos_por_fabricante]

    # Gráfico 4: Movimentações ao longo do tempo (últimos 6 meses)
    movimentacoes_por_mes = HistoricoMovimentacao.objects \
                                                 .annotate(mes_ano=TruncMonth('data_movimentacao')) \
                                                 .values('mes_ano') \
                                                 .annotate(total=Count('id')) \
                                                 .filter(mes_ano__gte=timezone.now() - datetime.timedelta(days=180)) \
                                                 .order_by('mes_ano')
    labels_movimentacao_mes = [item['mes_ano'].strftime('%b/%Y') for item in movimentacoes_por_mes]
    series_movimentacao_mes = [item['total'] for item in movimentacoes_por_mes]

    context = {
        'total_equipamentos': total_equipamentos,
        'total_locais': total_locais,
        'movimentacoes_ultimo_mes': movimentacoes_ultimo_mes,
        'itens_em_alerta': itens_em_alerta,

        # Dados para os gráficos JSON (serão buscados via API no JS)
        'chart_data': json.dumps({
            'equipamentos_por_local': {'labels': labels_local, 'series': series_local},
            'equipamentos_por_tipo': {'labels': labels_tipo, 'series': series_tipo},
            'equipamentos_por_fabricante': {'labels': labels_fabricante, 'series': series_fabricante},
            'movimentacoes_por_mes': {'labels': labels_movimentacao_mes, 'series': series_movimentacao_mes},
        })
    }
    return render(request, "home.html", context)


# --- API para dados dos gráficos (opcional, mas boa prática para dashboard dinâmico) ---
# Se você quiser que o JS busque os dados do gráfico via AJAX, adicione estas views:

import json
from django.db.models import Q

def get_dashboard_chart_data(request):
    """
    API que retorna os dados para os gráficos do dashboard em formato JSON.
    """
    # Gráfico 1: Equipamentos por Local (Top 10 locais)
    equipamentos_por_local = Equipamento.objects.values('local__nome') \
                                              .annotate(quantidade=Count('id')) \
                                              .order_by('-quantidade')[:10]
    labels_local = [item['local__nome'] for item in equipamentos_por_local]
    series_local = [item['quantidade'] for item in equipamentos_por_local]

    # Gráfico 2: Equipamentos por Tipo
    equipamentos_por_tipo = Equipamento.objects.values('tipo__tipo') \
                                               .annotate(quantidade=Count('id')) \
                                               .order_by('-quantidade')
    labels_tipo = [item['tipo__tipo'] for item in equipamentos_por_tipo]
    series_tipo = [item['quantidade'] for item in equipamentos_por_tipo]

    # Gráfico 3: Equipamentos por Fabricante (Top 10 fabricantes)
    equipamentos_por_fabricante = Equipamento.objects.values('fabricante__fabricante') \
                                                     .annotate(quantidade=Count('id')) \
                                                     .order_by('-quantidade')[:10]
    labels_fabricante = [item['fabricante__fabricante'] for item in equipamentos_por_fabricante]
    series_fabricante = [item['quantidade'] for item in equipamentos_por_fabricante]

    # Gráfico 4: Movimentações ao longo do tempo (últimos 6 meses)
    movimentacoes_por_mes = HistoricoMovimentacao.objects \
                                                 .annotate(mes_ano=TruncMonth('data_movimentacao')) \
                                                 .values('mes_ano') \
                                                 .annotate(total=Count('id')) \
                                                 .filter(mes_ano__gte=timezone.now() - datetime.timedelta(days=180)) \
                                                 .order_by('mes_ano')
    labels_movimentacao_mes = [item['mes_ano'].strftime('%b/%Y') for item in movimentacoes_por_mes]
    series_movimentacao_mes = [item['total'] for item in movimentacoes_por_mes]

    data = {
        'equipamentos_por_local': {'labels': labels_local, 'series': series_local},
        'equipamentos_por_tipo': {'labels': labels_tipo, 'series': series_tipo},
        'equipamentos_por_fabricante': {'labels': labels_fabricante, 'series': series_fabricante},
        'movimentacoes_por_mes': {'labels': labels_movimentacao_mes, 'series': series_movimentacao_mes},
    }
    return JsonResponse(data)

