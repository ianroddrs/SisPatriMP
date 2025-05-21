class Equipamentos{
    constructor(){
        this.localidades = this.getLocalidades()

        this.filtro = document.querySelector('#filtro')
        this.exibir = document.querySelector('#exibir')
        this.agrupar = document.querySelector('#agrupar')
        this.detalhes = document.querySelector('#detalhes')

        this.tabela = document.querySelector('#tabela')

        this.modal = document.querySelector("#modal-form")
    }

    getLocalidades(){
        fetch('/static/json/relacao_polos_cidades.json')
        .then(res => res.json())
        .then(data => {
            this.localidades = data
        })
    }
}

let e = new Equipamentos()

function adicionarOptions(){
    let select = e.modal.querySelector('select#cidades')

    Object.keys(e.localidades).forEach(polo => {
        let cidades = e.localidades[polo]

        let optgroup = document.createElement('optgroup')
        optgroup.label = polo

        cidades.forEach(cidade => {
            let option = document.createElement('option')
            option.value = cidade
            option.textContent = cidade

            optgroup.appendChild(option)
        })

        select.appendChild(optgroup)
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

if(e.modal){
    e.modal.addEventListener('show.bs.modal', async event => {
        let button = event.relatedTarget
        let modalTitle = e.modal.querySelector('.modal-title')
        let modalBody = e.modal.querySelector('.modal-body')
        adicionarOptions()
    })
}