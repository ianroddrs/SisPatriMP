class Equipamentos{
    constructor(){
        this.filtro = document.querySelector('#filtro')
        this.exibir = document.querySelector('#exibir')
        this.agrupar = document.querySelector('#agrupar')
        this.detalhes = document.querySelector('#detalhes')

        this.tabela = document.querySelector('#tabela')

        this.modal = document.querySelector("#modal-form")
    }
}

let e = new Equipamentos()

if(e.modal){
    e.modal.addEventListener('show.bs.modal', async event => {
        let button = event.relatedTarget
        let modalTitle = e.modal.querySelector('.modal-title')
        let modalBody = e.modal.querySelector('.modal-body')
    })
}