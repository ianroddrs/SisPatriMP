let modal = document.querySelector('#modal-form')

if(modal){
    modal.addEventListener('show.bs.modal', async event => {
        let button = event.relatedTarget
        let response = await fetch('/static/html/formulario_cadastro_equipamento.html')
        let formulario = await response.text();

        let modalTitle = modal.querySelector('.modal-title')
        let modalBody = modal.querySelector('.modal-body')

        modalBody.innerHTML = formulario

        try {
            let response = await fetch('/api/datalists');
            let json = await response.json();
            localidades = json;
            
            function preencherTodosSelects() {
                Object.keys(localidades).forEach(id => {
                    let select = modalBody.querySelector(`#${id}`);
                    let options_list = localidades[id];
            
                    if (!select) return; // Se não existir o select, pula
            
                    select.innerHTML = ''; // Limpa o select
            
                    options_list.forEach(item => {
                        let opt = document.createElement('option');
                        opt.value = item.toUpperCase();
                        opt.textContent = item.toUpperCase();
                        select.appendChild(opt);
                    });
                });
            }
            
            preencherTodosSelects();
            
            // Agora adiciona o evento para TODOS os selects
            Object.keys(localidades).forEach(id => {
                let select = modalBody.querySelector(`#${id}`);
                if (!select) return;
            
                select.addEventListener('change', async e => {
                    let valor = e.target.value;
                    let name = e.target.name;
            
                    let url = '/api/datalists';
                    if (valor) {
                        // Se tiver valor selecionado, adiciona parâmetros na URL
                        url += `?${name}=${valor}`;
                    }
            
                    try {
                        let resp = await fetch(url);
            
                        if (!resp.ok) throw new Error('Erro na requisição');
            
                        let novoJson = await resp.json();
                        localidades = novoJson;
            
                        // Atualiza TODOS os selects com os novos dados
                        preencherTodosSelects();
                    } catch (err) {
                        console.error('Erro ao atualizar localidades:', err);
                    }
                });
            });
            
            

          } catch (error) {
            console.error('Fetch error:', error);
            callback(null);
          }
    })
}

async function enviarDados() {
    let formulario = document.querySelector('form')
    let inputs = formulario.querySelectorAll('input, select, textarea')
    let submit = true

    inputs.forEach(input => {
        if(input.required && (!input.value || input.value == "null")){
            input.classList.add('is-invalid')
            submit = false
        }
    })

    if(submit){
        formulario.submit()
    }else{
        alert('Preencha os campos obrigatórios')
    }
}