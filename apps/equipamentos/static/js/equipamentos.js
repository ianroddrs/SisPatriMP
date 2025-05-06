class Equipamentos{
    constructor(){
        this.localidades = this.getLocalidades()
    }

    getLocalidades(){
        fetch('api/localidades')
        .then(res => res.json())
        .then(data => {
            this.localidades = data.localidades
        })
    }   
}

let e = new Equipamentos()

let modal = document.querySelector('#modal-form')

if(modal){
    modal.addEventListener('show.bs.modal', async event => {
        let button = event.relatedTarget
        let modalTitle = modal.querySelector('.modal-title')
        let modalBody = modal.querySelector('.modal-body')
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