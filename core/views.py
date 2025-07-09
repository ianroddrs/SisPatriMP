from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
import datetime
import json
from django.db.models import Q

from core.models import Regioes, Cidade, Local, HistoricoMovimentacao, Equipamento, TipoEquipamento, FabricanteEquipamento

def home(request):

    if request.GET.get('action') == 'populate_db':
        regioes_path = 'core/static/json/regioes.json'
        with open(regioes_path, 'r', encoding='utf-8') as file:
            regioes_data = json.load(file)
            for regiao, cidades in regioes_data.items():
                regiao, _ = Regioes.objects.get_or_create(nome=regiao)
                for cidade in cidades:
                    Cidade.objects.get_or_create(
                        nome=cidade,
                        regiao=regiao
                    )

        locais_path = 'core/static/json/locais.json'
        with open(locais_path, 'r', encoding='utf-8') as file:
            locais_data = json.load(file)
            for cidade, locais in locais_data.items():
                for local in locais:
                    nome = local['local']
                    descricao = local['descricao']

                    cidade_obj, _ = Cidade.objects.get_or_create(nome=cidade)
                    Local.objects.get_or_create(
                        nome=nome,
                        cidade=cidade_obj,
                        descricao=descricao
                    )

        equipamentos_path = 'core/static/json/equipamentos.json'
        with open(equipamentos_path, 'r', encoding='utf-8') as file:
            equipamentos_data = json.load(file)
            for equipamento in equipamentos_data:
                patrimonio = equipamento['patrimonio']
                tipo_nome = equipamento['tipo']
                marca_nome = equipamento['marca']
                local_nome = equipamento['local']

                tipo_obj, _ = TipoEquipamento.objects.get_or_create(tipo=tipo_nome)
                fabricante_obj, _ = FabricanteEquipamento.objects.get_or_create(fabricante=marca_nome)
                local_obj = Local.objects.get(nome=local_nome)

                Equipamento.objects.get_or_create(
                    patrimonio=patrimonio,
                    tipo=tipo_obj,
                    fabricante=fabricante_obj,
                    local=local_obj,
                )


    total_equipamentos = Equipamento.objects.count()
    total_locais = Local.objects.count()
    data_30_dias_atras = timezone.now() - datetime.timedelta(days=30)
    movimentacoes_ultimo_mes = HistoricoMovimentacao.objects.filter(
        data_movimentacao__gte=data_30_dias_atras
    ).count()
    itens_em_alerta = Equipamento.objects.filter(
        Q(observacao__icontains='alerta') | Q(observacao__isnull=True) | Q(observacao__exact='')
    ).count()
    equipamentos_por_local = Equipamento.objects.values('local__nome') \
                                              .annotate(quantidade=Count('id')) \
                                              .order_by('-quantidade')[:10]
    labels_local = [item['local__nome'] for item in equipamentos_por_local]
    series_local = [item['quantidade'] for item in equipamentos_por_local]

    equipamentos_por_tipo = Equipamento.objects.values('tipo__tipo') \
                                               .annotate(quantidade=Count('id')) \
                                               .order_by('-quantidade')
    labels_tipo = [item['tipo__tipo'] for item in equipamentos_por_tipo]
    series_tipo = [item['quantidade'] for item in equipamentos_por_tipo]

    equipamentos_por_fabricante = Equipamento.objects.values('fabricante__fabricante') \
                                                     .annotate(quantidade=Count('id')) \
                                                     .order_by('-quantidade')[:10]
    labels_fabricante = [item['fabricante__fabricante'] for item in equipamentos_por_fabricante]
    series_fabricante = [item['quantidade'] for item in equipamentos_por_fabricante]

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

        'chart_data': json.dumps({
            'equipamentos_por_local': {'labels': labels_local, 'series': series_local},
            'equipamentos_por_tipo': {'labels': labels_tipo, 'series': series_tipo},
            'equipamentos_por_fabricante': {'labels': labels_fabricante, 'series': series_fabricante},
            'movimentacoes_por_mes': {'labels': labels_movimentacao_mes, 'series': series_movimentacao_mes},
        })
    }
    return render(request, "home.html", context)

def get_dashboard_chart_data(request):

    equipamentos_por_local = Equipamento.objects.values('local__nome') \
                                              .annotate(quantidade=Count('id')) \
                                              .order_by('-quantidade')[:10]
    labels_local = [item['local__nome'] for item in equipamentos_por_local]
    series_local = [item['quantidade'] for item in equipamentos_por_local]

    equipamentos_por_tipo = Equipamento.objects.values('tipo__tipo') \
                                               .annotate(quantidade=Count('id')) \
                                               .order_by('-quantidade')
    labels_tipo = [item['tipo__tipo'] for item in equipamentos_por_tipo]
    series_tipo = [item['quantidade'] for item in equipamentos_por_tipo]

    equipamentos_por_fabricante = Equipamento.objects.values('fabricante__fabricante') \
                                                     .annotate(quantidade=Count('id')) \
                                                     .order_by('-quantidade')[:10]
    labels_fabricante = [item['fabricante__fabricante'] for item in equipamentos_por_fabricante]
    series_fabricante = [item['quantidade'] for item in equipamentos_por_fabricante]

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

