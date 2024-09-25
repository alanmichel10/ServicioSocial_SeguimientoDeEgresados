document.addEventListener('DOMContentLoaded', function () {
    const trabajoInput = document.getElementById('trabajoInput');
    const camposNA = document.querySelectorAll('[data-na]');

    trabajoInput.addEventListener('change', function () {
        if (this.value === 'No') {
            camposNA.forEach(function (campo) {
                if (campo.tagName === 'SELECT') {
                    // Si es un campo de selección, selecciona la opción "N/A"
                    campo.value = 'NoAplica';
                    campo.setAttribute('readonly', true);
                } else {
                    // Si es un campo de texto, establece el valor en "N/A" y marca como solo lectura
                    campo.value = 'N/A';
                    campo.setAttribute('readonly', true);
                }
            });
        } else {
            camposNA.forEach(function (campo) {
                if (campo.tagName === 'SELECT') {
                    // Si es un campo de selección, selecciona la primera opción y habilita el campo
                    campo.selectedIndex = 0;
                    campo.removeAttribute('readonly');
                } else {
                    // Si es un campo de texto, establece el valor en blanco y habilita el campo
                    campo.value = '';
                    campo.removeAttribute('readonly');
                }
            });
        }
    });
});
