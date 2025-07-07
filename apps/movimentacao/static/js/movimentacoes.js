document.addEventListener('DOMContentLoaded', () => {
    // === Elementos do Modal de Nova Movimentação ===
    const modalNovaMovimentacao = document.getElementById('modal-nova-movimentacao');
    const formNovaMovimentacao = document.getElementById('form-nova-movimentacao');
    const equipamentoSelect = document.getElementById('equipamento-select');
    const localOrigemDisplay = document.getElementById('local-origem-display');
    const localDestinoSelect = document.getElementById('local-destino-select');
    const observacaoNovaMovimentacao = document.getElementById('observacao-nova-movimentacao');

    // === Elementos do Modal de Edição de Movimentação ===
    const modalEditMovimentacao = document.getElementById('modal-edit-movimentacao');
    const formEditMovimentacao = document.getElementById('form-edit-movimentacao');
    const editMovimentacaoIdInput = document.getElementById('edit-movimentacao-id');
    const editObservacaoInput = document.getElementById('edit-observacao');
    const editMovimentacaoEquipamentoNomeSpan = document.getElementById('edit-movimentacao-equipamento-nome');

    // === Elementos do Modal de Exclusão de Movimentação ===
    const modalDeleteMovimentacao = document.getElementById('modal-delete-movimentacao');
    const formDeleteMovimentacao = document.getElementById('form-delete-movimentacao');
    const deleteMovimentacaoEquipamentoNomeSpan = document.getElementById('delete-movimentacao-equipamento-nome');

    // Inicializa a exibição do local de origem
    localOrigemDisplay.value = 'Selecione um equipamento para ver o local de origem';

    // === Lógica para o Modal de Nova Movimentação ===
    modalNovaMovimentacao.addEventListener('show.bs.modal', async () => {
        formNovaMovimentacao.reset();
        localOrigemDisplay.value = 'Selecione um equipamento para ver o local de origem';
        // await populateEquipamentosAndLocais(); 
    });

    equipamentoSelect.addEventListener('change', () => {
        const selectedOption = equipamentoSelect.options[equipamentoSelect.selectedIndex];
        const localAtualId = selectedOption.getAttribute('data-local-atual-id');
        const localAtualNome = selectedOption.textContent.split('Local Atual: ')[1];
        
        localOrigemDisplay.value = localAtualNome; 
        // localOrigemIdHidden.value = localAtualId;
    });

    formNovaMovimentacao.addEventListener('submit', async (event) => {
        event.preventDefault();

        const url = formNovaMovimentacao.action;
        const formData = new FormData(formNovaMovimentacao);

        try {
            formNovaMovimentacao.submit();
        } catch (error) {
            console.error('Erro ao registrar nova movimentação:', error);
            window.dataManager.showAlert('Erro ao registrar movimentação. Verifique os dados.', 'danger');
        }
    });

    // === Lógica para o Modal de Edição de Movimentação ===
    modalEditMovimentacao.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        const movimentacaoId = button.getAttribute('data-id');
        const observacao = button.getAttribute('data-observacao');
        const equipamentoNome = button.getAttribute('data-equipamento-nome');

        editMovimentacaoIdInput.value = movimentacaoId;
        editObservacaoInput.value = observacao;
        editMovimentacaoEquipamentoNomeSpan.textContent = equipamentoNome;
        formEditMovimentacao.action = `/movimentacao/update_movimentacao/${movimentacaoId}/`; 
    });

    formEditMovimentacao.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        const url = formEditMovimentacao.action;
        const formData = new FormData(formEditMovimentacao);

        try {
            formEditMovimentacao.submit(); 
        } catch (error) {
            console.error('Erro ao atualizar movimentação:', error);
            window.dataManager.showAlert('Erro ao atualizar movimentação. Tente novamente.', 'danger');
        }
    });

    // === Lógica para o Modal de Exclusão de Movimentação ===
    modalDeleteMovimentacao.addEventListener('show.bs.modal', (event) => {
        const button = event.relatedTarget;
        const movimentacaoId = button.getAttribute('data-id');
        const equipamentoNome = button.getAttribute('data-equipamento-nome');

        deleteMovimentacaoEquipamentoNomeSpan.textContent = `"${equipamentoNome}"`;
        formDeleteMovimentacao.action = `/movimentacao/delete_movimentacao/${movimentacaoId}/`; 
    });

    formDeleteMovimentacao.addEventListener('submit', async (event) => {
        event.preventDefault();

        const url = formDeleteMovimentacao.action;
        const formData = new FormData(formDeleteMovimentacao);

        try {
            formDeleteMovimentacao.submit();
        } catch (error) {
            console.error('Erro ao excluir movimentação:', error);
            window.dataManager.showAlert('Erro ao excluir movimentação. Tente novamente.', 'danger');
        }
    });

    /*
    async function populateEquipamentosAndLocais() {
        try {
            const equipamentos = await window.dataManager.request('/movimentacao/api/movimentacao/equipamentos/');
            equipamentoSelect.innerHTML = '<option value="" selected disabled>Selecione um equipamento</option>';
            equipamentos.forEach(eq => {
                const option = document.createElement('option');
                option.value = eq.id;
                option.textContent = `${eq.nome} (Patr: ${eq.patrimonio}) - Local Atual: ${eq.local_atual}`;
                option.setAttribute('data-local-atual-id', eq.local_atual_id);
                equipamentoSelect.appendChild(option);
            });

            const locais = await window.dataManager.request('/movimentacao/api/movimentacao/locais/');
            localDestinoSelect.innerHTML = '<option value="" selected disabled>Selecione o local de destino</option>';
            locais.forEach(local => {
                const option = document.createElement('option');
                option.value = local.id;
                option.textContent = `${local.nome} (${local.cidade} - ${local.regiao})`;
                localDestinoSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Erro ao carregar dados para selects:', error);
            window.dataManager.showAlert('Erro ao carregar opções de equipamentos ou locais.', 'danger');
        }
    }
    // Chame esta função se você não estiver populando via Django context
    // populateEquipamentosAndLocais();
    */
});


