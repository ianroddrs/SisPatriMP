// static/js/localidades.js

document.addEventListener('DOMContentLoaded', () => {
    // Não há lógica JS complexa aqui, pois os modais de edição/exclusão já são gerados
    // pelo Django com os IDs corretos e as ações são enviadas via POST para as URLs de update/delete.
    // Apenas a inicialização básica do Bootstrap para os modais é necessária,
    // que já é feita automaticamente pelo Bootstrap.

    // No entanto, se houvesse a necessidade de preencher dinamicamente selects no futuro,
    // ou validações complexas, a classe DataManager seria usada aqui.

    // Exemplo de como você poderia usar o DataManager para enviar um formulário AJAX,
    // se quisesse evitar o refresh da página ao adicionar/editar (não implementado aqui para manter a consistência com o refresh do Django messages).
    /*
    const addLocalForm = document.querySelector('#modal-add-local form');
    if (addLocalForm) {
        addLocalForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(addLocalForm);
            try {
                // Supondo que a view de localidades retorne JSON se for AJAX
                const response = await dataManager.request(addLocalForm.action, 'POST', formData);
                console.log('Local adicionado:', response);
                dataManager.showAlert('Local adicionado com sucesso!', 'success');
                // Fechar modal e recarregar a tabela ou adicionar dinamicamente a linha
                const modal = bootstrap.Modal.getInstance(document.getElementById('modal-add-local'));
                if (modal) modal.hide();
                window.location.reload(); // Recarrega para mostrar a lista atualizada e mensagens
            } catch (error) {
                console.error('Erro ao adicionar local:', error);
                dataManager.showAlert('Erro ao adicionar local.', 'danger');
            }
        });
    }
    */
});
