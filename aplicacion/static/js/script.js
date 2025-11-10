let isSearching = false;
let resolveConfirm = null;

function isLoading() {
    const loader = document.getElementById('loader');
    if (isSearching) {
        loader.style.display = 'flex';
    } else if (!isSearching) {
        setTimeout(() => {
            loader.style.display = 'none';
        }, 1000);
    }
}

function setSearching(value) {
    isSearching = value;
    isLoading();
}

function href(url) {
    window.location.href = url;
}

function openAlert(title, text) {
    const modal = new bootstrap.Modal(document.getElementById('dialog-alert'));
    document.getElementById('alert-title').textContent = title;
    document.getElementById('alert-content').textContent = text;
    setTimeout(() => {
        modal.show();
    }, 1100)
}


function openConfirm(title, text) {
    return new Promise((resolve) => {
        resolveConfirm = resolve;
        
        const modal = new bootstrap.Modal(document.getElementById('dialog-confirm'));
        document.getElementById('confirm-title').textContent = title;
        document.getElementById('confirm-content').textContent = text;
        modal.show();
    });
}

// Función para cuando el usuario acepta
function confirmAccept() {
    if (resolveConfirm) {
        resolveConfirm(true);
        resolveConfirm = null;
    }
    
    // Pequeño delay para asegurar que Bootstrap ha procesado el modal
    setTimeout(() => {
        const modal = bootstrap.Modal.getInstance(document.getElementById('dialog-alert'));
        if (modal) {
            modal.hide();
        }
    }, 10);
}

// Función para cuando el usuario cancela
function confirmCancel() {
    if (resolveConfirm) {
        resolveConfirm(false);
        resolveConfirm = null;
    }
    const modal = bootstrap.Modal.getInstance(document.getElementById('dialog-alert'));
    modal.hide();
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

// Registrar usuario

async function regist_user(event) {
    if (isSearching) return;
    setSearching(true);
    event.preventDefault()
    const url = '/regist_user';
    const formData = new FormData();

    // Campos
    const nombre = document.getElementById('name').value;
    const segundoNombre = document.getElementById('surname').value;
    const apellido = document.getElementById('lastname').value;
    const segundoApellido = document.getElementById('second_lastname').value;
    const cedula = document.getElementById('cedula').value;
    const email = document.getElementById('email').value;
    const contraseña = document.getElementById('contraseña').value;

    if (!nombre) {
        setSearching(false);
        openAlert('Crear usuario', 'El campo nombre esta vacio');
        return;
    }

    if (!apellido) {
        setSearching(false);
        openAlert('Crear usuario', 'El campo apellido esta vacio');
        return;
    }

    if (!segundoApellido) {
        alert('El campo segundo apellido esta vacio')
        setSearching(false);
        return;
    }

    if (!cedula) {
        setSearching(false);
        openAlert('Crear usuario', 'El campo cedula esta vacio');
        return;
    }

    if (!email) {
        setSearching(false);
        openAlert('Crear usuario', 'El campo email esta vacio');
        return;
    }

    if (!contraseña) {
        setSearching(false);
        openAlert('Crear usuario', 'El campo contraseña esta vacio');
        return;
    }

    if (cedula.length > 8) {
        setSearching(false);
        openAlert('Crear usuario', 'El campo cedula esta vacio');
        return;
    }

    if (contraseña.length > 8) {
        setSearching(false);
        openAlert('Crear usuario', 'La contraseña puede tener máximo 8 caracteres');
        return;
    }

    if (nombre.length > 12 || segundoNombre.length > 12) {
        setSearching(false);
        openAlert('Crear usuario', 'Los nobres pueden tener máximo 12 caracteres');
        return;
    }

    if (apellido.length > 20 || segundoApellido.length > 20) {
        setSearching(false);
        openAlert('Crear usuario', 'Los apellidos pueden tener máximo 20 caracteres');
        return;
    }

    if (email.length > 50) {
        setSearching(false);
        openAlert('Crear usuario', 'El email puede tener un máximo de 50 caracteres')
        return;
    }

    try {
        formData.append('nombre', nombre);
        formData.append('segundoNombre', segundoNombre);
        formData.append('apellido', apellido);
        formData.append('segundoApellido', segundoApellido);
        formData.append('cedula', cedula);
        formData.append('email', email);
        formData.append('contraseña', contraseña);

        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (!response.ok) {
            openAlert('Crear usuario', `${data.error}`);
            throw new Error(data.error);
        }

        openAlert('Crear usuario', 'El usuario fue creado satisfactoriamente')
        window.location.href = '/';
    } catch(e) {
        console.error(e);
    } finally {
        setSearching(false);
    }
}

// Olvidar contraseña
async function olvidar_contraseña(event) {
    if (isSearching) return;
    setSearching(true);
    event.preventDefault()
    const url = '/forgot_password';
    const email = document.getElementById('email-olvidar-contraseña').value.trim();
    const formData = new FormData();

    if (!email) {
        setSearching(false);
        openAlert('Recuperar cuenta', 'Debes ingresar un email')
        return;
    }

    if ( email.length > 50) {
        setSearching(false);
        openAlert('Recuperar cuenta', 'El email puede tener 50 caracteres máximo')
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
            openAlert('Recuperar cuenta', `${data.error}`)
            throw new Error(data.error);
        }

        openAlert('Recuperar cuenta', `${data.message}`)
        window.location.href = `/verificacion_dos_pasos/${data.idusuario}`
    } catch (e) {
        console.log(e)
    } finally {
        setSearching(false);
    }

}

async function verificar_codigo(idusuario, event) {
    if (isSearching) return;
    setSearching(true);
    event.preventDefault();
    const url = `/verificacion_dos_pasos/${idusuario}`
    const codigo = document.getElementById('codigo-olvidar-contraseña').value.trim();
    const formData = new FormData();

    if (!codigo) {
        setSearching(false);
        openAlert('Recuperar cuenta', 'Debe ingresar el codigo de verificación')
        return;
    }

    
    if (codigo.length > 6) {
        setSearching(false);
        openAlert('Recuperar cuenta', 'Un código de verificación no puede tener más de 6 digitos')
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
            openAlert('Recuperar cuenta', 'Código de recuperación invalido')
            throw new Error(data.error);
        }

        openAlert('Recuperar cuenta', `${data.message}`)
        window.location.href = `/recuperar_contraseña/${data.user}`
    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }

}

async function recuperar_contraseña(idusuario, event) {
    if (isSearching) return;
    setSearching(true);
    event.preventDefault();
    const url = `/recuperar_contraseña/${idusuario}`;
    const contraseñaNueva = document.getElementById('recuperar-contraseña').value.trim();
    const contraseaNuevaConfirmar = document.getElementById('recuperar-contraseña-confirmar').value.trim();
    const formData = new FormData();

    if (!contraseaNuevaConfirmar || !contraseñaNueva) {
        setSearching(false);
        openAlert('Recuperar cuenta', 'Debe ingresar una contraseña')
        return null;
    }

    if(contraseñaNueva !== contraseaNuevaConfirmar) {
        setSearching(false);
        openAlert('Recuperar cuenta', 'Las contraseñas no coinciden')
        return null;
    }

    if (contraseñaNueva.length > 8 || contraseaNuevaConfirmar.length > 8) {
        setSearching(false);
        openAlert('Recuperar cuenta', 'La contraseña puede tener máximo 8 caracteres')
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
            openAlert('Recuperar cuenta', 'Error al actualizar contraseña')
            throw new Error(data.error);
        }

        openAlert('Recuperar cuenta', `${data.message}`)
        window.location.href = '/';

    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }

    return false;
}
// Inicio

async function stats() {
    if (isSearching) return;
    setSearching(true);

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

        mostrar_stats(data)
        inicializarGrafico(data);
    } catch (error) {
        console.log(error)
    } finally {
        setSearching(false);
    }
}

