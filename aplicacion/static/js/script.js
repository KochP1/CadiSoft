let isSearching = false;

function href(url) {
    window.location.href = url;
}

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

// Olvidar contraseña
async function olvidar_contraseña(event) {
    event.preventDefault()
    const url = '/forgot_password';
    const email = document.getElementById('email-olvidar-contraseña').value.trim();
    const formData = new FormData();

    if (!email) {
        alert('Todos los campos son obligatorios')
        return;
    }

    if ( email.length > 50) {
        alert('El email puede tener 50 caracteres máximo');
        return;
    }

    formData.append('email', email);

    try {
        const response = await fetch(url, {
        method: 'POST',
        body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error);
            throw new Error(data.error);
        }

        alert(data.message);
        window.location.href = `/verificacion_dos_pasos/${data.idusuario}`
    } catch (e) {
        console.log(e)
    }

}

async function verificar_codigo(idusuario, event) {
    event.preventDefault();
    const url = `/verificacion_dos_pasos/${idusuario}`
    const codigo = document.getElementById('codigo-olvidar-contraseña').value.trim();
    const formData = new FormData();

    if (!codigo) {
        alert('Debe ingresar el codigo de verificación');
        return;
    }

    
    if (codigo.length > 6) {
        alert('Un código de verificación no puede tener más de 6 digitos');
        return;
    }

    formData.append('codigo', codigo);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            alert('Código de recuperación inválido')
            throw new Error(data.error);
        }

        alert(data.message);
        window.location.href = `/recuperar_contraseña/${data.user}`
    } catch(e) {
        console.log(e)
    }

}

async function recuperar_contraseña(idusuario, event) {
    event.preventDefault();
    const url = `/recuperar_contraseña/${idusuario}`;
    const contraseñaNueva = document.getElementById('recuperar-contraseña').value.trim();
    const contraseaNuevaConfirmar = document.getElementById('recuperar-contraseña-confirmar').value.trim();
    const formData = new FormData();

    if (!contraseaNuevaConfirmar || !contraseñaNueva) {
        alert('Todos los campos son obligatorios');
        return null;
    }

    if(contraseñaNueva !== contraseaNuevaConfirmar) {
        alert('La confirmación de la contraseña no es igual a la nueva contraseña');
        return null;
    }

    if (contraseñaNueva.length > 8 || contraseaNuevaConfirmar.length > 8) {
        alert('La contraseña puede tener máximo 8 caracteres');
        return null;
    }

    formData.append('contraseñaNueva', contraseñaNueva);
    formData.append('contraseaNuevaConfirmar', contraseaNuevaConfirmar);

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        alert(data.message);
        window.location.href = '/';

    } catch(e) {
        console.log(e)
    }

    return false;
}

// Inicio

async function stats() {
    if (isSearching) return;
    isSearching = true;

    const url = '/inicio_stats'

    try{
        const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
        });

        const data = await response.json()

        if (!response.ok) {
            throw new Error(`Error`)
        }

        console.log(data.alumnos)
        mostrar_stats(data)
    } catch (error) {
        console.log(error)
    } finally {
        isSearching = false
    }
}

function interval(elemento, limite) {
    let cantidad = 0;
    const duracion = 1700;
    const incrementos = limite;
    const intervalo = duracion / incrementos;
    
    let tiempo = setInterval(() => {
        elemento.textContent = cantidad;
        cantidad += 1;

        if (cantidad === limite) {
            clearInterval(tiempo);
        }
    }, intervalo);
}

function mostrar_stats(data) {
    const p_profesores = document.getElementById('num-profesores');
    const p_alumnos = document.getElementById('num-alumnos');
    const p_cursos = document.getElementById('num-cursos');
    const p_facultades = document.getElementById('num-facultades');

    const profesores = parseInt(data.profesores);
    const alumnos = parseInt(data.alumnos);
    const cursos = parseInt(data.cursos);
    const facultades = parseInt(data.facultades);

    setTimeout(() => {
        interval(p_profesores, profesores);
        interval(p_alumnos, alumnos);
        interval(p_cursos, cursos);
        interval(p_facultades, facultades);
    }, 200)
}

