const outputLog = document.getElementById('outputLog');
const startButton = document.getElementById('startButton');
const loadingSpinner = document.getElementById('loadingSpinner');


function appendToLog(message, className = '') {
    const p = document.createElement('p');
    p.textContent = message;
    if (className) {
        p.classList.add(className);
    }
    outputLog.appendChild(p);
    outputLog.scrollTop = outputLog.scrollHeight; // Rola para o final
}

async function startVerification() {
    showLoading(); // Exibe o carregamento

    try {
        // Faz uma requisição para o endpoint da API Django
        const response = await fetch('api/printers_status/');
        
        if (!response.ok) {
            appendToLog(`Erro ao chamar a API: ${response.status} ${response.statusText}`, 'status-error');
            return;
        }

        const data = await response.json();
        
        if (data.results && data.results.length > 0) {
            data.results.forEach(item => {
                let message = `URL: ${item.url}`;
                let className = '';

                if (item.status === "OK") {
                    message += ` | Status: ${item.content}`;
                }else{
                    message += ` | Status: Sem Conexão`;

                }
                
                appendToLog(message, className);
            });
        } else {
            appendToLog("Nenhum resultado retornado pela API.", 'status-warning');
        }

    } catch (error) {
        appendToLog(`Erro inesperado ao buscar dados da API: ${error.message}`, 'status-error');
        console.error('Erro ao buscar dados da API:', error);
    } finally {
        hideLoading(); // Esconde o carregamento
    }
}