function interval(elemento, limite) {
    if (limite === 0) {
        return;
    }

    let cantidad = 0;
    const duracion = 1700;
    const incrementos = limite;
    const intervalo = duracion / incrementos;
    
    let tiempo = setInterval(() => {
        cantidad += 1;
        elemento.textContent = cantidad;

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

async function inicializarGrafico(datos) {
    
    if (!datos) {
        const datosEjemplo = {
            meses: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            inscripciones: [15, 22, 18, 25, 30, 28, 35, 40, 32, 27, 20, 18]
        };
        crearGrafico(datosEjemplo);
        return;
    }

    crearGrafico(datos);
}

function crearGrafico(datos) {
    const ctx = document.getElementById('inscripcionesChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: datos.meses,
            datasets: [{
                label: 'Número de Inscripciones',
                data: datos.inscripciones,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Inscripciones Mensuales - ${new Date().getFullYear()}`,
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Cantidad de Inscripciones'
                    },
                    ticks: {
                        stepSize: 5
                    },
                    font: {
                            size: 12 // ← Números del eje Y más grandes
                        }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Meses del Año'
                    },
                    font: {
                            size: 14 // ← Eje X más grande
                        }
                }
            }
        }
    });
}

//stats()

if (window.location.pathname === '/inicio') {
    stats();
}
// Profesores

async function crearProfesor(event) {
    event.preventDefault();
    const rol = 'profesor'
    const nombre = document.getElementById('nombreProfesor').value.trim();
    const segundoNombre = document.getElementById('segundoNombreProfesor').value.trim();
    const apellido = document.getElementById('apellidoProfesor').value.trim();
    const segundoApellido = document.getElementById('segundoApellidoProfesor').value.trim();
    const cedula = document.getElementById('cedulaProfesor').value.trim();
    const email = document.getElementById('emailProfesor').value.trim();
    const contraseña = document.getElementById('contraseñaProfesor').value.trim();
    const especialidad = document.getElementById('especialidadProfesor').value.trim();
    const imagen = document.getElementById('imagenProfesor').files[0];


    if (especialidad === '') {
        setSearching(false);
        openAlert('Crear profesor', 'El campo especialidad esta vacio');
        return;
    }

    if (!nombre) {
        setSearching(false);
        openAlert('Crear profesor', 'El campo nombre esta vacio');
        return;
    }

    if (!apellido) {
        setSearching(false);
        openAlert('Crear profesor', 'El campo apellido esta vacio');
        return;
    }

    if (!cedula) {
        setSearching(false);
        openAlert('Crear profesor', 'El campo cedula esta vacio');
        return;
    }

    if (!email) {
        setSearching(false);
        openAlert('Crear profesor', 'El campo email esta vacio');
        return;
    }

    if (!contraseña) {
        setSearching(false);
        openAlert('Crear profesor', 'El campo contraseña esta vacio');
        return;
    }

    if (cedula.length > 8) {
        setSearching(false);
        openAlert('Crear profesor', 'El campo cedula esta vacio');
        return;
    }

    if (contraseña.length > 8) {
        setSearching(false);
        openAlert('Crear profesor', 'La contraseña puede tener máximo 8 caracteres');
        return;
    }

    if (nombre.length > 12 || segundoNombre.length > 12) {
        setSearching(false);
        openAlert('Crear profesor', 'Los nobres pueden tener máximo 12 caracteres');
        return;
    }

    if (apellido.length > 20 || segundoApellido.length > 20) {
        setSearching(false);
        openAlert('Crear profesor', 'Los apellidos pueden tener máximo 20 caracteres');
        return;
    }

    if (email.length > 50) {
        setSearching(false);
        openAlert('Crear profesor', 'El email puede tener un máximo de 50 caracteres')
        return;
    }

    if (especialidad.length > 12) {
        setSearching(false);
        openAlert('Crear profesor', 'La especialidad puede tener máximo 20 caracteres');
        return;
    }
    

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

    if (isSearching) return;
    setSearching(true);

    try {
        const response = await fetch('/profesores/', {
            method: 'POST',
            body: formData
        });
    
        if (response.ok) {
            openAlert('Crear profesor', `Profesor creado satisfactoriamente`)
            window.location.href = '/profesores/'
        } else {
            openAlert('Crear profesor', `Error al crear profesor`)
        }
    } catch (error) {
        console.log(error)
    } finally {
        setSearching(false);
    }
}

// Eliminar profesor
async function eliminar_profesor(idusuarios) {
    try {
        const confirm = await openConfirm('Eliminar profesor', 'Estas seguro de que quieres eliminar el profesor?');
        if (confirm) {
            if (isSearching) return;
            setSearching(true);
            const response = await fetch(`/profesores/eliminar_profesor/${idusuarios}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
        
            if (response.ok) {
                openAlert('Eliminar profesor', `Profesor eliminado satisfactoriamente`)
                window.location.reload();
            } else {
                openAlert('Eliminar profesor', `Error al eliminar profesor`)
            }
        }
    } catch(e) {
        console.error(e);
    } finally {
        setSearching(false);
    }
}

// Usuarios

function update_foto(idusuarios) {
    const form = document.getElementById('updateFoto');
    const imagen = document.getElementById('fotoPerfil').files[0];

    if (!imagen) {
        openAlert('Editar usuario', 'Debe seleccionar una imágen');
        return;
    }

    if (isSearching) return;
    setSearching(true);
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
                openAlert('Editar usuario', 'Imágen actualizada');
                window.location.reload();
            } else {
                openAlert('Editar usuario', 'Error al actualizar imágen');
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setSearching(false);
        }
    });
}

async function edit_email(idusuarios) {
    const email = document.getElementById('edit-email').value;

    if(!email) {
        setSearching(false);
        openAlert('Editar usuario', 'Debe ingresar un correo valido');
        return;
    }

    if (email.length > 50) {
        setSearching(false);
        openAlert('Editar usuario', 'El email puede tener máximo 50 caracteres');
        return;
    }

    try {
        if (isSearching) return;
        setSearching(true);
        const response = await fetch(`/update_email/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'email': email})
        });
    
        if (response.ok) {
            openAlert('Editar usuario', 'Email actualizado satisfactoriamente');
            window.location.reload();
        } else {
            openAlert('Editar usuario', 'Error al actualizar email');
        }
    } catch (e) {
        console.log(`Error: ${e}`);
    } finally {
        setSearching(false);
    }
}

async function edit_nombres(idusuarios) {
    const nombre = document.getElementById('editNombre').value;
    const segundoNombre = document.getElementById('editSegundoNombre').value;

    if (!nombre) {
        setSearching(false);
        openAlert('Editar usuario', 'El campo nombre no puede estar vacio');
        return;
    }

    if (nombre.length > 12 || segundoNombre.length > 12) {
        setSearching(false);
        openAlert('Editar usuario', 'Los nombres pueden tener máximo 12 caracteres');
        return;
    }

    try{
        if (isSearching) return;
        setSearching(true);
        const response = await fetch(`/edit_nombres/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'nombre': nombre, 'segundoNombre': segundoNombre})
        });
    
        if (response.ok) {
            openAlert('Editar usuario', 'Nombres actualizados');
            window.location.reload();
        } else {
            openAlert('Editar usuario', 'Error actualzando nombres');
        }
    } catch (e) {
        console.log(`Error: ${e}`)
    } finally {
        setSearching(false);
    }
}

async function edit_apellidos(idusuarios) {
    const apellido = document.getElementById('editApellido').value;
    const segundoApellido = document.getElementById('editSegundoApellido').value;

    if (!apellido || !segundoApellido) {
        setSearching(false);
        openAlert('Editar usuario', 'Debe llenar ambos apellidos');
        return;
    }

    if (apellido.length > 20 || segundoApellido.length > 20) {
        setSearching(false);
        openAlert('Editar usuario', 'Los apellidos pueden tener un máximo de 20 caracteres');
        return;
    }

    try{
        if (isSearching) return;
        setSearching(true);
        const response = await fetch(`/edit_apellidos/${idusuarios}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'apellido': apellido, 'segundoApellido': segundoApellido})
        });
    
        if (response.ok) {
            openAlert('Editar usuario', 'Apellidos actualizados');
            window.location.reload();
        } else {
            openAlert('Editar usuario', 'Error actualizando apellidos');
        }
    } catch (e) {
        console.log(`Error: ${e}`)
    } finally {
        setSearching(false);
    }
}

async function edit_cedula(idusuarios) {
    const cedula = document.getElementById('edit-cedula').value;
    if (isSearching) return;
    setSearching(true);

    if(!cedula) {
        setSearching(false);
        openAlert('Editar usuario', 'Debe ingresar la cédula');
        return;
    }

    if (cedula.length > 8) {
        setSearching(false);
        openAlert('Editar usuario', 'La cédula puede tener máximo 8 caracteres');
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
            openAlert('Editar usuario', 'Cédula actualizada satisfactoriamente');
            window.location.reload();
        } else {
            openAlert('Editar usuario', 'Error al actualizar cédula');
        }
    } catch (e) {
        console.log(`Error: ${e}`);
    } finally {
        setSearching(false);
    }
}

async function edit_contraseña(idusuarios) {
    const contraseñaActual = document.getElementById('edit-contraseña').value;
    const contraseaNueva = document.getElementById('contraseña-nueva').value;
    if (isSearching) return;
    setSearching(true);

    if (contraseaNueva.length > 8 || contraseñaActual.length > 8) {
        setSearching(false);
        openAlert('Editar usuario', 'La contraseña puede tener máximo 8 caracteres');
        return;
    }

    if (!contraseaNueva || !contraseñaActual) {
        setSearching(false);
        openAlert('Editar usuario', 'Debe llenar ambos campos de contraseña');
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
            openAlert('Editar usuario', 'Contraseña actualizada');
            log_out();
        } else{
            openAlert('Editar usuario', 'La contraseña actual es incorrecta');
        }
    } catch(e) {
        console.log(`Error: ${e}`);
    } finally {
        setSearching(false);
    }
}

// Facultad

async function crearFacultad(event) {
    event.preventDefault();
    const nombreFacultad = document.getElementById('nombreFacultad').value;

    if (nombreFacultad === '') {
        setSearching(false);
        openAlert('Crear facultad', 'Debe ingresar el nombre de la facultad');
        return;
    }

    if (nombreFacultad.length > 30) {
        setSearching(false);
        openAlert('Crear facultad', 'La facultad puede tener un máximo de 30 caracteres');
        return;
    }


    if (isSearching) return;
    setSearching(true);
    const formData = new FormData;
    formData.append('nombreFacultad', nombreFacultad)

    try {
        const response = await fetch('/facultades/', {
            method: 'POST',
            body: formData
        })
    
        if (response.ok) {
            openAlert('Crear facultad', 'Facultad creada');
            window.location.reload();
        } else{
            openAlert('Crear facultad', 'Error al crear facultad');
        }
    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

function obtener_campos_facultad(idfacultad) {
    const editNombreFacultad = document.getElementById('edit-nombreFacultad');
    const nombreFacultad = document.getElementById(`nombre-facultad-${idfacultad}`).textContent;
    const btnModalEditFacultad = document.getElementById('btn-edit-facultad')

    btnModalEditFacultad.setAttribute('idfacultad', idfacultad)

    editNombreFacultad.value = nombreFacultad
}

async function editar_facultad(idfacultad, event) {
    event.preventDefault();
    const form = document.getElementById('edit-facultad-form');
    const nombreFacultad = document.getElementById('edit-nombreFacultad').value;

    if (nombreFacultad === '') {
        setSearching(false);
        openAlert('Editar facultad', 'Debe ingresar el nombre de la facultad');
        return;
    }

    if (nombreFacultad.length > 30) {
        setSearching(false);
        openAlert('Editar facultad', 'La facultad puede tener un máximo de 30 caracteres');
        return;
    }

    if (isSearching) return;
    setSearching(true);

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
    } finally {
        setSearching(false);
    }
}

async function elim_facultad(idfacultad) {
    const confirm = await openConfirm('Eliminar facultad', '¿Estas seguro de quieres eliminar esta facultad?, esto afectara a los cursos que estan dentro de esta')
    if(confirm) {
        try {
            if (isSearching) return;
            setSearching(true);
            const response = await fetch(`/facultades/edit_facultad/${idfacultad}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
    
            if (response.ok) {
                openAlert('Eliminar facultad', 'Facultad eliminada');
                window.location.href = '/facultades/'
            } else {
                openAlert('Eliminar facultad', 'Error al eliminar facultad');
            }
        } catch (e) {
            console.log(`Error: ${e}`)
        } finally {
            setSearching(false);
        }
    }
}