//stats()

if (window.location.pathname === '/inicio') {
    stats();
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

// Crear registro familiar de alumno

async function crear_registro_familiar(idAlumno, event) {
    event.preventDefault()
    const formData = new FormData();
    const url = `/alumnos/crear_registro_familiar/${idAlumno}`;
    const nombrePapa = document.getElementById('nombrePapa').value.trim();
    const apellidoPapa = document.getElementById('apellidoPapa').value.trim();
    const nombreMama = document.getElementById('nombreMama').value.trim();
    const apellidoMama = document.getElementById('apellidoMama').value.trim();
    const contacto = document.getElementById('contactoFamilia').value.trim();

    if (!nombrePapa || !apellidoMama || !apellidoPapa || !nombreMama || !contacto) {
        alert('Todos los campos son obligatorios');
        return;
    }

    if (nombrePapa.length > 12 || nombreMama.length > 12) {
        alert('Nombres pueden tener maximo 12 caracteres');
        return;
    }

    if (apellidoPapa.length > 20 || apellidoMama.length > 20) {
        alert('Apellidos pueden tener maximo 20 caracteres');
        return;
    }

    formData.append('nombrePapa', nombrePapa);
    formData.append('apellidoPapa', apellidoPapa);
    formData.append('nombreMama', nombreMama);
    formData.append('apellidoMama', apellidoMama);
    formData.append('contacto', contacto);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        alert(data.message);
        window.location.reload();
    } catch(e) {
        console.log(e)
    }
}

async function edit_datos_papa(idFamilia, event) {
    event.preventDefault();
    const url = `/alumnos/edit_registro_fam_papa/${idFamilia}`;
    const NombrePapa = document.getElementById('editNombrePapa').value.trim();
    const ApellidoPapa = document.getElementById('editApellidoPapa').value.trim();
    const formData = new FormData();

    if (!NombrePapa || !ApellidoPapa) {
        alert('Todos los campos son obligatorios');
        return;
    }

    if (NombrePapa.length > 12) {
        alert('Los nombres pueden tener máximo 12 caracteres');
        return;
    }

    if (ApellidoPapa.length > 20) {
        alert('Los apellidos pueden tener máximo 20 caracteres');
        return;
    }

    formData.append('NombrePapa' ,NombrePapa);
    formData.append('ApellidoPapa' ,ApellidoPapa);

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        alert(data.message);
        window.location.reload();
    } catch(e) {
        console.log(e)
    }
}

async function edit_datos_mama(idFamilia, event) {
    event.preventDefault();
    const url = `/alumnos/edit_registro_fam_mama/${idFamilia}`;
    const NombreMama = document.getElementById('editNombreMama').value.trim();
    const ApellidoMama = document.getElementById('editApellidoMama').value.trim();
    const formData = new FormData();

    if (!NombreMama || !ApellidoMama) {
        alert('Todos los campos son obligatorios');
        return;
    }

    if (NombreMama.length > 12) {
        alert('Los nombres pueden tener máximo 12 caracteres');
        return;
    }

    if (ApellidoMama.length > 20) {
        alert('Los apellidos pueden tener máximo 20 caracteres');
        return;
    }

    formData.append('NombreMama' ,NombreMama);
    formData.append('ApellidoMama' ,ApellidoMama);

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        alert(data.message);
        window.location.reload();
    } catch(e) {
        console.log(e)
    }
}

async function edit_datos_contacto(idFamilia, event) {
    event.preventDefault();
    const url = `/alumnos/edit_registro_fam_contacto/${idFamilia}`;
    const contacto = document.getElementById('edit-contacto').value.trim();
    const formData = new FormData();

    if (!contacto) {
        alert('Todos los campos son obligatorios');
        return;
    }

    if (contacto.length > 11) {
        alert('El teléfono puede tener máximo 11 digitos');
        return;
    }

    formData.append('contacto', contacto)

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        alert(data.message);
        window.location.reload();
    } catch(e) {
        console.log(e)
    }
}

