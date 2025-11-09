let arraySecciones = []

const getSecciones = async (id) => {
    const url = `/inces/secciones/${id}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        arraySecciones = data.secciones;

        if (arraySecciones.length > 0) {
            document.getElementById('selectSeccion').style.display = 'block';
        }

    } catch(e) {
        console.error(e);
    }
}

// Elementos del DOM

const searchInputSecciones = document.getElementById('searchInputSecciones');
const customSelectSecciones = document.getElementById('customSelectSecciones');
const selectedValueSecciones = document.getElementById('selectedValueSecciones');
const selectedTextSecciones = document.getElementById('selectedTextSecciones');
let selectSec = null;

// Función para filtrar y mostrar opciones
async function filterOptionsSecciones(searchTerm = '') {
    await getSecciones();
    const filteredSecciones = arraySecciones.filter(sec => 
        sec.seccion.toLowerCase().includes(searchTerm.toLowerCase())
    );

    renderOptionsSecciones(filteredSecciones);
}

// Función para renderizar las opciones
function renderOptionsSecciones(secciones) {
    customSelectEmpresa.innerHTML = '';

    if (secciones.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No se encontraron resultados';
        customSelectEmpresa.appendChild(noResults);
        return;
    }

    secciones.forEach(sec => {
        const option = document.createElement('div');
        option.className = 'custom-option';
        option.dataset.value = sec.idSeccion;
        option.innerHTML = `
            <strong>${sec.seccion}</strong>
        `;

        option.addEventListener('click', () => {
            selectOptionSecciones(option, sec);
        });

        customSelectSecciones.appendChild(option);
    });
}


// Función para seleccionar una opción

function selectOptionSecciones(optionElement, seccion) {
    // Remover selección anterior
    if (selectedOption) {
        selectedOption.classList.remove('selected');
    }

    // Marcar como seleccionado
    optionElement.classList.add('selected');
    selectedOption = optionElement;

    // Actualizar valores
    selectedValueSecciones.value = seccion.idSeccion;
    selectedTextSecciones.textContent = seccion.seccion;
    searchInputSecciones.value = seccion.seccion;

    // Ocultar el dropdown
    customSelectSecciones.classList.remove('show');
}

// Event Listeners
// Event Listeners EMPRESAS
searchInputSecciones.addEventListener('focus', () => {
    customSelectSecciones.classList.add('show');
    filterOptionsSecciones();
});

searchInputSecciones.addEventListener('input', (e) => {
    filterOptionsSecciones(e.target.value);
});

searchInputSecciones.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        const firstOption = customSelectSecciones.querySelector('.custom-option');
        if (firstOption) firstOption.focus();
    }
});

// Cerrar dropdown al hacer clic fuera
document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-select-container')) {
        customSelectSecciones.classList.remove('show');
    }
});


// Navegación con teclado
customSelectSecciones.addEventListener('keydown', (e) => {
    const options = Array.from(customSelectSecciones.querySelectorAll('.custom-option'));
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
                searchInputSecciones.focus();
            }
            break;
        case 'Enter':
            e.preventDefault();
            if (document.activeElement.classList.contains('custom-option')) {
                const seccion = arraySecciones.find(c => c.idSeccion == document.activeElement.dataset.value);
                selectOptionSecciones(document.activeElement, seccion);
            }
            break;
        case 'Escape':
            customSelectSecciones.classList.remove('show');
            searchInputSecciones.focus();
            break;
    }
});

// Inicializar
filterOptionsSecciones();

