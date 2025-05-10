// Cierre de sesion
async function log_out() {
    const response = await fetch('/log_out', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (response.ok) {
        window.location.href = '/'
    }
    else{
        alert('Error al cerrar sesión')
    }
}

// Profesores

function crearProfesor() {
    const form = document.getElementById('crear-profesor-form');
    const rol = 'profesor'
    const nombre = document.getElementById('nombreProfesor').value;
    const segundoNombre = document.getElementById('segundoNombreProfesor').value;
    const apellido = document.getElementById('apellidoProfesor').value;
    const segundoApellido = document.getElementById('segundoApellidoProfesor').value;
    const cedula = document.getElementById('cedulaProfesor').value;
    const email = document.getElementById('emailProfesor').value;
    const contraseña = document.getElementById('contraseñaProfesor').value;
    const especialidad = document.getElementById('especialidadProfesor').value;
    const imagen = document.getElementById('imagenProfesor').files[0];


    if (nombre === '' || segundoNombre === '' || apellido === '' || segundoApellido === '' || cedula === '' || email === '' || contraseña === '' || especialidad === '') {
        alert('Todos los campos deben ser llenados')
        window.location.reload()
    }

    
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('nombre', nombre);
        formData.append('segundoNombre', segundoNombre);
        formData.append('apellido', apellido);
        formData.append('segundoApellido', segundoApellido);
        formData.append('cedula', cedula);
        formData.append('email', email);
        formData.append('contraseña', contraseña);
        formData.append('rol', rol);
        formData.append('especialidad', especialidad);
        formData.append('imagen', imagen);

        if (cedula.length > 8) {
            alert('La cédula puede tener máximo 8 caracteres');
            window.location.reload();
        }

        try {
            console.log('ey')
            const response = await fetch('/profesores/', {
                method: 'POST',
                body: formData
            });
    
            if (response.ok) {
                alert('Profesor creado satisfactoriamente')
                window.location.href = '/profesores/'
            } else {
                alert('Error al crear el usuario')
            }
        } catch (error) {
            console.log(error)
        }
    })
}

// Eliminar profesor
async function eliminar_profesor(idusuarios) {
    if (confirm('Estas seguro de que quieres eliminar el profesor?')) {
        const response = await fetch(`/profesores/eliminar_profesor/${idusuarios}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
        });
    
        if (response.ok) {
            alert('Profesor eliminado satisfactoriamente');
            window.location.reload();
        } else {
            alert('Error al eliminar el profesor');
        }
    }
}

// Usuarios

function update_foto(idusuarios) {
    const form = document.getElementById('updateFoto');
    const imagen = document.getElementById('fotoPerfil').files[0];

    if (!imagen) {
        alert('Por favor, seleccione una imagen');
        return;
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData();

        formData.append('imagen', imagen);

        try {
            const response = await fetch(`/update_foto/${idusuarios}`, {
                method: 'PATCH',
                body: formData,
            });

            if (response.ok) {
                alert('Imágen actualizada satisfactoriamente');
                window.location.reload();
            } else {
                alert('La imágen no pudo ser actualizada');
            }
        } catch (error) {
            console.error('Error:', error);
        }


    });
}

async function edit_email(idusuarios) {
    const email = document.getElementById('edit-email').value;

    if(!email) {
        alert('Debe ingresar el correo electrónico')
        return;
    }

    try {
        const response = await fetch(`/update_email/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'email': email})
        });
    
        if (response.ok) {
            alert('Email actualizado satisfactoriamente');
            window.location.reload();
        } else {
            alert('Error al actualizar el email');
        }
    } catch (e) {
        console.log(`Error: ${e}`);
    }
}

