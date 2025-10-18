const getCalificaciones = async () => {
    if (isSearching) return;
    setSearching(true);
    const url = '/alumnos/calificaciones';
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

        return data.calificaciones;
    } catch(e) {
        console.error(e);
    } finally {
        setSearching(false);
    }
}

// Función para crear una card de curso
function crearCardCurso(curso) {
    const card = document.createElement('div');
    card.className = 'curso-card';
    card.dataset.id = curso.id;
    
    // Determinar clase de color según la calificación
    const claseCalificacion = curso.definitiva >= 14 ? 'calificacion-aprobada' : 'calificacion-reprobada';
    
    card.innerHTML = `
        <div class="curso-header">
            <div class="curso-info">
                <h3 class="curso-nombre">${curso.nombre_curso}</h3>
                <div class="curso-detalles">
                    <div>Sección: ${curso.seccion}</div>
                    <div>Periodo: ${curso.fecha_inscripcion}---${curso.fecha_expiracion}</div>
                    <div class="curso-profesor">
                        <i class="fas fa-chalkboard-teacher"></i>
                        <span>${curso.nombre} ${curso.apellido}</span>
                    </div>
                </div>
            </div>
            <div class="calificacion-circulo ${claseCalificacion}">
                ${curso.definitiva.toFixed(1)}
            </div>
            <div class="expand-indicator ms-3">
                <i class="fas fa-chevron-down"></i>
            </div>
        </div>
        <div class="curso-detalle">
            <div class="detalle-contenido">
                <h5 class="mb-3">Detalle de Calificaciones</h5>
                <table class="tabla-calificaciones">
                    <thead>
                        <tr>
                            <th>Logro</th>
                            <th>Calificación</th>
                            <th>Porcentaje</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                Logro 1
                            </td>
                            <td>
                                ${curso.logro_1.toFixed(1)}
                            </td>
                            <td>20%</td>
                        </tr>

                        <tr>
                            <td>
                                Logro 2
                            </td>
                            <td>
                                ${curso.logro_2.toFixed(1)}
                            </td>
                            <td>20%</td>
                        </tr>

                        <tr>
                            <td>
                                Logro 3
                            </td>
                            <td>
                                ${curso.logro_3.toFixed(1)}
                            </td>
                            <td>20%</td>
                        </tr>

                        <tr>
                            <td>
                                Logro 1
                            </td>
                            <td>
                                ${curso.logro_4.toFixed(1)}
                            </td>
                            <td>20%</td>
                        </tr>

                        <tr>
                            <td>
                                Logro 1
                            </td>
                            <td>
                                ${curso.logro_5.toFixed(1)}
                            </td>
                            <td>20%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    return card;
}

// Función para inicializar el dashboard
async function inicializarDashboard() {
    const container = document.getElementById('cursos-container');
    cursosData = await getCalificaciones();
    
    // Crear y agregar cards para cada curso
    cursosData.forEach(curso => {
        const card = crearCardCurso(curso);
        container.appendChild(card);
    });
    
    // Agregar event listeners para expandir/contraer
    document.querySelectorAll('.curso-header').forEach(header => {
        header.addEventListener('click', function() {
            const card = this.closest('.curso-card');
            const detalle = card.querySelector('.curso-detalle');
            const indicator = card.querySelector('.expand-indicator');
            
            // Cerrar otros detalles abiertos
            document.querySelectorAll('.curso-detalle.expandido').forEach(d => {
                if (d !== detalle) {
                    d.classList.remove('expandido');
                    d.previousElementSibling.querySelector('.expand-indicator').classList.remove('rotated');
                }
            });
            
            // Alternar el estado actual
            detalle.classList.toggle('expandido');
            indicator.classList.toggle('rotated');
        });
    });
}

// Inicializar el dashboard cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', inicializarDashboard);