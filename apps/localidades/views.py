import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.contrib import messages
import os

# Importe seus modelos aqui
from core.models import Regioes, Cidade, Local

class LocalidadesView(View):
    """
    View para listar e cadastrar Localidades.
    """
    template_name = 'localidades.html'

    def _get_cidades_por_regiao(self):
        """Lê o arquivo JSON e retorna um dicionário de cidades agrupadas por região."""
        try:
            json_path = os.path.join(settings.BASE_DIR, 'sua_app', 'static', 'json', 'regioes.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get(self, request, *args, **kwargs):
        """
        Método GET: Exibe a lista de locais e o formulário de cadastro.
        """
        localidades = Local.objects.select_related('cidade__regiao').all().order_by('cidade__regiao__nome', 'cidade__nome', 'nome')
        cidades_regiao = self._get_cidades_por_regiao()
        
        context = {
            'localidades': localidades,
            'cidades_regiao': cidades_regiao
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Método POST: Cria uma nova localidade.
        """
        cidade_nome = request.POST.get('cidade')
        local_nome = request.POST.get('nome_local')
        local_descricao = request.POST.get('descricao', '')

        if not cidade_nome or not local_nome:
            messages.error(request, 'Cidade e Nome do Local são campos obrigatórios.')
            return redirect('localidades')

        # Encontra a região da cidade selecionada a partir do JSON
        cidades_regiao = self._get_cidades_por_regiao()
        regiao_nome = None
        for r_nome, cidades in cidades_regiao.items():
            if cidade_nome in cidades:
                regiao_nome = r_nome
                break
        
        if not regiao_nome:
            messages.error(request, f'A cidade "{cidade_nome}" não foi encontrada em nenhuma região.')
            return redirect('localidades')

        # Usa get_or_create para evitar duplicatas
        regiao, _ = Regioes.objects.get_or_create(nome=regiao_nome)
        cidade, _ = Cidade.objects.get_or_create(nome=cidade_nome, defaults={'regiao': regiao})
        
        # Cria a nova localidade
        Local.objects.create(
            nome=local_nome,
            cidade=cidade,
            descricao=local_descricao
        )

        messages.success(request, f'O local "{local_nome}" foi cadastrado com sucesso!')
        return redirect('localidades')


def local_update(request, pk):
    if request.method == 'POST':
        local = get_object_or_404(Local, pk=pk)
        
        nome = request.POST.get('nome_local')
        descricao = request.POST.get('descricao')

        if nome:
            local.nome = nome
            local.descricao = descricao
            local.save()
            messages.success(request, 'Local atualizado com sucesso!')
            return redirect('localidades')
        else:
            messages.error(request, 'O nome do local não pode ser vazio.')
            return redirect('localidades')
    
    # Redireciona para a lista se o método não for POST
    return redirect('localidades')


def local_delete(request, pk):
    if request.method == 'POST':
        local = get_object_or_404(Local, pk=pk)
        try:
            local.delete()
            messages.success(request, f'O local "{local.nome}" foi excluído com sucesso.')
        except Exception as e:
            # Adiciona proteção caso haja equipamentos vinculados a este local
            messages.error(request, f'Não foi possível excluir o local. Verifique se existem equipamentos vinculados a ele. Erro: {e}')
        
        return redirect('localidades')

    return redirect('localidades')