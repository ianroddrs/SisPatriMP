from django.shortcuts import render
from .models import Equipamento, TipoEquipamento
from main.models import Polo, Cidade, Local, HistoricoMovimentacao

def equipamentos(request):
    equipamentos = Equipamento.objects.select_related(
        'local', 'local__cidade', 'local__cidade__polo', 'tipo'
    ).prefetch_related('historico_movimentacao')
    
    print(equipamentos[0].historico_movimentacao.all())
    
    # inserir_equipamento()
    
    context = {
        'equipamentos': equipamentos
    }
    return render(request, 'equipamentos.html', context)

def inserir_equipamento():
    # Cria ou obtém o Polo
    polo, _ = Polo.objects.get_or_create(nome="Polo Exemplo")
    
    # Cria ou obtém a Cidade vinculada ao Polo
    cidade, _ = Cidade.objects.get_or_create(nome="Cidade Exemplo", polo=polo)
    
    # Cria ou obtém o Local vinculado à Cidade
    local, _ = Local.objects.get_or_create(nome="Sala Exemplo", cidade=cidade)
    
    # Cria ou obtém o Tipo de Equipamento
    tipo_equipamento, _ = TipoEquipamento.objects.get_or_create(descricao="Tipo Exemplo")
    
    # Cria o Equipamento com os dados informados
    equipamento = Equipamento.objects.create(
        local=local,
        tipo=tipo_equipamento,
        nome="Nome Exemplo",
        dominio="DOMINIO.EXEMPLO",
        mac="00:11:22:33:44:55",  # Formato padrão MAC
        fabricante="Fabricante Exemplo",
        patrimonio="12345",
        observacao="Equipamento inserido inicialmente."
    )
    
    # Registra um histórico de movimentação para o equipamento recém-criado
    HistoricoMovimentacao.objects.create(
        equipamento=equipamento,
        local_origem=None,      # Sem local de origem para a inserção inicial
        local_destino=local,
        observacao="Inserção inicial do equipamento."
    )
    
    print("Equipamento inserido com sucesso:", equipamento)

