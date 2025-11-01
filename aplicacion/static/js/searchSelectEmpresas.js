const arrayEmpresas = [
    { id: 1, nombre: "Total" },
    { id: 2, nombre: "Star gas" },
    { id: 3, nombre: "Jadever" },
    { id: 4, nombre: "Overland" }
];

// Elementos del DOM

const searchInputEmpresa = document.getElementById('searchInputEmpresa');
const customSelectEmpresa = document.getElementById('customSelectEmpresa');
const selectedValueEmpresa = document.getElementById('selectedValueEmpresa');
const selectedTextEmpresa = document.getElementById('selectedTextEmpresa');
let selectEmpresa = null;

// Función para filtrar y mostrar opciones
function filterOptionsEmpresas(searchTerm = '') {
    const filteredEmpresas = arrayEmpresas.filter(empresa => 
        empresa.nombre.toLowerCase().includes(searchTerm.toLowerCase())
    );

    renderOptionsEmpresas(filteredEmpresas);
}

// Función para renderizar las opciones
function renderOptionsEmpresas(empresas) {
    customSelectEmpresa.innerHTML = '';

    if (empresas.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No se encontraron resultados';
        customSelectEmpresa.appendChild(noResults);
        return;
    }

    empresas.forEach(empresa => {
        const option = document.createElement('div');
        option.className = 'custom-option';
        option.dataset.value = empresa.id;
        option.innerHTML = `
            <strong>${empresa.nombre}</strong>
        `;

        option.addEventListener('click', () => {
            selectOptionEmpresas(option, empresa);
        });

        customSelectEmpresa.appendChild(option);
    });
}


// Función para seleccionar una opción

function selectOptionEmpresas(optionElement, empresa) {
    // Remover selección anterior
    if (selectedOption) {
        selectedOption.classList.remove('selected');
    }

    // Marcar como seleccionado
    optionElement.classList.add('selected');
    selectedOption = optionElement;

    // Actualizar valores
    selectedValueEmpresa.value = empresa.id;
    selectedTextEmpresa.textContent = empresa.nombre;
    searchInputEmpresa.value = empresa.nombre;

    // Ocultar el dropdown
    customSelectEmpresa.classList.remove('show');
}

// Event Listeners
// Event Listeners EMPRESAS
searchInputEmpresa.addEventListener('focus', () => {
    customSelectEmpresa.classList.add('show');
    filterOptionsEmpresas();
});

searchInputEmpresa.addEventListener('input', (e) => {
    filterOptionsEmpresas(e.target.value);
});

searchInputEmpresa.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        const firstOption = customSelectEmpresa.querySelector('.custom-option');
        if (firstOption) firstOption.focus();
    }
});

// Cerrar dropdown al hacer clic fuera
document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-select-container')) {
        customSelectEmpresa.classList.remove('show');
    }
});


// Navegación con teclado
customSelectEmpresa.addEventListener('keydown', (e) => {
    const options = Array.from(customSelectEmpresa.querySelectorAll('.custom-option'));
    const currentIndex = options.indexOf(document.activeElement);

    switch(e.key) {
        case 'ArrowDown':
            e.preventDefault();
            if (currentIndex < options.length - 1) {
                options[currentIndex + 1].focus();
            }
            break;
        case 'ArrowUp':
            e.preventDefault();
            if (currentIndex > 0) {
                options[currentIndex - 1].focus();
            } else {
                searchInputEmpresa.focus();
            }
            break;
        case 'Enter':
            e.preventDefault();
            if (document.activeElement.classList.contains('custom-option')) {
                const empresa = arrayEmpresas.find(c => c.id == document.activeElement.dataset.value);
                selectOptionEmpresas(document.activeElement, empresa);
            }
            break;
        case 'Escape':
            customSelectEmpresa.classList.remove('show');
            searchInputEmpresa.focus();
            break;
    }
});

// Inicializar
filterOptionsEmpresas();