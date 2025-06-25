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

    def get(self, request, *args, **kwargs):
        """
        Método GET: Exibe a lista de locais e o formulário de cadastro.
        """
        localidades = Local.objects.select_related('cidade__regiao').all().order_by('cidade__regiao__nome', 'cidade__nome', 'nome')
        
        # Obter cidades e regiões diretamente do banco de dados
        cidades_regiao_data = []
        regioes = Regioes.objects.all().order_by('nome')
        for regiao in regioes:
            cidades_da_regiao = Cidade.objects.filter(regiao=regiao).order_by('nome')
            cidades_regiao_data.append({
                'regiao': regiao.nome,
                'cidades': [{'id': cidade.id, 'nome': cidade.nome} for cidade in cidades_da_regiao]
            })
        
        context = {
            'localidades': localidades,
            'cidades_regiao': cidades_regiao_data # Passa os dados dinâmicos para o template
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Método POST: Cria uma nova localidade.
        """
        cidade_id = request.POST.get('cidade') # Agora esperamos o ID da cidade
        local_nome = request.POST.get('nome_local')
        local_descricao = request.POST.get('descricao', '')

        if not cidade_id or not local_nome:
            messages.error(request, 'Cidade e Nome do Local são campos obrigatórios.')
            return redirect('localidades')

        try:
            cidade = get_object_or_404(Cidade, pk=cidade_id)
            
            # Cria a nova localidade
            Local.objects.create(
                nome=local_nome,
                cidade=cidade,
                descricao=local_descricao
            )
            messages.success(request, f'O local "{local_nome}" foi cadastrado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar local: {e}')
        
        return redirect('localidades')


def local_update(request, pk):
    if request.method == 'POST':
        local = get_object_or_404(Local, pk=pk)
        
        nome = request.POST.get('nome_local')
        descricao = request.POST.get('descricao')
        cidade_id = request.POST.get('cidade') # Permite atualizar a cidade também

        if nome:
            local.nome = nome
            local.descricao = descricao
            if cidade_id: # Atualiza a cidade se fornecida
                local.cidade = get_object_or_404(Cidade, pk=cidade_id)
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

