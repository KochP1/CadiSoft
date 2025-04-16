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

// Crear profesor

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
    const especialidad = document.getElementById('departamentoProfesor').value;

    if (especialidad == '') {
        alert('Debe escoger una especialidad')
    }
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('/profesores/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nombre: nombre,
                    segundoNombre: segundoNombre,
                    apellido: apellido,
                    segundoApellido: segundoApellido,
                    cedula: cedula,
                    email: email,
                    contraseña: contraseña,
                    rol: rol,
                    especialidad: especialidad
                })
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