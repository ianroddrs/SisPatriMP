from django.shortcuts import render
from .models import Equipamento, TipoEquipamento, FabricanteEquipamento
from main.models import Polo, Cidade, Local, HistoricoMovimentacao

def equipamentos(request):
    equipamentos = list(Equipamento.objects.select_related(
        'local', 'local__cidade', 'local__cidade__polo', 'tipo', 'fabricante'
    ).prefetch_related('historico_movimentacao'))
    
    for i in range(50):
        e = equipamentos[0]
        equipamentos.append(e)
    
    
    
    # print(equipamentos[0].historico_movimentacao.all())
    
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
    tipo_equipamento, _ = TipoEquipamento.objects.get_or_create(tipo="Tipo Exemplo")
    
    fabricante, _ = FabricanteEquipamento.objects.get_or_create(fabricante="fabricante Exemplo")
    
    # Cria o Equipamento com os dados informados
    equipamento = Equipamento.objects.create(
        local=local,
        tipo=tipo_equipamento,
        fabricante=fabricante,
        nome_equipamento="Nome Exemplo",
        descricao="exemplo do descrição",
        mac="00:11:22:33:44:55",  # Formato padrão MAC
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

