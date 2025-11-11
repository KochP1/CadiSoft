let materias = [];
let materiasEdit = []
let materiasCargar = [];
let count = 0;

const getMaterias = async () => {
    const id = parseInt(document.getElementById('excelMaterias').getAttribute('idCurso'));
    const url = `/inces/materias/${id}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        materias = data.materias;
    } catch(e) {
        console.error(e);
    }
}

const carga_masiva_materias = async (event) => {
    event.preventDefault();
    if (isSearching) return;
    setSearching(true);
    const url = '/inces/carga_masiva_materias';
    const formData = new FormData();
    const archivoInput = document.getElementById('excelMaterias');
    const archivo = archivoInput.files[0];

    // Verificar que se seleccionó un archivo
    if (!archivo) {
        openAlert('Inces', 'Por favor selecciona un archivo Excel');
        setSearching(false);
        return;
    }

    // Verificar que es un archivo Excel
    const extensionesPermitidas = ['.xlsx', '.xls', '.csv'];
    const nombreArchivo = archivo.name.toLowerCase();
    const esExcel = extensionesPermitidas.some(ext => nombreArchivo.endsWith(ext));
    
    if (!esExcel) {
        openAlert('Inces', 'Por favor selecciona un archivo Excel válido (.xlsx, .xls, .csv)');
        setSearching(false);
        return;
    }

    formData.append('excel', archivo);

    await getMaterias();

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        const modal = bootstrap.Modal.getInstance(document.getElementById('excel-modal'));
        modal.hide();
        document.getElementById('excelMaterias').value = '';

        const arrayExcel = data.materias;

        const container = document.getElementById('planEstudioContent');
        container.innerHTML = '';
        arrayExcel.forEach((item) => {
            if (materias.includes(item.materia)) {
                agregar_materia_excel(item);
            } else {
                throw new Error('Algunas materias del excel no coinciden con las del curso');
            }
        });
        materiasCargar = data.materias;
        openAlert('Inces', data.message);

    } catch(e) {
        openAlert('Inces', e.message);
        console.error(e);
    } finally {
        setSearching(false);
    }

}

const agregar_materia_excel = (newMateria) => {
    const container = document.getElementById('planEstudioContent');
    if (newMateria == '') {
        openAlert('Inces', 'Debe llenar el nombre de la materia');
        return;
    }

    count++;
    const comp = `<div class="plan-estudio__card">
                    <span class="plan-estudio-card__border">6</span>
                    <div class="plan-estudio__num">${count}</div>
                    <div class="plan-estudio__materia">
                        <span>${newMateria.materia}</span>
                        <span>${newMateria.inicio} - ${newMateria.final}</span>
                    </div>
                </div>`

    container.innerHTML+= comp;
}

const limpiar = () => {
    console.log('ejecuto')
    const container = document.getElementById('planEstudioContent');
    container.innerHTML = '';
    count = 0;
}

const crear_seccion_inces = async (event) => {
    event.preventDefault();
    if (isSearching) return;
    setSearching(true);
    const id = parseInt(document.getElementById('excelMaterias').getAttribute('idCurso'));
    const url = `/inces/crear_seccion/${id}`;
    const seccion = document.getElementById('crearSeccion').value.trim();
    const profesor = document.getElementById('profesorCrearSeccion').value.trim();
    const aula = document.getElementById('aulaSeccion').value.trim();

    if (!seccion || !profesor || !aula) {
        setSearching(false);
        openAlert('Secciones', `Todos los campos son obligatorios`);
        return;
    }

    if (seccion.length > 10) {
        setSearching(false);
        openAlert('Secciones', `La sección no puede tener más de 10 caracteres`);
        return;
    }

    if (aula.length > 10) {
        setSearching(false);
        openAlert('Secciones', `El aula no puede tener más de 10 caracteres`);
        return;
    }

    if (materiasCargar.length <= 0) {
        setSearching(false);
        openAlert('Secciones', `No hay planes de estudios para las materias`);
        return;
    }

    const requestData = {
        'seccion': seccion,
        'profesor': profesor,
        'aula': aula,
        'materias': materiasCargar
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

        openAlert('Inces', data.message);
    } catch(e) {
        openAlert('Inces', e)
        console.error(e);
    } finally {
        setSearching(false);
    }
}

const getMateriasById = async (id) => {
    const url = `/inces/materias_by_id/${id}`

        try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        return data.materias
    } catch(e) {
        console.error(e)
    }
}

const edit_seccion_inces = async (idSeccion) => {
    if (isSearching) return;
    setSearching(true);
    const url = `/inces/edit_seccion_inces/${idSeccion}`;

    if (materiasCargar.length <= 0) {
        materiasCargar = await getMateriasById(idSeccion);
    };

    console.log(materiasCargar)
    
    
    const requestData = {
        'materias': materiasCargar,
    }

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            openAlert('Secciones', `${data.error}`);
            throw new Error(data.error);
        }

        openAlert('Secciones', `${data.mensaje}`);
        window.location.reload();
    } catch(e) {
        console.error(e)
    } finally {
        setSearching(false);
    }
}