// Alumnos

// Eliminar alumno

async function eliminar_usuario(idusuarios) {
    const confirm = await openConfirm('¿Eliminar alumno', 'Estas seguro de eliminar el alumno?')
    if (confirm) {
        
        try {
            if (isSearching) return;
            setSearching(true);
            const response = await fetch(`/alumnos/eliminar_alumno/${idusuarios}`, {
                method: 'DELETE'
            });
    
            if (response.ok) {
                openAlert('Eliminar alumno', 'Alumno eliminado');
                window.location.reload();
            } else {
                openAlert('Eliminar alumno', 'Error al eliminar alumno');
            }
        } catch(e) {
            console.log(`Error: ${e}`);
        } finally {
            setSearching(false);
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
    if (isSearching) return;
    setSearching(true);

    if (!nombrePapa || !apellidoMama || !apellidoPapa || !nombreMama || !contacto) {
        setSearching(false);
        openAlert('Registro familiar', 'Todos los campos son obligatorios');
        return;
    }

    if (nombrePapa.length > 12 || nombreMama.length > 12) {
        setSearching(false);
        openAlert('Registro familiar', 'Los nombres pueden tener un máximo de 12 caractéres');
        return;
    }

    if (apellidoPapa.length > 20 || apellidoMama.length > 20) {
        setSearching(false);
        openAlert('Registro familiar', 'Los apellidos pueden tener un máximo de 20 caractéres');
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

        openAlert('Registro familiar', `${data.message}`);
        window.location.reload();
    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

async function edit_datos_papa(idFamilia, event) {
    event.preventDefault();
    const url = `/alumnos/edit_registro_fam_papa/${idFamilia}`;
    const NombrePapa = document.getElementById('editNombrePapa').value.trim();
    const ApellidoPapa = document.getElementById('editApellidoPapa').value.trim();
    const formData = new FormData();
    if (isSearching) return;
    setSearching(true);

    if (!NombrePapa || !ApellidoPapa) {
        setSearching(false);
        openAlert('Registro familiar', 'Todos los campos son obligatorios');
        return;
    }

    if (NombrePapa.length > 12) {
        setSearching(false);
        openAlert('Registro familiar', 'Los nombres pueden tener un máximo de 20 caractéres');
        return;
    }

    if (ApellidoPapa.length > 20) {
        setSearching(false);
        openAlert('Registro familiar', 'Los apellidos pueden tener un máximo de 20 caractéres');
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

        openAlert('Registro familiar', `${data.message}`);
        window.location.reload();
    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

async function edit_datos_mama(idFamilia, event) {
    event.preventDefault();
    const url = `/alumnos/edit_registro_fam_mama/${idFamilia}`;
    const NombreMama = document.getElementById('editNombreMama').value.trim();
    const ApellidoMama = document.getElementById('editApellidoMama').value.trim();
    const formData = new FormData();
    if (isSearching) return;
    setSearching(true);

    if (!NombreMama || !ApellidoMama) {
        setSearching(false);
        openAlert('Registro familiar', 'Todos los campos son obligatorios');
        return;
    }

    if (NombreMama.length > 12) {
        setSearching(false);
        openAlert('Registro familiar', 'Los nombres pueden tener un máximo de 20 caractéres');
        return;
    }

    if (ApellidoMama.length > 20) {
        setSearching(false);
        openAlert('Registro familiar', 'Los apellidos pueden tener un máximo de 20 caractéres');
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

        openAlert('Registro familiar', `${data.message}`);
        window.location.reload();
    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

async function edit_datos_contacto(idFamilia, event) {
    event.preventDefault();
    const url = `/alumnos/edit_registro_fam_contacto/${idFamilia}`;
    const contacto = document.getElementById('edit-contacto').value.trim();
    const formData = new FormData();
    if (isSearching) return;
    setSearching(true);

    if (!contacto) {
        setSearching(false);
        openAlert('Registro familiar', 'Todos los campos son obligatorios');
        return;
    }

    if (contacto.length > 11) {
        setSearching(false);
        openAlert('Registro familiar', 'El teléfono puede tener máximo 11 caractéres');
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

        openAlert('Registro familiar', `${data.message}`);
        window.location.reload();
    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

async function eliminar_registro_familiar(idRegistro) {
    const url = `/alumnos/eliminar_registro_familiar/${idRegistro}`;
    const confirm = await openConfirm('Registro familiar', 'Estas seguro de que quieres eliminar el registro familiar?');

    if(confirm) {
        try {
            if (isSearching) return;
            setSearching(true);
            const response = await fetch(url, {
                method: 'DELETE'
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error);
            }

            openAlert('Registro familiar', `${data.message}`);
            window.location.reload();
        } catch (e) {
            console.log(e)
        } finally {
            setSearching(false);
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
        setSearching(true);

        const formData = new FormData;
        const cedula = document.getElementById('inscripcion-buscar-cedula').value.trim();
        const url = '/inscripciones/buscar_alumno'

        formData.append('cedula', cedula)

        if (!cedula) {
            setSearching(false);
            openAlert('Inscripciones', 'Debe ingresar una cédula');
            return;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                openAlert('Inscripciones', 'No se encontro el alumno');
                throw new Error('Hubo un error buscando al alumno')
            }

            let data = await response.json()
            mostrar_panel_inscripcion(data.alumno)

        } catch(e) {
            console.log(e)
        } finally {
            setSearching(false);
        }
    })
}

async function buscar_curso() {
    if (isSearching) return;
    setSearching(true);
    const curso = document.getElementById('curso-inscripcion').value;
    const url = '/inscripciones/buscar_curso';

    if (!curso) {
        setSearching(false);
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
            openAlert('Inscripciones', 'Curso no encontrado');
            throw new Error ('Error al buscar el curso');
        }

        const data = await response.json()
        seleccionar_seccion(data.cursos)
    } catch (e) {
        console.log(e);
    } finally {
        setSearching(false);
    }
}

async function buscar_horario() {
    if (isSearching) return;
    setSearching(true);
    const idSeccion = document.getElementById('select-seccion-inscripcion').value.trim();
    const url = '/inscripciones/mostar_horario';

    if (!idSeccion || idSeccion === 'Selecciona una Sección') {
        setSearching(false);
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
        setSearching(false);
    }
}

async function elim_preinscripcion(event, id) {
    event.preventDefault();
    const url = `/inscripciones/elim_preinscripcion/${id}`;
    const confirm = await openConfirm('Preinscripciones', '¿Estás seguro de que quieres eliminar la preinscripción?')
    if (confirm) {
            if (isSearching) return;
            setSearching(true);
            try {
                const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = response.json()

            if (!response.ok) {
                openAlert('Preinscripciones', `${data.error}`);
                throw new Error(data.error);
            }

            openAlert('Preinscripciones', 'La preinscripción fue eliminada')
            window.location.reload();
        } catch(e) {
            console.error(e);
        } finally {
            setSearching(false);
        }
    }
}

async function inscribir_alumno(event) {
    event.preventDefault();
    const form = document.getElementById('inscripcion-form');
    const idAlumno = document.getElementById('alumno-id-inscripcion').value;
    const periodoInicio = document.getElementById('InicioPeriodo').value;
    const periodoFinal = document.getElementById('FinPeriodo').value;
    const tipoInscripcion = document.getElementById('select-tipo-inscripcion').value;
    const idSeccion = document.getElementById('select-seccion-inscripcion').value;
    if (isSearching) return;
    setSearching(true);

    if (!form) {
        setSearching(false);
        return;
    }

    if (!periodoInicio || !periodoFinal) {
        setSearching(false);
        openAlert('Inscripciones', 'Debes ingresar el periodo de inscripcion');
        return;
    }

    if (periodoInicio > periodoFinal) {
        setSearching(false);
        openAlert('Inscripciones', 'La fecha "Inicio" no puede ser mayor que la de "Finalización"');
        return;
    }

    if (!idSeccion) {
        setSearching(false);
        openAlert('Inscripciones', 'Debes ingresar una sección');
        return;
    }

    if (!tipoInscripcion) {
        setSearching(false);
        openAlert('Inscripciones', 'Es necesario especificar el tipo de inscripción');
        return;
    }

    const formData = new FormData();
    formData.append('idAlumno', idAlumno);
    formData.append('periodoInicio', periodoInicio);
    formData.append('periodoFinal', periodoFinal);
    formData.append('idSeccion', idSeccion);
    formData.append('tipo', tipoInscripcion);

    try {
        const response = await fetch('/inscripciones/inscribir_alumno', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.mensaje || 'Error al inscribir');
                
        openAlert('Inscripciones', `${data.mensaje}`);
        window.location.reload();
        } catch (e) {
            openAlert('Inscripciones', `${e.message}`);
            console.error(e);
        } finally {
            setSearching(false);
        }
}

async function crearAlumno(event) {
    event.preventDefault();
    const rol = 'alumno'
    const nombre = document.getElementById('nombreAlumno').value.trim();
    const segundoNombre = document.getElementById('segundoNombreAlumno').value.trim();
    const apellido = document.getElementById('apellidoAlumno').value.trim();
    const segundoApellido = document.getElementById('segundoApellidoAlumno').value.trim();
    const cedula = document.getElementById('cedulaAlumno').value.trim();
    const email = document.getElementById('emailAlumno').value.trim();
    const contraseña = document.getElementById('contraseñaAlumno').value.trim();
    const imagen = document.getElementById('imagenAlumno').files[0];

    if (isSearching) return;
    setSearching(true);


    if (!nombre) {
        setSearching(false);
        openAlert('Crear alumno', 'El campo nombre esta vacio');
        return;
    }

    if (!apellido) {
        setSearching(false);
        openAlert('Crear alumno', 'El campo apellido esta vacio');
        return;
    }

    if (!cedula) {
        setSearching(false);
        openAlert('Crear alumno', 'El campo cedula esta vacio');
        return;
    }

    if (!email) {
        setSearching(false);
        openAlert('Crear alumno', 'El campo email esta vacio');
        return;
    }

    if (!contraseña) {
        setSearching(false);
        openAlert('Crear alumno', 'El campo contraseña esta vacio');
        return;
    }

    if (cedula.length > 8) {
        setSearching(false);
        openAlert('Crear alumno', 'El campo cedula esta vacio');
        return;
    }

    if (contraseña.length > 8) {
        setSearching(false);
        openAlert('Crear alumno', 'La contraseña puede tener máximo 8 caracteres');
        return;
    }

    if (nombre.length > 12 || segundoNombre.length > 12) {
        setSearching(false);
        openAlert('Crear alumno', 'Los nobres pueden tener máximo 12 caracteres');
        return;
    }

    if (apellido.length > 20 || segundoApellido.length > 20) {
        setSearching(false);
        openAlert('Crear alumno', 'Los apellidos pueden tener máximo 20 caracteres');
        return;
    }

    if (email.length > 50) {
        setSearching(false);
        openAlert('Crear alumno', 'El email puede tener un máximo de 50 caracteres')
        return;
    }

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
    try {
        const response = await fetch('/inscripciones/alumnos_regulares', {
            method: 'POST',
            body: formData
        });
    
        if (response.ok) {
            openAlert('Crear alumno', 'Alumno creado satisfactoriamente')
            clearInputs(['nombreAlumno', 'segundoNombreAlumno', 'apellidoAlumno', 'segundoApellidoAlumno', 'cedulaAlumno', 'emailAlumno', 'contraseñaAlumno', 'imagenAlumno'])
            document.getElementById('inscripcion-buscar-cedula').value = cedula;
        } else {
            openAlert('Crear alumno', 'Error al crear alumno')
        }
    } catch (error) {
        console.log(error)
    } finally {
        setSearching(false);
    }
}

function clearInputs(array) {
    array.forEach((element) => {
        document.getElementById(element).value = '';
    })
}

// CURSOS

async function get_facultades() {
    const url = '/cursos/buscar_facultades';

    if (isSearching) return;
    setSearching(true);

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
        setSearching(false);
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

    const url = '/cursos/';
    const facultad = document.getElementById('facultad-curso').value;
    const nombre_curso = document.getElementById('curso').value.trim();
    const duracion_curso = document.getElementById('duracion').value.trim();

    if (isSearching) return;
    setSearching(true);

    if (!facultad || !nombre_curso || duracion_curso) {
        setSearching(false);
        openAlert('Cursos', 'Todos los campos son obligatorios');
        return;
    }

    if (nombre_curso.length > 30) {
        setSearching(false);
        openAlert('Cursos', 'El nombre del curso puede tener máximo 30 caracteres');
        return;
    }

    const formData = new FormData();

    formData.append('idFacultad', facultad);
    formData.append('nombre_curso', nombre_curso);
    formData.append('duracion_curso', duracion_curso);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if(!response.ok) {
            openAlert('Cursos', `${data.error}`);
            throw new Error(data.error);
        }

        openAlert('Cursos', `${data.message}`);
        window.location.reload();
    } catch (e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

async function elim_curso(idcurso) {
    const url = `/cursos/eliminar_curso/${idcurso}`;
    const confirm = await openConfirm('Cursos', '¿Quieres eliminar este curso?');
    
    if (confirm) {
        try {
            if (isSearching) return;
            setSearching(true);
            const response = await fetch(url, {
                method: 'DELETE'
            });

            const data = response.json();

            if (!response.ok) {
                openAlert('Cursos', 'Error al eliminar curso');
                throw new Error(`Error: ${data.error}`)
            }

            openAlert('Cursos', 'Curso eliminado');
            window.location.reload();
        } catch (e) {
            console.log(e)
        } finally {
            setSearching(false);
        }
    }

}

async function edit_nombre_curso(idCurso, event) {
    event.preventDefault();
    const url = `/cursos/edit_nombre_curso/${idCurso}`;
    const curso = document.getElementById('editNombreCurso').value.trim();
    const formData = new FormData();
    if (isSearching) return;
    setSearching(true);

    if (!curso) {
        setSearching(false);
        openAlert('Cursos', 'Debe ingresar el nombre del curso');
        return;
    }

    if (curso.length > 30) {
        setSearching(false);
        openAlert('Cursos', 'El curso puede tener máximo 30 caracteres');
        return;
    }

    formData.append('curso', curso)

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            openAlert('Cursos', `${data.error}`);
            throw new Error(data.error);
        }

        openAlert('Cursos', `${data.message}`);
        window.location.reload();
    } catch (e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

async function edit_duracion_curso(idCurso, event) {
    event.preventDefault();
    const url = `/cursos/edit_duracion_curso/${idCurso}`;
    const duracion = document.getElementById('editDuracionCurso').value.trim();
    const formData = new FormData();
    if (isSearching) return;
    setSearching(true);

    if (!duracion) {
        setSearching(false);
        openAlert('Cursos', 'Debe ingresar la duración del curso');
        return;
    }

    formData.append('duracion', duracion)

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
    } catch (e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

async function edit_facultad_curso(idCurso, event) {
    event.preventDefault();
    const url = `/cursos/edit_facultad_curso/${idCurso}`;
    const facultad = document.getElementById('selectFacultadesEdit').value;
    const formData = new FormData();
    if (isSearching) return;
    setSearching(true);

    if (!facultad) {
        setSearching(false);
        openAlert('Cursos', 'Debe ingresar una facultad para el curso');
        return;
    }

    formData.append('facultad', facultad);

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
    } finally {
        setSearching(false);
    }
}

// SECCIONES 

async function eliminar_seccion(idSeccion) {
    const url = `/cursos/elim_seccion/${idSeccion}`;
    const confirm = await openConfirm('Secciones', '¿Estás seguro de que quieres eliminar la sección');
    if (confirm) {
        if (isSearching) return;
        setSearching(true);
        try {
            const response = await fetch(url, {
                method: 'DELETE'
            });

            const data = await response.json();

            if(!response.ok) {
                throw new Error(data.error);
            }

            openAlert('Secciones', `${data.message}`);
            window.location.reload();
        } catch(e) {
            console.log(e)
        } finally {
            setSearching(false);
        }
    }
}

async function crear_Seccion(idCurso, event) {
    event.preventDefault();
    const url = `/cursos/craer_seccion/${idCurso}`;
    const seccion = document.getElementById('crearSeccion').value.trim();
    const profesor = document.getElementById('profesorCrearSeccion').value.trim();
    const aula = document.getElementById('aulaSeccion').value.trim();
    if (isSearching) return;
    setSearching(true);

    if (!seccion || !profesor || horariosSeleccionados.length <= 0 || !aula) {
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

    horariosSeleccionados.forEach(element => {
        console.log(element.dia)
        console.log(element.horaInicio);
        console.log(element.horaFin);
    })

    // Preparar datos estructurados
    const requestData = {
        seccion: seccion,
        profesor: profesor,
        aula: aula,
        horarios: horariosSeleccionados.map(item => ({
            dia: item.dia,
            hora_inicio: item.horaInicio,
            hora_fin: item.horaFin
        }))
    };
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            openAlert('Secciones', `${data.error}`);
            throw new Error();
        }

        openAlert('Secciones', `${data.message}`);
        while(horariosSeleccionados.length) {
            horariosSeleccionados.pop();
        }
        window.location.href = `/cursos/seccion_curso/${idCurso}`;
    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
    
}

async function edit_seccion(event, id, idSeccion) {
    event.preventDefault();
    if (isSearching) return;
    setSearching(true);
    const url = `/cursos/edit_seccion_campos/${idSeccion}`
    const edit = document.getElementById(id)
    const formData = new FormData();

    if (id == 'editSeccion') {
        if (edit.value.trim().length > 10) {
            setSearching(false);
            openAlert('Secciones', `La sección no puede tener más de 10 caracteres`);
            return;
        }

        if (!edit.value.trim()) {
            setSearching(false);
            openAlert('Secciones', `El campo no puede estar vacio`);
            return;
        }

        formData.append('seccion', edit.value.trim())
    }

    if (id == 'profesorEditSeccion') {
        formData.append('profesor', edit.value.trim())
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            body: formData
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

async function edit_horario(idSeccion) {
    const url = `/cursos/edit_horario_seccion/${idSeccion}`;
    const profesor = document.getElementById('profesorEditSeccion').value;
    if (isSearching) return;
    setSearching(true);

    const horariosLimpios = horariosSeleccionados.filter(item => 
        item && 
        item.celdaId && 
        item.dia && 
        item.horaInicio && 
        item.horaFin && 
        item.curso
    );
    
    console.log('Enviando horarios limpios:', horariosLimpios);
    
    if (horariosLimpios.some(item => !item.celdaId)) {
        openAlert('Secciones', `Hay horarios corruptos. Por favor recarga la página.`);
        setSearching(false);
        return;
    }

    const requestData = {
        horarios: horariosLimpios,
        idProfesor: profesor
    };
    
    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Error al actualizar horario');
            openAlert('Secciones', `${data.error }` || 'Error al actualizar horario');
            throw new Error(data.error);
        }

        openAlert('Secciones', `${data.mensaje}`);
        horariosSeleccionados.length = 0;
        window.location.reload();
    } catch(e) {
        console.error('Error en edit_horario:', e);
    } finally {
        setSearching(false);
    }
}

async function buscar_horario_seccion(idSeccion) {
    if (isSearching) return;
    setSearching(true);
    const url = '/inscripciones/mostar_horario';

    if (!idSeccion || idSeccion === 'Selecciona una Sección') {
        setSearching(false);
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
        setSearching(false);
    }
}


// CALIFICACIONES 

async function colocar_logro_uno(idSeccion, idAlumno, idInscripcion) {
    const url = `/cursos/subir_logro_uno/${idSeccion}`;
    const inputNota = document.getElementById(`input-logro1-${idAlumno}`).value.trim();

    if (!inputNota) {
        alert('Debe ingresar una calificacion');
        return;
    }

    const requestData = {
        logro: inputNota,
        idAlumno: idAlumno,
        idInscripcion: idInscripcion
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        //alert(data.message);
        calcular_definitiva(idSeccion, idAlumno, idInscripcion);
    } catch(e) {
        console.log(e)
    }
}

async function colocar_logro_dos(idSeccion, idAlumno, idInscripcion) {
    const url = `/cursos/subir_logro_dos/${idSeccion}`;
    const inputNota = document.getElementById(`input-logro2-${idAlumno}`).value.trim();

    if (!inputNota) {
        alert('Debe ingresar una calificacion');
        return;
    }

    const requestData = {
        logro: inputNota,
        idAlumno: idAlumno,
        idInscripcion: idInscripcion
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        //alert(data.message);
        calcular_definitiva(idSeccion, idAlumno, idInscripcion);
    } catch(e) {
        console.log(e)
    }
}

async function colocar_logro_tres(idSeccion, idAlumno, idInscripcion) {
    const url = `/cursos/subir_logro_tres/${idSeccion}`;
    const inputNota = document.getElementById(`input-logro3-${idAlumno}`).value.trim();

    if (!inputNota) {
        alert('Debe ingresar una calificacion');
        return;
    }

    const requestData = {
        logro: inputNota,
        idAlumno: idAlumno,
        idInscripcion: idInscripcion
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        //alert(data.message);
        calcular_definitiva(idSeccion, idAlumno, idInscripcion);
    } catch(e) {
        console.log(e)
    }
}

async function colocar_logro_cuatro(idSeccion, idAlumno, idInscripcion) {
    const url = `/cursos/subir_logro_cuatro/${idSeccion}`;
    const inputNota = document.getElementById(`input-logro4-${idAlumno}`).value.trim();

    if (!inputNota) {
        alert('Debe ingresar una calificacion');
        return;
    }

    const requestData = {
        logro: inputNota,
        idAlumno: idAlumno,
        idInscripcion: idInscripcion
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        //alert(data.message);
        calcular_definitiva(idSeccion, idAlumno, idInscripcion);
    } catch(e) {
        console.log(e)
    }
}

async function colocar_logro_cinco(idSeccion, idAlumno, idInscripcion) {
    const url = `/cursos/subir_logro_cinco/${idSeccion}`;
    const inputNota = document.getElementById(`input-logro5-${idAlumno}`).value.trim();

    if (!inputNota) {
        alert('Debe ingresar una calificacion');
        return;
    }

    const requestData = {
        logro: inputNota,
        idAlumno: idAlumno,
        idInscripcion: idInscripcion
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        //alert(data.message);
        calcular_definitiva(idSeccion, idAlumno, idInscripcion);
    } catch(e) {
        console.log(e)
    }
}

async function calcular_definitiva(idSeccion, idAlumno, idInscripcion) {
    const url = `/cursos/subir_definitiva/${idSeccion}`;
    //if (isSearching) return;
    const parsearNota = (id) => {
        const valor = document.getElementById(id).value.trim();
        return valor === "" ? 0 : parseFloat(valor);
    };

    let nota1 = parsearNota(`input-logro1-${idAlumno}`) * 0.20;
    let nota2 = parsearNota(`input-logro2-${idAlumno}`) * 0.20;
    let nota3 = parsearNota(`input-logro3-${idAlumno}`) * 0.20;
    let nota4 = parsearNota(`input-logro4-${idAlumno}`) * 0.20;
    let nota5 = parsearNota(`input-logro5-${idAlumno}`) * 0.20;

    const definitiva = (nota1 + nota2 + nota3 + nota4 + nota5).toFixed(1);

    const requestData = {
        definitiva: definitiva,
        idAlumno: idAlumno,
        idInscripcion: idInscripcion
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error);
            throw new Error(data.error);
        }
        document.getElementById(`input-def-${idAlumno}`).value = definitiva;

        if (definitiva < 14) {
            document.getElementById(`input-def-${idAlumno}`).classList.add('reprobado');
        } else {
            document.getElementById(`input-def-${idAlumno}`).classList.remove('reprobado');
        }
    } catch(e) {
        console.log(e)
    }
}

async function asistencia(id, idAlumno) {
    const url = `/cursos/asistencia/${id}`;
    const inputNota = document.getElementById(`asistencia-${idAlumno}`).value.trim();

    if (!inputNota) {
        alert('Debe ingresar una asistencia');
        return;
    }

    const requestData = {
        asistencia: inputNota
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        //alert(data.message);
    } catch(e) {
        console.log(e)
    }
}

async function inasistencia(id, idAlumno) {
    const url = `/cursos/inasistencia/${id}`;
    const inputNota = document.getElementById(`inasistencia-${idAlumno}`).value.trim();

    if (!inputNota) {
        alert('Debe ingresar una cantidad');
        return;
    }

    if (parseInt(inputNota) >= 3) {
        document.getElementById(`inasistencia-${idAlumno}`).classList.add('reprobado');
    } else {
        document.getElementById(`inasistencia-${idAlumno}`).classList.remove('reprobado');
    }

    const requestData = {
        inasistencia: inputNota
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        //alert(data.message);
    } catch(e) {
        console.log(e)
    }
}

// ACERCA DE

async function restaurar() {
    if (confirm('¿Estás seguro de que quieres restaurar el sistema?, todos los registros serán eliminados')) {
        
        try {
            if (isSearching) return;
            setSearching(true);
            const url = '/acerca/restaurar';

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            const data = await response.json();

            if (!response.ok) throw new Error(data.error);

            alert(data.mensaje);
            log_out();
        } catch(e) {
            console.error(e);
        } finally {
            setSearching(false);
        }
    }
}

async function respaldo() {
    const confirm = await openConfirm('Respaldo', 'A continuación se generara un backup de la base de datos')
    if (confirm) {
        
        try {
            if (isSearching) return;
            setSearching(true);
            const url = '/acerca/generar-backup';

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error);
            }

            const blob = await response.blob();
            const response_url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = response_url;
            
            // Obtener el nombre del archivo del header Content-Disposition
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'backup.sql';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }
            
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(response_url);
            document.body.removeChild(a);
            
            openAlert('Respaldo', 'Respaldo generado satisfactoriamente');
        } catch(e) {
            console.error(e);
        } finally {
            setSearching(false);
        }
    }
}

async function descargar_manual() {
    if (isSearching) return;
    setSearching(true);
    const url = '/descargar-pdf/manual.pdf'
    try {
        const response = await fetch(url, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error('Error al descragar manual de usuario');
        }

                const blob = await response.blob();
        
        const urlTemporal = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = urlTemporal;
        link.download = 'manual.pdf';
        document.body.appendChild(link);
        
        link.click();
        
        document.body.removeChild(link);
        window.URL.revokeObjectURL(urlTemporal);

    } catch(e) {
        console.log(e)
    } finally {
        setSearching(false);
    }
}

// FACTURACIÓN

async function crearProducto(event) {
    event.preventDefault();
    const producto = document.getElementById('nombreProducto').value.trim();
    const precio = document.getElementById('precioProducto').value.trim();
    const stock = document.getElementById('stockProducto').value.trim();

    if (isSearching) return;
    setSearching(true);

    if (!producto || !precio || !stock) {
        setSearching(false);
        openAlert('Inventario', 'Todos los campos son obligatorios');
        return;
    }

    if (producto.length > 20) {
        setSearching(false);
        openAlert('Inventario', 'El producto puede tener un máximo de 20 caracteres');
        return;
    }

    const url = '/facturacion/inventario';
    const formData = new FormData();
    formData.append('nombre', producto);
    formData.append('precio', precio);
    formData.append('stock', stock);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error);

        openAlert('Inventario', `${data.mensaje}`);
        window.location.reload();
    } catch(e) {
        openAlert('Inventario', `${e}`);
        console.error(e)
    } finally {
        setSearching(false);
    }
}

async function elim_producto(idProducto) {
    const url = `/facturacion/elim_producto/${idProducto}`;
    const confirm = await openConfirm('Inventario' , '¿Estás seguro de que quieres eliminar el producto?')
    if (confirm) {
        try {
            if (isSearching) return;
            setSearching(true);
            const response = await fetch(url, {
                method: 'DELETE',
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error)
                throw new Error(data.error);
            }

            openAlert('Inventario', `Producto eliminado`);
            window.location.reload();
        } catch(e) {
            console.error(e)
        } finally {
            setSearching(false);
        }
    }
}

async function editar_producto(event, idProducto, campo) {
    event.preventDefault();
    const url = `/facturacion/edit_producto/${idProducto}`;
    const formData = new FormData();
    const edit = document.getElementById(campo).value.trim();
    if (isSearching) return;
    setSearching(true);

    if (!edit) {
        setSearching(false);
        openAlert('Inventario', `El campo a actualizar debe estar lleno`);
        return;
    }

    if (campo === 'editNombreProducto') {
        
        if (edit.length > 20) {
            setSearching(false);
            openAlert('Inventario', `El nombre del producto puede tener máximo 20 caracteres`);
            return;
        }

        formData.append('nombre', edit);
    }

    if (campo === 'editPrecioProducto') {
        formData.append('precio', edit);
    }

    if (campo === 'editStockProducto') {
        formData.append('stock', edit);
    }

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error);
            throw new Error(data.error);
        }

        openAlert('Inventario', `${data.mensaje}`);
        window.location.reload();
    } catch(e) {
        console.error(e);
    } finally {
        setSearching(false);
    }
}