async function edit_nombres(idusuarios) {
    const nombre = document.getElementById('editNombre').value;
    const segundoNombre = document.getElementById('editSegundoNombre').value;

    if (!nombre || !segundoNombre) {
        alert('Debe llenar todos los campos');
        return;
    }

    try{
        const response = await fetch(`/edit_nombres/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'nombre': nombre, 'segundoNombre': segundoNombre})
        });
    
        if (response.ok) {
            alert('Nombres actualizados satisfactoriamente')
            window.location.reload();
        } else {
            alert('Error actualizando nombres')
        }
    } catch (e) {
        console.log(`Error: ${e}`)
    }
}

async function edit_apellidos(idusuarios) {
    const apellido = document.getElementById('editApellido').value;
    const segundoApellido = document.getElementById('editSegundoApellido').value;

    if (!apellido || !segundoApellido) {
        alert('Debe llenar todos los campos');
        return;
    }

    try{
        const response = await fetch(`/edit_apellidos/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'apellido': apellido, 'segundoApellido': segundoApellido})
        });
    
        if (response.ok) {
            alert('Apellidos actualizados satisfactoriamente')
            window.location.reload();
        } else {
            alert('Error actualizando apellidos')
        }
    } catch (e) {
        console.log(`Error: ${e}`)
    }
}

async function edit_cedula(idusuarios) {
    const cedula = document.getElementById('edit-cedula').value;

    if(!cedula) {
        alert('Debe ingresar la cédula')
        return;
    }

    if (cedula.length > 8) {
        alert('La cédula puede tener máximo 8 caracteres')
        return;
    }

    try {
        const response = await fetch(`/edit_cedula/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'cedula': cedula})
        });
    
        if (response.ok) {
            alert('cedula actualizada satisfactoriamente');
            window.location.reload();
        } else {
            alert('Error al actualizar la cedula');
        }
    } catch (e) {
        console.log(`Error: ${e}`);
    }
}

async function edit_contraseña(idusuarios) {
    const contraseñaActual = document.getElementById('edit-contraseña').value;
    const contraseaNueva = document.getElementById('contraseña-nueva').value;

    if (contraseaNueva.length > 8 || contraseñaActual.length > 8) {
        alert('La contraseña puede tener 8 caracteres máximo')
        return;
    }

    
    try {
        const response = await fetch(`/edit_contraseña/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'contraseñaActual': contraseñaActual, 'contraseñaNueva': contraseaNueva})
        });
    
        if (response.ok) {
            alert('La contraseña fue actualizada satisfactoriamente');
            log_out();
        } else{
            alert('La contraseña actual es incorrecta');
        }
    } catch(e) {
        console.log(`Error: ${e}`);
    }
}

// Facultad

function crearFacultad() {
    const form = document.getElementById('crear-facultad-form');
    const nombreFacultad = document.getElementById('nombreFacultad').value;

    if (nombreFacultad === '') {
        alert('Debe introducir el nombre de la facultad')
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData;

        formData.append('nombreFacultad', nombreFacultad)

        try {
            const response = await fetch('/facultades/', {
                method: 'POST',
                body: formData
            })
    
            if (response.ok) {
                alert('Facultad creada satisfactoriamente');
                window.location.reload();
            } else{
                alert('Error al crear la facultad')
            }
        } catch(e) {
            console.log(e)
        }
    })
}

function obtener_campos_facultad(idfacultad) {
    const editNombreFacultad = document.getElementById('edit-nombreFacultad');
    const nombreFacultad = document.getElementById(`nombre-facultad-${idfacultad}`).textContent;
    const btnModalEditFacultad = document.getElementById('btn-edit-facultad')

    btnModalEditFacultad.setAttribute('idfacultad', idfacultad)

    editNombreFacultad.value = nombreFacultad
}

function editar_facultad(idfacultad) {
    const form = document.getElementById('edit-facultad-form');
    const nombreFacultad = document.getElementById('edit-nombreFacultad').value;

    if (nombreFacultad === '') {
        alert('Debe introducir el nombre de la facultad')
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData;

        formData.append('nombreFacultad', nombreFacultad)

        try {
            const response = await fetch(`/facultades/edit_facultad/${idfacultad}`, {
                method: 'PATCH',
                body: formData
            })
    
            if (response.ok) {
                alert('Facultad actualizada satisfactoriamente');
                window.location.href = '/facultades/';
            } else{
                alert('Error al actualizar la facultad')
            }
        } catch(e) {
            console.log(e)
        }
    })
}

