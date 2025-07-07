document.addEventListener('DOMContentLoaded', () => {
    const modalEquipamento = document.getElementById('modal-equipamento');
    const equipamentoForm = document.getElementById('equipamento-form');
    const modalTitle = document.getElementById('modal-equipamento-label');
    const equipamentoIdInput = document.getElementById('equipamento_id');
    const cidadeSelect = document.getElementById('cidade');
    const localSelect = document.getElementById('local');
    const tipoEquipamentoSelect = document.getElementById('tipo_equipamento');
    const fabricanteSelect = document.getElementById('fabricante');
    const nomeInput = document.getElementById('nome');
    const descricaoInput = document.getElementById('descricao');
    const macInput = document.getElementById('mac');
    const patrimonioInput = document.getElementById('patrimonio');
    const observacaoInput = document.getElementById('observacao');
    const btnSalvarEquipamento = document.getElementById('btn-salvar-equipamento');

    // Modal de exclusão
    const modalDeleteEquipamento = document.getElementById('modal-delete-equipamento');
    const deleteEquipamentoNomeSpan = document.getElementById('delete-equipamento-nome');
    const deleteEquipamentoForm = document.getElementById('delete-equipamento-form');

    // Função para limpar o formulário
    const clearForm = () => {
        equipamentoForm.reset();
        equipamentoIdInput.value = '';
        localSelect.innerHTML = '<option value="" selected disabled>Primeiro, selecione a cidade</option>';
        modalTitle.textContent = 'Cadastrar Equipamento';
        equipamentoForm.action = '{% url "create_equipamento" %}';
        btnSalvarEquipamento.textContent = 'Salvar Equipamento';
    };

    // Evento para quando o modal de equipamento é aberto
    modalEquipamento.addEventListener('show.bs.modal', async (event) => {
        const button = event.relatedTarget; // Botão que acionou o modal
        const mode = button.getAttribute('data-mode'); // 'add' ou 'edit'

        clearForm(); // Limpa o formulário antes de preencher ou usar para adicionar

        if (mode === 'edit') {
            modalTitle.textContent = 'Editar Equipamento';
            btnSalvarEquipamento.textContent = 'Atualizar Equipamento';
            
            // Preenche os campos do formulário com os dados do equipamento
            const equipamentoId = button.getAttribute('data-id');
            const localId = button.getAttribute('data-local-id');
            const cidadeId = button.getAttribute('data-cidade-id');
            const tipoId = button.getAttribute('data-tipo-id');
            const fabricanteId = button.getAttribute('data-fabricante-id');
            const nome = button.getAttribute('data-nome');
            const descricao = button.getAttribute('data-descricao');
            const mac = button.getAttribute('data-mac');
            const patrimonio = button.getAttribute('data-patrimonio');
            const observacao = button.getAttribute('data-observacao');

            equipamentoIdInput.value = equipamentoId;
            nomeInput.value = nome;
            descricaoInput.value = descricao;
            macInput.value = mac;
            patrimonioInput.value = patrimonio;
            observacaoInput.value = observacao;

            equipamentoForm.action = `{% url "update_equipamento" 0 %}`.replace('0', equipamentoId);

            // Seleciona a cidade e carrega os locais
            cidadeSelect.value = cidadeId;
            if (cidadeId) {
                try {
                    const locais = await dataManager.request(`/api/locais-por-cidade/?cidade_id=${cidadeId}`);
                    localSelect.innerHTML = '<option value="" disabled>Selecione o local</option>';
                    locais.forEach(local => {
                        const option = document.createElement('option');
                        option.value = local.id;
                        option.textContent = local.nome;
                        localSelect.appendChild(option);
                    });
                    localSelect.value = localId; // Seleciona o local correto
                } catch (error) {
                    console.error('Erro ao carregar locais:', error);
                    dataManager.showAlert('Erro ao carregar locais.', 'danger');
                }
            }

            // Seleciona o tipo e fabricante
            tipoEquipamentoSelect.value = tipoId;
            fabricanteSelect.value = fabricanteId;

        } else { // Modo 'add'
            clearForm();
        }
    });

    // Evento para quando o modal de exclusão é aberto
    modalDeleteEquipamento.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        const equipamentoId = button.getAttribute('data-id');
        const equipamentoNome = button.getAttribute('data-nome');

        deleteEquipamentoNomeSpan.textContent = `"${equipamentoNome}"`;
        deleteEquipamentoForm.action = `{% url "delete_equipamento" 0 %}`.replace('0', equipamentoId);
    });

    // Listener para mudança na seleção de cidade
    cidadeSelect.addEventListener('change', async () => {
        const cidadeId = cidadeSelect.value;
        localSelect.innerHTML = '<option value="" selected disabled>Carregando locais...</option>'; // Mensagem de carregamento
        localSelect.disabled = true; // Desabilita enquanto carrega

        if (cidadeId) {
            try {
                const locais = await dataManager.request(`/api/locais-por-cidade/?cidade_id=${cidadeId}`);
                localSelect.innerHTML = '<option value="" selected disabled>Selecione o local</option>';
                if (locais.length === 0) {
                    localSelect.innerHTML = '<option value="" selected disabled>Nenhum local encontrado para esta cidade</option>';
                } else {
                    locais.forEach(local => {
                        const option = document.createElement('option');
                        option.value = local.id;
                        option.textContent = local.nome;
                        localSelect.appendChild(option);
                    });
                }
                localSelect.disabled = false;
            } catch (error) {
                console.error('Erro ao carregar locais:', error);
                dataManager.showAlert('Erro ao carregar locais.', 'danger');
                localSelect.innerHTML = '<option value="" selected disabled>Erro ao carregar locais</option>';
                localSelect.disabled = false;
            }
        } else {
            localSelect.innerHTML = '<option value="" selected disabled>Primeiro, selecione a cidade</option>';
            localSelect.disabled = false;
        }
    });

    /*
    const populateSelects = async () => {
        try {
            const tipos = await dataManager.request('{% url "api_tipos_equipamento" %}');
            tipoEquipamentoSelect.innerHTML = '<option value="" selected disabled>Selecione o tipo</option>';
            tipos.forEach(tipo => {
                const option = document.createElement('option');
                option.value = tipo.id; // Ou tipo.tipo se a view retornar o nome
                option.textContent = tipo.tipo;
                tipoEquipamentoSelect.appendChild(option);
            });

            const fabricantes = await dataManager.request('{% url "api_fabricantes" %}');
            fabricanteSelect.innerHTML = '<option value="" selected disabled>Selecione o fabricante</option>';
            fabricantes.forEach(fab => {
                const option = document.createElement('option');
                option.value = fab.id; // Ou fab.fabricante se a view retornar o nome
                option.textContent = fab.fabricante;
                fabricanteSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Erro ao popular selects:', error);
            dataManager.showAlert('Erro ao carregar opções de tipo/fabricante.', 'danger');
        }
    };
    populateSelects();
    */

    // Lida com o envio do formulário (Adicionar/Editar)
    equipamentoForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o envio padrão do formulário

        const formData = new FormData(equipamentoForm);
        const url = equipamentoForm.action;
        const method = equipamentoIdInput.value ? 'POST' : 'POST'; // Django usa POST para update e create via formulário

        try {
            // A requisição será tratada pelo Django e o refresh da página exibirá a mensagem
            equipamentoForm.submit(); 
        } catch (error) {
            console.error('Erro ao salvar equipamento:', error);
            dataManager.showAlert('Erro ao salvar equipamento. Verifique os dados.', 'danger');
        }
    });

    // Lida com o envio do formulário de exclusão
    deleteEquipamentoForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o envio padrão do formulário

        const url = deleteEquipamentoForm.action;
        const method = 'POST'; // Django usa POST para exclusão

        try {
            // A requisição será tratada pelo Django e o refresh da página exibirá a mensagem
            deleteEquipamentoForm.submit();
        } catch (error) {
            console.error('Erro ao excluir equipamento:', error);
            dataManager.showAlert('Erro ao excluir equipamento. Tente novamente.', 'danger');
        }
    });
});
