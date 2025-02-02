
// Validaciones de formulario
$(function () {
    $("#formulario").validate({
        rules: {
            nombre: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            edad: {
                required: true,
            },
            fono: {
                required: true,
                number: true
            },
            direccion: {
                required: true,

            }
        }, //rules
        messages: {
            nombre: {
                required: 'Ingrese su nombre',
                minlength: 'Caracteres insuficientes'
            },
            email: {
                required: 'Ingresa tu correo electrónico',
                email: 'Formato de correo no válido'
            },
            edad: {
                required: 'Ingrese su edad',
            },
            fono: {
                required: 'Ingrese un número de celular',
                minlength: 'Cantidad de digitos insuficiente'
            },
            direccion: {
                required: 'Ingrese su domicilio'
            }
        }
    });
});

// Alerta para formulario
// $(function () {
//     $('#enviar').click(function () {
//         // $('.alerta').show()
//         if($('#nombre').val() != ""){
//             $('.alerta').show()
//         }
//         else{
//             $('.alerta2').show()
//         }
//     })
// });

// Calculadora
$(function () {
    $('#sumar').click(function () {
        document.getElementById('resultado').value += '+';
    });
    $('#restar').click(function () {
        document.getElementById('resultado').value += '-';
    });
    $('#multiplicar').click(function () {
        document.getElementById('resultado').value += '*';
    });
    $('#dividir').click(function () {
        document.getElementById('resultado').value += '/';
    });

    $('#7').click(function () {
        document.getElementById('resultado').value += '7';
    });
    $('#8').click(function () {
        document.getElementById('resultado').value += '8';
    });
    $('#9').click(function () {
        document.getElementById('resultado').value += '9';
    });

    $('#4').click(function () {
        document.getElementById('resultado').value += '4';
    });
    $('#5').click(function () {
        document.getElementById('resultado').value += '5';
    });
    $('#6').click(function () {
        document.getElementById('resultado').value += '6';
    });

    $('#1').click(function () {
        document.getElementById('resultado').value += '1';
    });
    $('#2').click(function () {
        document.getElementById('resultado').value += '2';
    });
    $('#3').click(function () {
        document.getElementById('resultado').value += '3';
    });

    $('#0').click(function () {
        document.getElementById('resultado').value += '0';
    });
    $('#p').click(function () {
        document.getElementById('resultado').value += '.';
    });

    $('#reset').click(function () {
        document.getElementById('resultado').value = '';
    });


    $('#equal').click(function () {
        var result = eval($('#resultado').val());
        $('#resultado').val(result);
    });
});

// Api de Google Maps
// function iniciarMap(){
//     var coord = {lat:-33.4157558 ,lng: -70.7092091};

//     var map = new google.maps.Map(document.getElementById('map'),{
//         zoom: 10,
//         center: coord
//     });

//     var marker = new google.maps.Marker({
//         position: coord,
//         map: map
//     });
// }

function consultarPokemon(id) {

    fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
        .then(response => response.json())
        .then(data => crearPokemon(data))
        .catch(error => console.log(error))
}

function randomPokemon() {
    let primerId = Math.round(Math.random() * 150);

    consultarPokemon(primerId);
}

function crearPokemon(data) {
    var nombre = document.getElementById("nombre");
    var imagen = document.getElementById("poke");
    var numero = document.getElementById("numero");

    imagen.setAttribute("src", data.sprites.other.home.front_shiny);
    nombre.textContent = data.name;
    numero.textContent = "N°: " + data.id;
}

const carritoBtn = document.getElementById('carrito');
const carritoContainer = document.getElementById('carrito2');

carritoBtn.addEventListener('click', () => {
    carritoContainer.classList.toggle('show');
});

const carritoCerrarBtn = document.getElementById('carrito-cerrar');

carritoCerrarBtn.addEventListener('click', () => {
    carritoContainer.classList.remove('show');
});
