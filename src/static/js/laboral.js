document.addEventListener('DOMContentLoaded', function () {
    const trabajoInput = document.getElementById('trabajoInput');
    const camposNA = document.querySelectorAll('[data-na]');

    trabajoInput.addEventListener('change', function () {
        if (this.value === 'No') {
            camposNA.forEach(function (campo) {
                if (campo.tagName === 'SELECT') {
                    // Si es un campo de selección, selecciona la opción "N/A"
                    campo.value = 'NoAplica';
                    campo.style.pointerEvents = 'none';
                } else {
                    // Si es un campo de texto, establece el valor en "N/A"
                    campo.value = 'N/A';
                    campo.readOnly = true;
                }
                campo.style.backgroundColor = '#e9ecef'; // Color de fondo para indicar que no es editable
            });
        } else {
            camposNA.forEach(function (campo) {
                if (campo.tagName === 'SELECT') {
                    // Si es un campo de selección, selecciona la primera opción y habilita el campo
                    campo.selectedIndex = 0;
                    campo.style.pointerEvents = 'auto';
                } else {
                    // Si es un campo de texto, establece el valor en blanco y habilita el campo
                    campo.value = '';
                    campo.readOnly = false;
                }
                campo.style.backgroundColor = ''; // Restaura el color de fondo original
            });
        }
    });

    // Evitar que el usuario escriba en los campos cuando están en modo "N/A"
    camposNA.forEach(function (campo) {
        campo.addEventListener('input', function () {
            if (trabajoInput.value === 'No') {
                if (this.tagName === 'SELECT') {
                    this.value = 'NoAplica';
                } else {
                    this.value = 'N/A';
                }
            }
        });
    });
});