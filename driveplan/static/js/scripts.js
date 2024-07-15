

document.addEventListener('DOMContentLoaded', function() {

    const btnToggleLogin = document.getElementById('toggle-login');
    const formCliente = document.getElementById('form-cliente');
    const formMotorista = document.getElementById('form-motorista');

    btnToggleLogin.addEventListener('click', function() {
        if (formCliente.classList.contains('active')) {
            formCliente.classList.remove('active');
            formCliente.classList.add('inactive');
            formMotorista.classList.remove('inactive');
            formMotorista.classList.add('active');
            btnToggleLogin.textContent = 'Switch to Cliente';
        } else {
            formCliente.classList.remove('inactive');
            formCliente.classList.add('active');
            formMotorista.classList.remove('active');
            formMotorista.classList.add('inactive');
            btnToggleLogin.textContent = 'Switch to Motorista';
        }
    });


    formCliente.classList.add('active');
    formMotorista.classList.add('inactive');


    const registerForm = document.getElementById('registerModal').querySelector('form');
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        

        const name = document.getElementById('register-name').value;
        const email = document.getElementById('register-email').value;
        const phone = document.getElementById('register-phone').value;
        const cpfCnpj = document.getElementById('register-cpf-cnpj').value;
        const password = document.getElementById('register-password').value;
        const state = document.getElementById('register-state').value;
        const role = document.getElementById('register-role').value;


        console.log("Registrado:", { name, email, phone, cpfCnpj, password, state, role });


        registerForm.reset();
        bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
    });
});

