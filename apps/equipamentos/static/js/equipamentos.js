let modal = document.querySelector('#modal-form')

if(modal){
    modal.addEventListener('show.bs.modal', async event => {
        let button = event.relatedTarget
        let response = await fetch('/static/html/formulario_cadastro_equipamento.html')
        let formulario = await response.text();

        let modalTitle = modal.querySelector('.modal-title')
        let  modalBody = modal.querySelector('.modal-body')


        modalBody.innerHTML = formulario

        modalBody.querySelectorAll('select').forEach(select => {
            new TomSelect(select, {
                create: true,
                createOnBlur: true,     
                render: {
                    option_create: function(data, escape) {
                        return `<div class="create bg-white">Adicionar <strong>${escape(data.input)}</strong>&hellip;</div>`;
                    },
                    no_results: function() {
                        return '<div class="no-results bg-white">Nenhum resultado encontrado</div>';
                    },
                    item: function(data) {
                        return `<div class="tom-select-item rounded bg-white">${data.valor.toUpperCase()}</div>`;
                    },
                    option: function(data) {
                        return `<div class="tom-select-option rounded bg-white">${data.text}</div>`;
                    },
                    dropdown: function() {
                        return '<div class="rounded-3 border p-2 bg-white"></div>';
                    }
                },
                valueField: "id",
                labelField: "valor",
                searchField: "valor",
                load: function(query, callback){
                    fetch(`/api/localidades?${select.name}=${encodeURIComponent(query)}`)
                        .then(response => response.json())
                        .then(json => callback(json))
                        .catch(() => callback)
                }
            })
        })
    })
}

async function enviarDados() {
    document.querySelector('form').submit()
}