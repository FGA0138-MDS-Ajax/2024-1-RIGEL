document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        height: 'auto',
        dateClick: function(info) {
            $('#addEventModal').modal('show');
            document.getElementById('eventDate').value = info.dateStr;
        },
        eventClick: function(info) {
            if (confirm(`Deseja realmente excluir o evento '${info.event.title}'?`)) {
                info.event.remove();
                removeEventFromCronograma(info.event.id);
                removeEventNotification(info.event.id);
            }
        }
    });
    calendar.render();

    document.getElementById('calendario-btn').addEventListener('click', function() {
        showSection('calendario');
        calendar.render();
    });

    document.getElementById('cronograma-btn').addEventListener('click', function() {
        showSection('cronograma');
    });

    document.getElementById('financeiro-btn').addEventListener('click', function() {
        showSection('financeiro');
        updateFinanceiroSummary();
    });

    document.getElementById('clientes-btn').addEventListener('click', function() {
        showSection('clientes');
    });

    document.getElementById('viagens-btn').addEventListener('click', function() {
        showSection('viagens');
    });

    document.getElementById('modelo-viagem-btn').addEventListener('click', function() {
        showSection('modelo-viagem');
    });

    function showSection(sectionId) {
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });
        document.getElementById(sectionId).style.display = 'block';
    }

    document.getElementById('addEventForm').addEventListener('submit', function(e) {
        e.preventDefault();
        var eventName = document.getElementById('eventName').value;
        var eventDate = document.getElementById('eventDate').value;
        var eventTime = document.getElementById('eventTime').value;

        var event = {
            id: Date.now().toString(),
            title: eventName,
            start: eventDate + 'T' + eventTime,
            allDay: false
        };

        calendar.addEvent(event);
        addEventToCronograma(event);
        addNotification(event);
        $('#addEventModal').modal('hide');
        document.getElementById('addEventForm').reset();
    });

    function addEventToCronograma(event) {
        var date = new Date(event.start);
        var day = date.getDate();
        var month = date.getMonth() + 1; // Months are zero-based
        var year = date.getFullYear();
        var monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                          "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
        var monthName = monthNames[month - 1];

        var monthSection = document.getElementById('month-' + month);
        if (!monthSection) {
            monthSection = document.createElement('div');
            monthSection.id = 'month-' + month;
            monthSection.className = 'list-group-item';
            monthSection.innerHTML = `<h5>${monthName} ${year}</h5><div id="events-month-${month}"></div>`;
            document.getElementById('list-cronograma').appendChild(monthSection);
        }

        var eventsContainer = document.getElementById('events-month-' + month);
        if (eventsContainer) {
            var eventDiv = document.createElement('div');
            eventDiv.id = event.id;
            eventDiv.className = 'event-div';
            eventDiv.textContent = `${event.title} - Dia ${day}, ${event.start.split('T')[1]}`;
            eventsContainer.appendChild(eventDiv);
        }
    }

    function removeEventFromCronograma(eventId) {
        var eventDiv = document.getElementById(eventId);
        if (eventDiv) {
            eventDiv.remove();
        }
    }

    function addNotification(event) {
        var notificationsContainer = document.getElementById('notifications');
        var notification = document.createElement('div');
        notification.id = event.id;
        notification.className = 'notification-item alert alert-success';
        notification.textContent = `${event.title} em ${event.start.split('T')[0]} às ${event.start.split('T')[1]}`;
        notificationsContainer.appendChild(notification);
    }

    function removeEventNotification(eventId) {
        var notification = document.getElementById(eventId);
        if (notification) {
            notification.remove();
        }
    }

    $('#notifications-collapse').on('shown.bs.collapse', function () {
        document.getElementById('notification-icon').className = 'fas fa-chevron-up';
    });

    $('#notifications-collapse').on('hidden.bs.collapse', function () {
        document.getElementById('notification-icon').className = 'fas fa-chevron-down';
    });

    // Funcionalidade do modelo de viagem
    const editBtn = document.getElementById('editBtn');
    const saveBtn = document.getElementById('saveBtn');
    const taxaKmInput = document.getElementById('taxaKm');
    const taxaMinEsperaInput = document.getElementById('taxaMinEspera');
    const modeloForm = document.getElementById('modeloForm');

    editBtn.addEventListener('click', function() {
        taxaKmInput.disabled = false;
        taxaMinEsperaInput.disabled = false;
        saveBtn.style.display = 'inline'; // Exibir botão Salvar
        editBtn.style.display = 'none'; // Ocultar botão Editar
    });

    modeloForm.addEventListener('submit', function(e) {
        e.preventDefault();
        taxaKmInput.disabled = true;
        taxaMinEsperaInput.disabled = true;
        saveBtn.style.display = 'none'; // Ocultar botão Salvar
        editBtn.style.display = 'inline'; // Exibir botão Editar
        console.log('Modelo Salvo:', taxaKmInput.value, taxaMinEsperaInput.value); // Log dos valores salvos
    });

    // Funcionalidade de Viagens
    const viagensForm = document.getElementById('viagensForm');
    const viagensList = document.getElementById('viagensList');
    const financeiroList = document.getElementById('financeiroList');

    viagensForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const cliente = document.getElementById('viagemCliente').value;
        const data = document.getElementById('viagemData').value;
        const hora = document.getElementById('viagemHora').value;
        const valor = parseFloat(document.getElementById('viagemValor').value).toFixed(2);

        const viagem = {
            id: Date.now().toString(),
            cliente,
            data,
            hora,
            valor,
            status: 'Não pago'
        };

        addViagemToList(viagem);
        addViagemToFinanceiro(viagem);
        saveViagensToLocalStorage(); // Salvar as viagens no Local Storage
        viagensForm.reset();
    });

    function addViagemToList(viagem) {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.setAttribute('data-id', viagem.id);
        li.innerHTML = `
            ${viagem.cliente} - ${viagem.data}
            <div>
                <button class="btn btn-sm btn-danger" onclick="removeViagem('${viagem.id}')">Remover</button>
            </div>
        `;
        viagensList.appendChild(li);
    }

    function addViagemToFinanceiro(viagem) {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.setAttribute('data-id', viagem.id);
        li.setAttribute('data-valor', viagem.valor);
        li.innerHTML = `
            ${viagem.cliente} - ${viagem.data} - R$${viagem.valor}
            <div>
                <select class="form-control form-control-sm status-select">
                    <option value="Não pago" ${viagem.status === 'Não pago' ? 'selected' : ''}>Não pago</option>
                    <option value="Em andamento" ${viagem.status === 'Em andamento' ? 'selected' : ''}>Em andamento</option>
                    <option value="Pago" ${viagem.status === 'Pago' ? 'selected' : ''}>Pago</option>
                </select>
                <button class="btn btn-sm btn-danger" onclick="removeViagem('${viagem.id}')">Remover</button>
            </div>
        `;
        financeiroList.appendChild(li);

        li.querySelector('.status-select').addEventListener('change', function() {
            viagem.status = this.value;
            updateViagemStatus(viagem.id, this.value);
            updateFinanceiroSummary();
            saveViagensToLocalStorage(); // Salvar as viagens no Local Storage
        });
    }

    function updateViagemStatus(viagemId, status) {
        const viagemItem = document.querySelector(`#viagensList [data-id='${viagemId}']`);
        if (viagemItem) {
            viagemItem.querySelector('.badge').textContent = status;
        }
    }

    function updateFinanceiroSummary() {
        let totalRecebido = 0;
        let totalAReceber = 0;

        document.querySelectorAll('#financeiroList .list-group-item').forEach(item => {
            const valor = parseFloat(item.getAttribute('data-valor'));
            const status = item.querySelector('.status-select').value;

            if (status === 'Pago') {
                totalRecebido += valor;
            } else if (status === 'Em andamento') {
                totalAReceber += valor;
            }
        });

        document.getElementById('totalRecebido').textContent = `Total Recebido: R$${totalRecebido.toFixed(2)}`;
        document.getElementById('totalAReceber').textContent = `Total a Receber: R$${totalAReceber.toFixed(2)}`;
    }

    function saveViagensToLocalStorage() {
        const viagens = [];
        document.querySelectorAll('#viagensList .list-group-item').forEach(item => {
            const id = item.getAttribute('data-id');
            const [cliente, data] = item.textContent.split(' - ');
            const status = item.querySelector('.status-select').value;
            viagens.push({ id, cliente, data, status });
        });
        localStorage.setItem('viagens', JSON.stringify(viagens));
    }

    function loadViagensFromLocalStorage() {
        const viagens = JSON.parse(localStorage.getItem('viagens')) || [];
        viagens.forEach(viagem => {
            addViagemToList(viagem);
            addViagemToFinanceiro(viagem);
        });
        updateFinanceiroSummary();
    }

    window.removeViagem = function(id) {
        const viagemItem = document.querySelector(`#viagensList [data-id='${id}']`);
        const financeiroItem = document.querySelector(`#financeiroList [data-id='${id}']`);
        if (viagemItem) viagemItem.remove();
        if (financeiroItem) financeiroItem.remove();
        saveViagensToLocalStorage();
        updateFinanceiroSummary();
    };

    // Funcionalidade de Clientes
    const clientesForm = document.getElementById('clientesForm');
    const clientesList = document.getElementById('clientesList');

    clientesForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const nome = document.getElementById('clienteNome').value;
        const email = document.getElementById('clienteEmail').value;
        const telefone = document.getElementById('clienteTelefone').value;
        const cpf = document.getElementById('clienteCPF').value;

        const cliente = {
            id: Date.now().toString(),
            nome,
            email,
            telefone,
            cpf
        };

        addClienteToList(cliente);
        clientesForm.reset();
    });

    function addClienteToList(cliente) {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `${cliente.nome} - ${cliente.email} - ${cliente.telefone} - ${cliente.cpf}`;
        clientesList.appendChild(li);
    }

    loadViagensFromLocalStorage(); // Carregar as viagens do Local Storage ao inicializar a página
});

















