// static/js/main.js

/**
 * Classe utilitária para gerenciar requisições de dados (AJAX) e operações comuns de UI.
 */
class DataManager {
    constructor() {
        this.csrfToken = this._getCookie('csrftoken');
    }

    /**
     * Obtém o token CSRF dos cookies.
     * @param {string} name - Nome do cookie.
     * @returns {string|null} O valor do cookie ou null se não encontrado.
     * @private
     */
    _getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Realiza uma requisição HTTP (GET, POST, PUT, DELETE).
     * @param {string} url - A URL para a requisição.
     * @param {string} method - O método HTTP (GET, POST, PUT, DELETE).
     * @param {Object|FormData|null} data - Os dados a serem enviados (para POST/PUT).
     * @returns {Promise<Object>} Uma promessa que resolve com os dados da resposta JSON.
     */
    async request(url, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'X-CSRFToken': this.csrfToken,
            },
        };

        if (data) {
            // Se os dados não forem FormData, assume que é JSON
            if (!(data instanceof FormData)) {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(data);
            } else {
                // Se for FormData, o navegador define o Content-Type automaticamente
                options.body = data;
            }
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                // Tenta ler a mensagem de erro do backend se disponível
                const errorData = await response.json().catch(() => ({ message: response.statusText }));
                throw new Error(errorData.message || 'Erro na requisição.');
            }
            // Verifica se a resposta tem conteúdo antes de tentar parsear como JSON
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                // Se não for JSON, pode ser uma resposta de sucesso sem conteúdo (ex: 204 No Content)
                return { success: true, message: 'Operação realizada com sucesso.' };
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            // Rejeita a promessa para que o código chamador possa capturar o erro
            throw error; 
        }
    }

    /**
     * Exibe uma mensagem de alerta Bootstrap.
     * @param {string} message - A mensagem a ser exibida.
     * @param {string} type - O tipo de alerta (success, danger, info, warning).
     */
    showAlert(message, type) {
        const alertContainer = document.querySelector('.alert-container') || document.createElement('div');
        if (!alertContainer.classList.contains('alert-container')) {
            alertContainer.classList.add('alert-container');
            document.querySelector('main').prepend(alertContainer); // Assume que 'main' é o container principal
        }
        
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        alertContainer.innerHTML = alertHtml;

        setTimeout(() => {
            const alertElement = alertContainer.querySelector('.alert');
            if (alertElement) {
                const bsAlert = new bootstrap.Alert(alertElement);
                bsAlert.close();
            }
        }, 5000); // Remove o alerta após 5 segundos
    }
}

// Exporta uma instância da classe para ser usada globalmente ou importada
window.dataManager = new DataManager();

// Adiciona um container para mensagens de alerta, se não existir
document.addEventListener('DOMContentLoaded', () => {
    let alertContainer = document.querySelector('.alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.classList.add('alert-container');
        const mainContent = document.querySelector('main'); // ou outro container principal
        if (mainContent) {
            mainContent.prepend(alertContainer);
        } else {
            document.body.prepend(alertContainer);
        }
    }
});