async function elim_factura(idFactura) {
    const url = `/facturacion/elim_factura/${idFactura}`;
    const confirm = await openConfirm('Inventario', '¿Estás seguro de que quieres eliminar la factura?');
    if (confirm) {
        if (isSearching) return;
        setSearching(true);
        try {
            const response = await fetch(url, {
                method: 'DELETE',
            });

            const data = await response.json();

            if (!response.ok) {
                openAlert('Inventario', `${data.error}`);
                throw new Error(data.error);
            }

            openAlert('Inventario', `${data.mensaje}`);
            window.location.reload();
        } catch(e) {
            console.error(e)
        } finally {
            setSearching(true);
        }
    }
}

async function buscar_producto() {
    const producto = document.getElementById('buscar-producto').value.trim();
    const formData = new FormData();
    const url = '/facturacion/buscar_producto_factura';
    if (isSearching) return;
    setSearching(true);

    if (!producto) {
        setSearching(false);
        openAlert('Inventario', `Ingresa un producto a agregar`);
        return;
    }

    try {

        formData.append('nombre', producto)

        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            openAlert('Inventario', `${data.error}`);
            throw new Error(data.error);
        }

        render_producto(data.producto)
    } catch(e) {
        console.error(e);
    } finally {
        setSearching(false);
    }
}

