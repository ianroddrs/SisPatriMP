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
        fetch('?action=localidades')
        .then(res => res.json())
        .then(data => {
            let localidades = JSON.parse(data.localidades)
            this.localidades = localidades
        })
    }
}

let e = new Equipamentos()

function adicionarOptions(){
    let options = {
        polos : Object.keys(e.localidades),
        cidades : Object.values(e.localidades).flatMap(polo => Object.keys(polo)),
        locais : Object.values(e.localidades).flatMap(polo =>Object.values(polo).flat())
    }

    Object.keys(options).forEach(i=>{
        let select = e.modal.querySelector([`select#${i}`])
        options[i].forEach(j=>{
            let option = document.createElement('option')
            option.value = j
            option.textContent = j
            select.appendChild(option)
        })

        select.addEventListener('change', () => {
            
        })
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