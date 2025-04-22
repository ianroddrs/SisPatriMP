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
            let response = await fetch('/api/localidades');
            let json = await response.json();
            localidades = json;

            modalBody.querySelectorAll('datalist').forEach(datalist => {
                let options_list = localidades[datalist.id]
                let opt = document.createElement('option')

                options_list.forEach(item =>{
                    console.log(item)
                    opt.value = item
                })

                // datalist.appendChild(opt)
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
        if(input.required && (!input.value || input.value == "Selecione uma opção")){
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