let productosArray = [];
async function guardar_factura() {
    const url = '/facturacion/';
    const cliente = document.getElementById('nombreFactura').value.trim();
    const telefono = document.getElementById('telefonoFactura').value.trim();
    const cedula = document.getElementById('cedulaFactura').value.trim();
    const direccion = document.getElementById('direccionFactura').value.trim();
    const total = parseFloat(document.getElementById('total-factura').innerHTML);
    if (isSearching) return;
    setSearching(true);

    if (!cliente || !cedula || !direccion || !telefono) {
        setSearching(false);
        openAlert('Inventario', `Todos los campos son obligatorios`);
        return;
    }

    if (!cliente.length > 50) {
        setSearching(false);
        openAlert('Inventario', `El cliente puede tener un máximo de 50 caracteres`);
        return;
    }

    if (!telefono.length > 11) {
        setSearching(false);
        openAlert('Inventario', `EL teléfono puede tener un máximo de 10 caracteres`);
        return;
    }

    if (!cedula.length > 8) {
        setSearching(false);
        openAlert('Inventario', `La cédula puede tener un máximo de 8 caracteres`);
        return;
    }

    if (!direccion.length > 50) {
        setSearching(false);
        openAlert('Inventario', `La dirección puede tener un máximo de 30 caracteres`);
        return;
    }

    if (!total || total <= 0) {
        setSearching(false);
        openAlert('Inventario', `El monto no puede ser 0`);
        return;
    }

    const requestData = {
        cliente: cliente,
        telefono: telefono,
        cedula: cedula,
        direccion: direccion,
        total: total,
        productos: productosArray
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

        if (!response.ok) {
            alert(data.error);
            openAlert('Inventario', `${data.error}`);
            throw new Error(data.error);
        }

        openAlert('Inventario', `${data.mensaje}`);
    } catch(e) {
        console.error(e);
    } finally {
        setSearching(false);
    }


}

