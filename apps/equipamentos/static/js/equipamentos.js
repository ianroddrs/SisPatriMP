let modal = document.querySelector('#modal-form')

if(modal){
    modal.addEventListener('show.bs.modal', async event => {
        let button = event.relatedTarget
        let response = await fetch('/static/html/formulario_cadastro_equipamento.html')
        let formulario = await response.text();

        let modalTitle = modal.querySelector('.modal-title')
        let  modalBody = modal.querySelector('.modal-body')


        modalBody.innerHTML = formulario

        modalBody.querySelectorAll('select').forEach(async select => {
            // let localidades = await fetch(`/api/localidades?${select.name}=${encodeURIComponent(query)}`)
            try {
                const response = await fetch('/api/localidades');
                const json = await response.json();
                localidades = json;
                callback(json); // optionally call the callback
              } catch (error) {
                console.error('Fetch error:', error);
                callback(null); // or handle error as needed
              }
              
              console.log(localidades);
        })
    })
}

async function enviarDados() {
    let formulario = document.querySelector('form')
    let inputs = formulario.querySelectorAll('input, select, textarea')
    let submit= true

    inputs.forEach(input => {
        if(input.required && !input.value){
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