async function elim_facultad(idfacultad) {

    if(confirm('¿Estas seguro de quieres eliminar esta facultad?')) {
        try {
            const response = await fetch(`/facultades/edit_facultad/${idfacultad}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
    
            if (response.ok) {
                alert('Facultad eliminada satisfactoriamente')
                window.location.href = '/facultades/'
            } else {
                alert('Error al eliminar facultad')
            }
        } catch (e) {
            console.log(`Error: ${e}`)
        }
    }
}

// Alumnos

// Eliminar alumno

async function eliminar_usuario(idusuarios) {
    if (confirm('Estas seguro de que quieres eliminar el alumno')) {
        
        try {
            const response = await fetch(`/alumnos/eliminar_alumno/${idusuarios}`, {
                method: 'DELETE'
            });
    
            if (response.ok) {
                alert('El alumno ha sido eliminado satisfactoriamente');
                window.location.reload();
            } else {
                alert('Error al eliminar al alumno');
            }
        } catch(e) {
            console.log(`Error: ${e}`);
        }
    }
}

// INSCRIPCIONES

// Buscar alumno por cédula
let isSearching = false;
function buscar_alumno() {
    const form = document.getElementById('buscar-alumno-inscripcion')
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (isSearching) return;
        isSearching = true;

        const formData = new FormData;
        const cedula = document.getElementById('inscripcion-buscar-cedula').value
        const url = '/inscripciones/buscar_alumno'

        formData.append('cedula', cedula)

        if (!cedula) {
            alert('Por favor ingrese una cédula');
            isSearching = false;
            return;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                alert('El alumno no existe')
                throw new Error('Hubo un error buscando al alumno')
            }

            let data = await response.json()
            mostrar_panel_inscripcion(data.alumno)

        } catch(e) {
            console.log(e)
        } finally {
            isSearching = false;
        }
    })
}

async function buscar_curso() {
    if (isSearching) return;
    isSearching = true;
    const curso = document.getElementById('curso-inscripcion').value;
    const url = '/inscripciones/buscar_curso';

    console.log(curso)

    if (!curso) {
        isSearching = false;
        return;
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'curso': curso})
        });

        if (!response.ok) {
            alert('Curso no encontrado')
            throw new Error ('Error al buscar el curso');
        }

        const data = await response.json()
        seleccionar_seccion(data.cursos)
    } catch (e) {
        console.log(e);
    } finally {
        isSearching = false
    }
}

async function buscar_horario() {
    if (isSearching) return;
    isSearching = true;
    const idSeccion = document.getElementById('select-seccion-inscripcion').value;
    const url = '/inscripciones/mostar_horario';

    if (!idSeccion || idSeccion === 'Selecciona una Sección') {
        isSearching = false;
        return;
    }
    
    try {
        const response = await fetch(url ,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'idSeccion': idSeccion})
            }
        )


        if (!response.ok) {
            throw new Error('Error al buscar el horario de la sección');
        }

        const data = await response.json();

        mostrar_horario(data.horarioSeccion)
    } catch(e) {
        console.log(e)
    } finally {
        isSearching = false
    }
}

function inscribir_alumno() {
    const form = document.getElementById('inscripcion-form');
    const idAlumno = document.getElementById('alumno-id-inscripcion').value;
    const periodoInicio = document.getElementById('InicioPeriodo').value;
    const periodoFinal = document.getElementById('FinPeriodo').value;
    const idSeccion = document.getElementById('select-seccion-inscripcion').value;

    if (!form) {
        return;
    }

    

    form.addEventListener('submit', async(event) => {
        event.preventDefault();
        if (isSearching) return;
        isSearching = true;

        const formData = new FormData();
        const url = '/inscripciones/inscribir_alumno';

        

        formData.append('idAlumno' ,idAlumno);
        formData.append('periodoInicio',periodoInicio);
        formData.append('periodoFinal', periodoFinal);
        formData.append('idSeccion', idSeccion);

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            })

            const data = await response.json();

            if (!response.ok) {
                throw new Error('Error al inscribir el alumno');
            }
            alert(data.mensaje);
            window.location.reload();
        } catch (e) {
            console.log(e)
        } finally {
            isSearching = false;
        }
    })
}

// FRONT END 

function mostrar_contraseña(contraseña) {
    const inputContraseña = document.getElementById(contraseña);
    const contraseñaIcono = document.getElementById('contraseña-icon');

    if (!inputContraseña || !contraseñaIcono) {
        return;
    }

    if (inputContraseña.type === 'password') {
        inputContraseña.type = 'text'
        contraseñaIcono.classList.remove('fa-eye-slash')
        contraseñaIcono.classList.add('fa-eye')
    } else {
        inputContraseña.type = 'password'
        contraseñaIcono.classList.add('fa-eye-slash')
        contraseñaIcono.classList.remove('fa-eye')
    }
}

function mostrar_panel_inscripcion(data) {
    const container = document.getElementById('inscripcion-options__container');
    let nombre = document.getElementById('alumno-nombre-inscripcion');
    let apellido = document.getElementById('alumno-apellido-inscripcion');
    let cedula = document.getElementById('alumno-cedula-inscripcion');
    let id = document.getElementById('alumno-id-inscripcion');
    let imagen = document.getElementById('img-alumno-inscripcion');
    const idusuario = data.idusuarios;


    try {
        nombre.value = data.nombre;
        apellido.value = data.apellido;
        cedula.value = data.cedula;
        id.value = data.idAlumno;
        imagen.src = `/get_profile_image/${idusuario}`
        container.style.display = 'flex';
    } catch(e) {
        console.log(e)
    }
}

function seleccionar_seccion(data) {
    const select = document.getElementById('select-seccion-inscripcion');
    const btn = document.getElementById('btn-inscribir');
    btn.style.display = 'flex';

    if (select && data) {
        select.style.display = 'block';
        data.forEach(curso => {
            let option = document.createElement('option')
            option.value = curso.idSeccion;
            option.text = curso.seccion;
            select.appendChild(option);
        });
        
    } else {
        alert('Error al mostrar secciones')
    }
}

function mostrar_horario(data) {
    const tabla = document.getElementById('tbody-horario');
    const tablaContainer = document.getElementById('horario__container');
    
    tabla.innerHTML = '';

    if (tabla && data) {
        // Mapeo entre días y sus IDs en la tabla
        const diasMap = {
            'Lunes': 'lunes',
            'Martes': 'martes',
            'Miércoles': 'miercoles',
            'Jueves': 'jueves',
            'Viernes': 'viernes',
            'Sábado': 'sabado'
        };

        data.forEach(horario => {
            const horaInicio = new Date(`2000-01-01T${horario.horario_hora}`);
            const horaFin = new Date(`2000-01-01T${horario.horario_hora_final}`);
            
            let horaActual = horaInicio;
            while (horaActual < horaFin) {
                const horaSiguiente = new Date(horaActual.getTime() + 60 * 60 * 1000); // +1 hora
                if (horaSiguiente > horaFin) horaSiguiente = horaFin;

                const horaFormateada = `${horaActual.getHours()}:${horaActual.getMinutes().toString().padStart(2, '0')}`;
                const horaSiguienteFormateada = `${horaSiguiente.getHours()}:${horaSiguiente.getMinutes().toString().padStart(2, '0')}`;

                let tbody = `
                    <tr>
                        <td id="hora">${horaFormateada}-${horaSiguienteFormateada}</td>
                        ${Object.entries(diasMap).map(([dia, id]) => `
                            <td id="${id}">${horario.horario_dia === dia ? `
                                <p>${horario.nombre_curso} <br> Aula: ${horario.horario_aula}</p>
                            ` : ''}</td>
                        `).join('')}
                    </tr>
                `;

                tabla.innerHTML += tbody;
                horaActual = horaSiguiente;
            }
        });

        tablaContainer.style.display = 'block';
    }
}
