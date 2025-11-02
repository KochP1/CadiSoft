// VARIABLES GLOBALES
let materias = [];
let count = 0;
console.log(materias);
console.log(count);


const crear_curso_inces = async (event) => {
    event.preventDefault();
    if (isSearching) return;
    setSearching(true);
    const url = '/inces/crear_curso';
    const curso = document.getElementById('cursoinces').value.trim();
    const facultad = parseInt(document.getElementById('selectedValue').value);
    const imagen = null;
    const duracion = document.getElementById('duracionInces').value;

    if (curso === '') {
        openAlert('Inces', 'Debe llenar el nombre del curso');
        setSearching(false);
        return;
    }

    if (curso.length > 30) {
        openAlert('Inces', 'El curso puede tener máximo 30 caracteres');
        setSearching(false);
        return;
    }

    if (facultad < 0) {
        openAlert('Inces', 'Seleccione una facultad');
        setSearching(false);
        return;
    }

    if (duracion <= 0) {
        openAlert('Inces', 'Ingrese una duracion para el curso');
        setSearching(false);
        return;
    }

    if (materias.length == 0) {
        openAlert('Inces', 'Debe crear al menos una materia para el curso');
        setSearching(false);
        return;
    }

    const requestData = {
        curso: curso,
        facultad: facultad,
        imagen: imagen,
        duracion: duracion,
        materias: materias
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

    } catch(e) {
        openAlert('Inces', e);
        console.error(e);
    } finally {
        materias = [];
        count = 0;
        limpiar_materias();
        setSearching(false);
    }

}

const agregar_materia = () => {
    let newMateria = document.getElementById('materiaInces').value.trim();
    const noMaterias = document.getElementById('sin-materias__container');
    const materiasContainer = document.getElementById('materias-list__container');
    const ul = document.getElementById('materias-ul');

    console.log(newMateria);

    if (newMateria == '') {
        openAlert('Inces', 'Debe llenar el nombre de la materia');
        return;
    }

    count++;
    noMaterias.style.display = 'none';
    materiasContainer.style.display = 'flex';

    const li = document.createElement('li');
    const divNum = document.createElement('div');
    const span = document.createElement('span');

    divNum.classList.add('numero-materia');
    divNum.textContent = count;
    divNum.addEventListener('click', function() {
        elim_materia(this);
    });

    span.innerHTML = newMateria;

    li.appendChild(divNum);
    li.appendChild(span)
    ul.appendChild(li);

    materias.push(newMateria);
    newMateria = '';
    console.log(materias);
    console.log(count);
}

const limpiar_materias = () => {
    let newMateria = document.getElementById('materiaInces').value.trim();
    const ul = document.getElementById('materias-ul');
    const noMaterias = document.getElementById('sin-materias__container');
    const materiasContainer = document.getElementById('materias-list__container');
    ul.innerHTML = '';
    materiasContainer.style.display = 'none';
    noMaterias.style.display = 'flex';
    materias = [];
    count = 0;
    newMateria = '';
    console.log(materias);
    console.log(count);
}

const elim_materia = (div) => {
    const span = div.nextElementSibling;
    // Eliminar el elemento padre del div
    div.parentElement.remove();
    
    // Reorganizar los números de las materias
    count = 0;
    const divs = document.querySelectorAll('.numero-materia');
    divs.forEach((item) => {
        count++;
        item.textContent = count;
    })

    if (span) {
        materias = materias.filter(x => x !== span.textContent.trim());
        console.log(materias);
    }
}

