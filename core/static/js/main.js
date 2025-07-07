class DataManager {
    constructor() {
        this.csrfToken = this._getCookie('csrftoken');
    }

    _getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async request(url, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'X-CSRFToken': this.csrfToken,
            },
        };

        if (data) {
            if (!(data instanceof FormData)) {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(data);
            } else {
                options.body = data;
            }
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: response.statusText }));
                throw new Error(errorData.message || 'Erro na requisição.');
            }
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return { success: true, message: 'Operação realizada com sucesso.' };
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error; 
        }
    }

    showAlert(message, type) {
        const alertContainer = document.querySelector('.alert-container') || document.createElement('div');
        if (!alertContainer.classList.contains('alert-container')) {
            alertContainer.classList.add('alert-container');
            document.querySelector('main').prepend(alertContainer);
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
        }, 5000);
    }
}

window.dataManager = new DataManager();

// Adiciona um container para mensagens de alerta, se não existir
document.addEventListener('DOMContentLoaded', () => {
    let alertContainer = document.querySelector('.alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.classList.add('alert-container');
        const mainContent = document.querySelector('main');
        if (mainContent) {
            mainContent.prepend(alertContainer);
        } else {
            document.body.prepend(alertContainer);
        }
    }
});
