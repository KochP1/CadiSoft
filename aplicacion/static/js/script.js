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
        alert('Debe ingresar el correo electrónico')
        return;
    }

    if (cedula.length > 8) {
        alert('La cédula puede tener máximo 8 caracteres')
        window.location.reload();
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
