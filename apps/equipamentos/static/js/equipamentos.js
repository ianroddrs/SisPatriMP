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

            Object.keys(localidades).forEach(id => {
                let datalist = modalBody.querySelector(`#${id}`)
                let options_list = localidades[id]
                
                options_list.forEach(item =>{
                    let opt = document.createElement('option')
                    opt.value = item.toUpperCase()
                    opt.textContent = item.toUpperCase()
                    datalist.appendChild(opt)
                })
            })
            

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