// INCES

async function inscribir_inces(event) {
    event.preventDefault();
    if (isSearching) return;
    setSearching(true);

    const url = '/inces/'
    const alumno = document.getElementById('alumno-id-inscripcion').value;
    const inicio = document.getElementById('InicioPeriodo').value;
    const final = document.getElementById('FinPeriodo').value;
    const empresa = document.getElementById('selectedValueEmpresa').value;
    const seccion = document.getElementById('selectedValueSecciones').value;

    if (!alumno || alumno == '') {
        setSearching(false);
        openAlert('INCES', 'Debe Buscar un alumno para inscribir');
        return;
    }

    if (!inicio || inicio == '') {
        setSearching(false);
        openAlert('INCES', 'Debe escoger una fecha de inicio');
        return;
    }

    if (inicio > final) {
        setSearching(false);
        openAlert('Inscripciones', 'La fecha "Inicio" no puede ser mayor que la de "Finalización"');
        return;
    }

    if (!empresa || empresa == '') {
        setSearching(false);
        openAlert('INCES', 'Debe escoger la empresa que representa al alumno');
        return;
    }

    if (!final || final == '') {
        setSearching(false);
        openAlert('INCES', 'Debe escoger una fecha de finalización');
        return;
    }

    if (!seccion || seccion == '') {
        setSearching(false);
        openAlert('INCES', 'Debe escoger una sección para inscribir');
        return;
    }

    const requestData = {
        'alumno': alumno,
        'empresa': empresa,
        'inicio': inicio,
        'final': final,
        'seccion': seccion,
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error);
        }

        openAlert('INCES', data.message);
        setTimeout(() => {
            window.location.href = '/inces/gestion_insc';
        }, 1300)
    } catch(e) {
        openAlert('INCES', e);
        console.error(e);
    } finally {
        setSearching(false);
    }
}