async function eliminar_registro_familiar(idRegistro) {
    const url = `/alumnos/eliminar_registro_familiar/${idRegistro}`;

    if(confirm('Estas seguro de que quieres eliminar el registro familiar?')) {
        try {
            const response = await fetch(url, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error);
            }

            alert(data.message);
            window.location.reload();
        } catch (e) {
            console.log(e)
        }
    }
}

// INSCRIPCIONES

// Buscar alumno por cédula
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

    if (!periodoInicio || !periodoFinal) {
        alert('Debes ingresar el periodo de inscripción')
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

function crearAlumno() {
    const form = document.getElementById('crear-alumno-form');
    const rol = 'alumno'
    const nombre = document.getElementById('nombreAlumno').value;
    const segundoNombre = document.getElementById('segundoNombreAlumno').value;
    const apellido = document.getElementById('apellidoAlumno').value;
    const segundoApellido = document.getElementById('segundoApellidoAlumno').value;
    const cedula = document.getElementById('cedulaAlumno').value;
    const email = document.getElementById('emailAlumno').value;
    const contraseña = document.getElementById('contraseñaAlumno').value;
    const imagen = document.getElementById('imagenAlumno').files[0];


    if (nombre === '' || segundoNombre === '' || apellido === '' || segundoApellido === '' || cedula === '' || email === '' || contraseña === '') {
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
        formData.append('imagen', imagen);

        if (cedula.length > 8) {
            alert('La cédula puede tener máximo 8 caracteres');
            window.location.reload();
        }

        try {
            const response = await fetch('/inscripciones/alumnos_regulares', {
                method: 'POST',
                body: formData
            });
    
            if (response.ok) {
                alert('Alumno creado satisfactoriamente')
                window.location.reload();
            } else {
                alert('Error al crear el alumno')
            }
        } catch (error) {
            console.log(error)
        }
    })
}

// CURSOS

async function get_facultades() {
    const url = '/cursos/buscar_facultades';

    if (isSearching) return;
    isSearching = true;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        select_facultades(data.facultades);

    } catch (e) {
        console.log(e);
    } finally {
        isSearching = false;
    }
}

function select_facultades(data) {
    const select = document.getElementById('facultad-curso');

    if (select && data) {
        data.forEach((element) => {
            const option = document.createElement('option');
            option.classList.add('form-control')
            option.classList.add('mb-3')
            option.value = element.idFacultad;
            option.textContent = element.facultad;
            
            select.appendChild(option)
        })
    }
}

async function crear_curso(event) {
    event.preventDefault();

    console.log('me ejecuto')

    const url = '/cursos/';
    const facultad = document.getElementById('facultad-curso').value;
    const nombre_curso = document.getElementById('curso').value.trim();

    if (!facultad || !nombre_curso) {
        alert('Todos los campos son obligatorios');
        return;
    }

    if (nombre_curso.length > 40) {
        alert('El nombre del curso puede tener 40 caracteres máximo');
        return;
    }

    console.log('me ejecuto')
    const formData = new FormData();

    formData.append('idFacultad', facultad);
    formData.append('nombre_curso', nombre_curso);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        console.log('me ejecuto')
        const data = await response.json();

        if(!response.ok) {
            alert('ERROR')
            throw new Error(data.error);
        }

        alert(data.message);
    } catch (e) {
        console.log(e)
    }
}

async function elim_curso(idcurso) {
    const url = `/cursos/eliminar_curso/${idcurso}`;

    if (isSearching) return;
    isSearching = true;

    if (idcurso) {
        try {
            const response = await fetch(url, {
                method: 'DELETE'
            });

            const data = response.json();

            if (!response.ok) {
                throw new Error(`Error: ${data.error}`)
            }

            alert('Curso eliminado satisfactoriamente')
            window.location.reload();
        } catch (e) {
            console.log(e)
        } finally {
            isSearching = false
        }
    }

}

