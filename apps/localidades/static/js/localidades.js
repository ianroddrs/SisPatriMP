document.addEventListener('DOMContentLoaded', () => {/*
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
                window.location.reload();
            } catch (error) {
                console.error('Erro ao adicionar local:', error);
                dataManager.showAlert('Erro ao adicionar local.', 'danger');
            }
        });
    }
    */
});