async function cambiarStatus(idusuarios, idInscripcion, attribute) {
    if (isSearching) return;
    setSearching(true);

    const url = `/inces/mod_status/${idInscripcion}`;
    console.log(url);
    console.log(idusuarios);
    console.log(attribute);
    console.log(idInscripcion);
    const status = attribute == '1' ? 0: 1;

    const mensaje = attribute == '1' ? 'desactivar': 'activar';

    const requestData = {
        'status': status
    }
    try {
        const confirm = await openConfirm('INCES', `¿Estás seguro de que quieres ${mensaje} la inscripción?`)
        if (confirm) {
            const response = await fetch(url, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error);
            };

            openAlert('INCES', data.message);
            document.getElementById(`btn-status-${idusuarios}`).setAttribute('status', status.toString())
            validarStatusInsc(idusuarios);
        }
    } catch(e) {
        openAlert('INCES', e);
        console.error(e);
    } finally {
        setSearching(false);
    }

}

// EMPRESAS
async function crear_empresa(event) {
    event.preventDefault();
    if (isSearching) return;
    setSearching(true);
    const url = '/inces/empresas'
    const nombre = document.getElementById('nombreEmpresa').value.trim();

    if (!nombre || nombre == '') {
        setSearching(false);
        openAlert('Empresas', 'Debe llenar el campo');
        return;
    }

    if (nombre.length > 30) {
        setSearching(false);
        openAlert('Empresas', 'La empresa puede tener máximo 30 caracteres');
        return;
    }

    const requestData = {
        'nombre': nombre
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

    if (!response.ok) {
        throw new Error(data.error);
    }

    openAlert('Empresas', data.message);
    window.location.reload();
    } catch(e) {
        openAlert('Empresas', data.error);
        console.error(e);
    } finally {
        setSearching(false);
    }
}

async function editar_empresa(event, id) {
    event.preventDefault();
    if (isSearching) return;
    setSearching(true);
    const url = `/inces/mod_empresa/${id}`
    const nombre = document.getElementById('edit-nombreEmpresa').value.trim();

    if (!nombre || nombre == '') {
        setSearching(false);
        openAlert('Empresas', 'Debe llenar el campo');
        return;
    }

    const requestData = {
        'nombre': nombre
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
        throw new Error(data.error);
    }

    openAlert('Empresas', data.message);
    setTimeout(() => {
        window.location.reload();
    }, 1300)
    } catch(e) {
        openAlert('Empresas', data.error);
        console.error(e);
    } finally {
        setSearching(false);
    }
}

async function eliminar_empresa(id) {
    if (isSearching) return;
    setSearching(true);
    const url = `/inces/mod_empresa/${id}`

    const confirm = await openConfirm('INCES' , '¿Estás seguro de que quieres eliminar la empresa?')
    if (confirm) {
        try {
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error);
            }

            openAlert('Empresas', data.message);
            window.location.reload();
        } catch(e) {
            openAlert('Empresas', data.error);
            console.error(e);
        } finally {
            setSearching(false);
        }
    }
}

function obtenerDataEditEmpresa(id, empresa) {
    const form = document.getElementById('edit-empresa-form');
    form.setAttribute('idEmpresa', id);
    const input = document.getElementById('edit-nombreEmpresa');
    input.value = empresa;
}
// FRONT END 

function generar_factura() {
    const cliente = document.getElementById('nombreFactura').value.trim();
    const cedula = document.getElementById('cedulaFactura').value.trim();
    const direccion = document.getElementById('direccionFactura').value.trim();
    const telefono = document.getElementById('telefonoFactura').value.trim();
    const total = document.getElementById('total-factura').textContent;

    document.getElementById('cliente-factura').textContent = cliente;
    document.getElementById('direccion-factura').textContent = direccion;
    document.getElementById('telefono-factura').textContent = telefono;
    document.getElementById('cedula-factura').textContent = cedula;
    document.getElementById('totalFactura').textContent = total;
}

function actualizarProductosArray(idProducto, nuevaCantidad) {
    const index = productosArray.findIndex(p => p.idProducto === idProducto);
    if (index !== -1) {
        productosArray[index].cantidadProducto = nuevaCantidad;
    } else {
        productosArray.push({
            idProducto: idProducto,
            cantidadProducto: nuevaCantidad
        });
    }

    console.log(productosArray)
}

function eliminarProductoArray(idProducto) {
    const index = productosArray.findIndex(p => p.idProducto.toString() === idProducto.toString());
    console.log(index)
    if (index !== -1) {
        productosArray.splice(index, 1);
        console.log(`Producto con ID ${idProducto} eliminado.`);
    } else {
        console.log(`Producto con ID ${idProducto} no encontrado.`);
    }
    
    console.log("Array actualizado:", productosArray);
}


function render_producto(data) {
    const tbody = document.getElementById('facturacion-tbody');
    const factura = document.getElementById('facturacion-body');
    const productos = document.querySelectorAll('.producto-tr');
    const precio = parseFloat(data.precio);
    const idProducto = data.idProducto.toString();
    let productoExistente = null;

    productos.forEach(element => {
        if (element.getAttribute('idProducto') === idProducto) {
            productoExistente = element;
        }
    });

    if (!productoExistente) {
        const productoHTML = `
            <tr id="producto-${idProducto}" class="producto-tr" idProducto="${idProducto}">
                <td><input type="text" class="codigo" value="${data.idProducto}" readonly></td>
                <td><input type="text" class="descripcion" value="${data.nombre}" readonly></td>
                <td><input type="number" id="cantidad-factura-${idProducto}" class="cantidad" min="1" value="1" onchange="calc_subtotal(${data.idProducto})"></td>
                <td><input type="number" class="precio" id="precio-factura-${data.idProducto}" step="0.01" min="0" value="${precio.toFixed(2)}" readonly></td>
                <td class="subtotal" id="subTotal-${idProducto}">${precio.toFixed(2)}</td>
                <td><button class="eliminar" onclick="eliminar_producto_factura('${idProducto}')">✕</button></td>
            </tr>`;

        const facturaHtml = `<tr id="facturación-item-${idProducto}" idProducto="${idProducto} class="producto-tr">
                                <td>${data.nombre}</td>
                                <td id="cantidad-facturacion-${idProducto}">1</td>
                                <td id="precio-facturacion-${data.idProducto}">${precio.toFixed(2)}</td>
                                <td id="subtotal-facturacion-${data.idProducto}">${precio.toFixed(2)}</td>
                            </tr>`
        
        tbody.insertAdjacentHTML('beforeend', productoHTML);
        factura.insertAdjacentHTML('beforeend', facturaHtml);
        actualizarProductosArray(data.idProducto, 1);
    } else {
        const cantidadInput = productoExistente.querySelector(`#cantidad-factura-${idProducto}`);
        let cantidad = parseInt(cantidadInput.value) + 1;
        cantidadInput.value = cantidad;
        
        const subtotal = precio * cantidad;
        productoExistente.querySelector(`#subTotal-${idProducto}`).textContent = subtotal.toFixed(2);

        actualizarProductosArray(data.idProducto, cantidad);
    }

        calc_total();
}

function eliminar_producto_factura(id) {
    const producto = document.getElementById(`facturación-item-${id}`);
    const productoFactura = document.getElementById(`producto-${id}`);
    const total = parseFloat(document.getElementById('total-factura').textContent);
    const subTotal = parseFloat(document.getElementById(`subTotal-${id}`).textContent);
    const newSubTotal = total - subTotal;
    producto.remove();
    productoFactura.remove();
    document.getElementById('total-factura').textContent = newSubTotal.toFixed(2);

    eliminarProductoArray(id);
}

function calc_total() {
    let total = 0
    const tdSubTotal = document.querySelectorAll('.subtotal');

    tdSubTotal.forEach((element) => {
        total += parseFloat(element.textContent)
    })
    document.getElementById('total-factura').textContent = total.toFixed(2);
}

function calc_subtotal(id) {
    const subTotal = document.getElementById(`subTotal-${id}`);
    const subtTotalFactura = document.getElementById(`subtotal-facturacion-${id}`);
    let cantidad = parseInt(document.getElementById(`cantidad-factura-${id}`).value.trim());
    const precio = parseFloat(document.getElementById(`precio-factura-${id}`).value.trim());

    if (cantidad <= 0) {
        openAlert('Inventario', 'La cantidad no puede ser igual o menor a 0');
        cantidad = 1;
        document.getElementById(`cantidad-factura-${id}`).value = 1;
    }
    const newSubtotal = cantidad * precio;

    document.getElementById(`cantidad-facturacion-${id}`).textContent = cantidad;

    subTotal.textContent = newSubtotal.toFixed(2);
    subtTotalFactura.textContent = newSubtotal.toFixed(2);
    actualizarProductosArray(id, cantidad)
    calc_total();
}

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
    let container = document.getElementById('inscripcion-options__container');
    if (container == null) container = document.getElementById('inces-insc__wrapper');

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
        id.value = data.idusuarios;
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
        openAlert('Inscripción', 'Error al mostrar secciones');
    }
}

