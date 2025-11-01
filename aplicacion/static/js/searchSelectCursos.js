// Array de prueba - arrayCursos
let arrayCursos = [
    { id: 1, nombre: "Matemáticas Avanzadas", categoria: "Ciencias" },
    { id: 2, nombre: "Programación en JavaScript", categoria: "Tecnología" },
    { id: 3, nombre: "Historia del Arte", categoria: "Humanidades" },
    { id: 4, nombre: "Física Cuántica", categoria: "Ciencias" },
    { id: 5, nombre: "Desarrollo Web Full Stack", categoria: "Tecnología" },
    { id: 6, nombre: "Literatura Contemporánea", categoria: "Humanidades" },
    { id: 7, nombre: "Química Orgánica", categoria: "Ciencias" },
    { id: 8, nombre: "Inteligencia Artificial", categoria: "Tecnología" },
    { id: 9, nombre: "Filosofía Moderna", categoria: "Humanidades" },
    { id: 10, nombre: "Biología Molecular", categoria: "Ciencias" }
];

const getCursos = async () => {
    const url = '/inces/cursos';

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.error);

    if (data.cursos.length > 0) arrayCursos = data.cursos;
}

// Elementos del DOM
const searchInput = document.getElementById('searchInput');
const customSelect = document.getElementById('customSelect');
const selectedValue = document.getElementById('selectedValue');
const selectedText = document.getElementById('selectedText');

let selectedOption = null;

// Función para filtrar y mostrar opciones
async function filterOptions(searchTerm = '') {
    await getCursos();
    const filteredCursos = arrayCursos.filter(curso => 
        curso.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        curso.categoria.toLowerCase().includes(searchTerm.toLowerCase())
    );

    renderOptions(filteredCursos);
}

// Función para renderizar las opciones
function renderOptions(cursos) {
    customSelect.innerHTML = '';

    if (cursos.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = 'No se encontraron resultados';
        customSelect.appendChild(noResults);
        return;
    }

    cursos.forEach(curso => {
        const option = document.createElement('div');
        option.className = 'custom-option';
        option.dataset.value = curso.id;
        option.innerHTML = `
            <strong>${curso.nombre}</strong>
            <br>
            <small class="text-muted">${curso.categoria}</small>
        `;

        option.addEventListener('click', () => {
            selectOption(option, curso);
        });

        customSelect.appendChild(option);
    });
}

// Función para seleccionar una opción
function selectOption(optionElement, curso) {
    // Remover selección anterior
    if (selectedOption) {
        selectedOption.classList.remove('selected');
    }

    // Marcar como seleccionado
    optionElement.classList.add('selected');
    selectedOption = optionElement;

    // Actualizar valores
    selectedValue.value = curso.id;
    selectedText.textContent = curso.nombre;
    searchInput.value = curso.nombre;

    // Ocultar el dropdown
    customSelect.classList.remove('show');
}

// Event Listeners
searchInput.addEventListener('focus', () => {
    customSelect.classList.add('show');
    filterOptions();
});

searchInput.addEventListener('input', (e) => {
    filterOptions(e.target.value);
});

searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        const firstOption = customSelect.querySelector('.custom-option');
        if (firstOption) firstOption.focus();
    }
});

// Cerrar dropdown al hacer clic fuera
document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-select-container')) {
        customSelect.classList.remove('show');
    }
});


// Navegación con teclado
customSelect.addEventListener('keydown', (e) => {
    const options = Array.from(customSelect.querySelectorAll('.custom-option'));
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
                searchInput.focus();
            }
            break;
        case 'Enter':
            e.preventDefault();
            if (document.activeElement.classList.contains('custom-option')) {
                const curso = arrayCursos.find(c => c.id == document.activeElement.dataset.value);
                selectOption(document.activeElement, curso);
            }
            break;
        case 'Escape':
            customSelect.classList.remove('show');
            searchInput.focus();
            break;
    }
});

// Inicializar
filterOptions();