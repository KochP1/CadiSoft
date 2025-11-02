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
    const curso = document.getElementById('').value.trim();

    if (curso === '') {
        openAlert('Inces', 'Debe llenar el nombre del curso');
        setSearching(false);
        return;
    }

    const requestData = {
        curso: curso,
        materias: materias
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: requestData
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

    } catch(e) {
        openAlert('Inces', data.error);
        console.error(e);
    } finally {
        materias = [];
        count = 0;
        limpiar_materias();
        setSearching(false);
    }

}

const agregar_materia = () => {
    const newMateria = document.getElementById('materiaInces').value.trim();
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
    const newMateria = document.getElementById('materiaInces').value.trim();
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
    // Eliminar el elemento padre del div
    div.parentElement.remove();
    
    // Reorganizar los números de las materias
    count = 0;
    const divs = document.querySelectorAll('.numero-materia');
    divs.forEach((item) => {
        count++;
        item.textContent = count;
    })
}