function mostrar_horario(data) {
    document.getElementById('horario__container').style.display = 'block';
    limpiar_horario();
    limpiar_horario_read_only();
    
    if (!data || !data.length) return;

    const dias = {
        'Lunes': 1, 'Martes': 2, 'Miercoles': 3, 
        'Jueves': 4, 'Viernes': 5, 'Sabado': 6
    };

    const horas = {
        '08:00:00': 1, '09:00:00': 2, '10:00:00': 3, '11:00:00': 4,
        '12:00:00': 5, '13:00:00': 6, '14:00:00': 7, '15:00:00': 8,
        '16:00:00': 9, '17:00:00': 10
    };

    const tabla = document.getElementById('tabla-horario');
    
    // LIMPIAR el array completamente antes de cargar
    horariosSeleccionados.length = 0;
    
    data.forEach(element => {
        const dia = element.horario_dia;
        const horaInicio = element.horario_hora;
        const horaFin = element.horario_hora_final;
        const nombreCurso = element.nombre_curso || 'Curso';
        const idHorario = element.idhorario;
        const aula = element.horario_aula;
        const color = getRandomColor();

        const inicioNumeros = horaInicio.replace(/:00:00$/, '').replace(/^0/, '');
        const finNumeros = horaFin.replace(/:00:00$/, '').replace(/^0/, '');
        
        const filaInicio = horas[horaInicio];
        const filaFin = horas[horaFin];
        const columnaDia = dias[dia];
        
        if (columnaDia && filaInicio && filaFin) {
            for (let i = filaInicio; i < filaFin; i++) {
                const fila = tabla.rows[i];
                if (fila && fila.cells[columnaDia]) {
                    const celda = fila.cells[columnaDia];
                    celda.innerHTML = `${nombreCurso}<br>${aula}`;
                    celda.classList.add('horario-curso');
                    celda.style.backgroundColor = color;
                }
            }
        }

        // ESTRUCTURA CONSISTENTE: Siempre incluir celdaId Y horario
        if (document.getElementById('editSeccion')) {
            const celdaId = `columna-${dia.toLowerCase()}-${inicioNumeros}-${finNumeros}`;
            
            horariosSeleccionados.push({
                celdaId: celdaId,
                dia: dia,
                horaInicio: horaInicio,
                horaFin: horaFin,
                curso: nombreCurso,
                seccion: document.getElementById('editSeccion').value.trim(),
                color: color,
                horario_aula: aula,
                horario: idHorario  // ← Incluir el ID del horario también
            });
        }
    });
    
    console.log('📊 Horarios cargados:', horariosSeleccionados);
}

function limpiar_horario() {
    // Eliminar elementos undefined/null y duplicados
    const horariosLimpios = [];
    const celdasVistas = new Set();
    
    horariosSeleccionados.forEach(item => {
        if (item && item.celdaId && !celdasVistas.has(item.celdaId)) {
            horariosLimpios.push(item);
            celdasVistas.add(item.celdaId);
        }
    });
    
    horariosSeleccionados.length = 0;
    horariosSeleccionados.push(...horariosLimpios);
    
    console.log('Array limpiado:', horariosSeleccionados);
}

function limpiar_horario_read_only() {
    const tabla = document.getElementById('tabla-horario');
    
    // Reiniciar todas las celdas del horario
    for (let i = 1; i < tabla.rows.length; i++) {
        const fila = tabla.rows[i];
        for (let j = 1; j < fila.cells.length; j++) {
            const celda = fila.cells[j];
            celda.textContent = '';
            celda.style.backgroundColor = 'transparent';
            celda.classList.remove('horario-curso');
        }
    }
}


function getRandomColor() {
    const colors = ['#FFD700', '#98FB98', '#ADD8E6', '#FFB6C1', '#E6E6FA', '#FFA07A', '#90EE90', '#87CEFA', '#FFC0CB'];
    return colors[Math.floor(Math.random() * colors.length)];
}

let horariosSeleccionados = [];
function select_horario(idCelda, nombreCurso) {
    const celda = document.getElementById(idCelda);
    if (!celda) return;

    // DETECCIÓN MEJORADA
    const yaEstaSeleccionada = celda.innerHTML.trim() !== '' && celda.style.backgroundColor !== '';
    
    console.log(`🔄 Celda: ${idCelda}, Seleccionada: ${yaEstaSeleccionada}`);
    
    if (!yaEstaSeleccionada) {
        // SELECCIONAR
        const seccion = (document.getElementById('crearSeccion')?.value.trim() || 
                        document.getElementById('editSeccion')?.value.trim()) || 'Sin sección';
        const aula = (document.getElementById('aulaSeccion')?.value.trim() || 
                      document.getElementById('editAulaSeccion')?.value.trim()) || 'Sin aula';
        const color = getRandomColor();
        const dia = celda.getAttribute('data-dia');
        const horaInicio = celda.getAttribute('data-hora-inicio');
        const horaFin = celda.getAttribute('data-hora-fin');

        celda.style.backgroundColor = color;
        celda.innerHTML = `${nombreCurso}<br>${seccion}<br><small>${aula}</small>`;
        celda.classList.add('horario-seleccionado');

        // ELIMINAR cualquier elemento existente con este celdaId (incluyendo undefined)
        const indicesAEliminar = [];
        horariosSeleccionados.forEach((item, index) => {
            if (item && item.celdaId === celda.id) {
                indicesAEliminar.push(index);
            }
        });
        indicesAEliminar.sort((a, b) => b - a).forEach(index => {
            console.log(index == celda.id)
        });

        
        // Eliminar en orden descendente para no afectar índices
        indicesAEliminar.sort((a, b) => b - a).forEach(index => {
            horariosSeleccionados.splice(index, 1);
        });

        // AGREGAR nuevo elemento
        horariosSeleccionados.push({
            celdaId: celda.id,
            dia: dia,
            horaInicio: horaInicio,
            horaFin: horaFin,
            curso: nombreCurso,
            seccion: seccion,
            color: color,
            horario_aula: aula,
            horario: null  // Para nuevos horarios, no hay ID todavía
        });
        
        console.log('✅ Seleccionada:', celda.id);
        
    } else {
        // DESELECCIONAR
        celda.style.backgroundColor = '';
        celda.innerHTML = '';
        celda.classList.remove('horario-seleccionado');
        
        // ELIMINAR - Buscar por celdaId y eliminar SOLO ese elemento
        let indicesAEliminar = [];

        if (horariosSeleccionados.length == 1) {
            horariosSeleccionados = [];
        } else {
            horariosSeleccionados.forEach((item, index) => {
                console.log('ITEM: ' + item.celdaId)
                console.log('CELDA OBTENIDA: ' + celda.id);
                if (item.celdaId === celda.id) {
                    console.log('ITEM: ' + item.celdaId)
                    console.log('CELDA OBTENIDA: ' + celda.id);
                    console.log('index: ' + index)
                    indicesAEliminar.push(index);
                }
            });

            if (indicesAEliminar.length > 0) {
                // DESELECCIONAR
                celda.style.backgroundColor = '';
                celda.innerHTML = '';
                celda.classList.remove('horario-seleccionado');
            }

            console.log('indices: ' + indicesAEliminar);
            
            // Eliminar en orden descendente
            indicesAEliminar.sort((a, b) => b - a).forEach(index => {
                horariosSeleccionados.splice(index, 1);
            });
        }
        
        console.log('❌ Deseleccionada:', celda.id);
    }
    
    // LOG MEJORADO - Filtrar elementos undefined
    const horariosValidos = horariosSeleccionados.filter(item => item !== undefined && item !== null);
    console.log('📊 Horarios actuales:', horariosValidos.map(h => h.celdaId));
    console.log('🔍 Array completo:', horariosValidos);
}
let flagNotas = false

function toggleInputNotas() {
    const input = document.querySelectorAll('.mod-calificacion')
    const btn = document.getElementById('toggle-calificacion');
    const estado = !flagNotas;
    let border = '';

    input.forEach((element) => {
        if (element.classList.contains('dark-mode')) {
            border = '1px solid #fff';
        } else {
            border = '1px solid #333'
        }
    })
    
    if (flagNotas === false) {
        alert('Podra modificar las calificaciones de cada alumno');
        btn.textContent = 'Desactivar modificación';
    } else {
        alert('Se desactiva la modificación de calificaciones');
        btn.textContent = 'Activar modificación';
    }
    
    input.forEach((element) => {
        if (flagNotas === false) {
            element.removeAttribute('readonly');
            element.style.border = border;

        } else if (flagNotas === true) {
            element.setAttribute('readonly', true);
            element.style.border = 'none';
        }
    })

    flagNotas = estado;
}

function validarTecla(event) {
    const charCode = event.which ? event.which : event.keyCode;
    const charStr = String.fromCharCode(charCode);
    
    // Permitir solo letras y espacios
    return /[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/.test(charStr);
}

function changeFilterNumber() {
    const value = document.getElementById('cantidad-secciones').value.trim();
    const radio1 = document.getElementById('filtrar-mayor-label');
    const radio2 = document.getElementById('filtrar-menor-label');
    const radio3 = document.getElementById('filtrar-igual-label');

    if (value != null && typeof(value) != 'undefined') {
        radio1.textContent = `Filtrar por secciones con mas de ${value} participantes`;
        radio2.textContent = `Filtrar por secciones con menos de ${value} participantes`;
        radio3.textContent = `Filtrar por secciones con ${value} participantes`;
    }
}

function validarStatusInsc(id) {
    const btn = document.getElementById(`btn-status-${id}`)
    const status = btn.getAttribute('status');
    btn.classList.remove(status == '1' ? 'btn-danger' : 'btn-success');
    btn.textContent = status == true ? 'Activa' : 'Inactiva';
    const clase = status == '1' ? 'btn-success' : 'btn-danger';
    btn.classList.add(clase);
}