// FRONT END 

function get_id_alumno(idAlumno) {
    const form = document.getElementById('crear-registro-familiar-form');

    form.setAttribute('idAlumno', idAlumno)
}

function mostrar_contraseña(contraseña) {
    const inputContraseña = document.getElementById(contraseña);
    const contraseñaIcono = document.querySelector(`[id-input="${contraseña}"]`);

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
    const createdOptions = document.querySelectorAll('.seccion-option');
    btn.style.display = 'flex';

    if (createdOptions.length > 0) {
        limpiar_horario();
        createdOptions.forEach(element => {
            element.remove();
        })
    }

    if (select && data) {
        select.style.display = 'block';
        data.forEach(curso => {
            let option = document.createElement('option')
            option.classList.add('seccion-option')
            option.value = curso.idSeccion;
            option.text = curso.seccion;
            select.appendChild(option);
        });
        
    } else {
        alert('Error al mostrar secciones')
    }
}

function mostrar_horario(data) {
    document.getElementById('horario__container').style.display = 'block';
    limpiar_horario();
    
    if (!data || !data.length) return;

    const dias = {
        'Lunes': 1,
        'Martes': 2,
        'Miércoles': 3,
        'Jueves': 4,
        'Viernes': 5,
        'Sábado': 6
    };

    const horas = {
        '08:00:00': 1,  // 8:00-9:00 am
        '09:00:00': 2,  // 9:00-10:00 am
        '10:00:00': 3,  // 10:00-11:00 am
        '11:00:00': 4,  // 11:00-12:00 am
        '12:00:00': 5,  // 12:00-01:00 pm
        '13:00:00': 6,  // 01:00-02:00 pm
        '14:00:00': 7,  // 02:00-03:00 pm
        '15:00:00': 8,  // 03:00-04:00 pm
        '16:00:00': 9   // 04:00-05:00 pm
    };

    data.forEach(element => {
        const dia = element.horario_dia;
        const horaInicio = element.horario_hora;
        const horaFin = element.horario_hora_final;
        
        const columna = dias[dia];
        const filaInicio = horas[horaInicio];
        const filaFin = horas[horaFin];
        
        if (columna && filaInicio) {
            const duracion = filaFin ? (filaFin - filaInicio + 1) : 1;
            
            const tabla = document.getElementById('tabla-horario');
            
            const fila = tabla.rows[filaInicio];
            
            if (fila && fila.cells[columna]) {
                const celda = fila.cells[columna];
                celda.textContent = element.nombre_curso;
                celda.style.backgroundColor = getRandomColor();
                
                if (duracion > 1) {
                    celda.rowSpan = duracion;
                    
                    for (let i = 1; i < duracion; i++) {
                        const siguienteFila = tabla.rows[filaInicio + i];
                        if (siguienteFila && siguienteFila.cells[columna]) {
                            siguienteFila.cells[columna].style.display = 'none';
                        }
                    }
                }
            }
        }
    });
}

function limpiar_horario() {
    const tabla = document.getElementById('tabla-horario');
    
    for (let i = 1; i < tabla.rows.length; i++) {
        for (let j = 1; j < tabla.rows[i].cells.length; j++) {
            const celda = tabla.rows[i].cells[j];
            celda.textContent = '';
            celda.style.backgroundColor = '';
            celda.style.display = '';
            celda.removeAttribute('rowSpan');
        }
    }
}


function getRandomColor() {
    const colors = ['#FFD700', '#98FB98', '#ADD8E6', '#FFB6C1', '#E6E6FA', '#FFA07A', '#90EE90', '#87CEFA', '#FFC0CB'];
    return colors[Math.floor(Math.random() * colors.length)];
}
