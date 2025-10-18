// Datos de ejemplo - En un caso real, estos vendrían de una API
const cursosData = [
    {
        id: 1,
        nombre: "Matemáticas Avanzadas",
        seccion: "A",
        profesor: "Dr. Carlos Rodríguez",
        definitiva: 18.5,
        logros: [
            { nombre: "Logro 1: Fundamentos", calificacion: 19, porcentaje: 20 },
            { nombre: "Logro 2: Álgebra Lineal", calificacion: 18, porcentaje: 20 },
            { nombre: "Logro 3: Cálculo Diferencial", calificacion: 17, porcentaje: 20 },
            { nombre: "Logro 4: Cálculo Integral", calificacion: 19, porcentaje: 20 },
            { nombre: "Logro 5: Aplicaciones", calificacion: 20, porcentaje: 20 }
        ]
    },
    {
        id: 2,
        nombre: "Programación Web",
        seccion: "B",
        profesor: "Ing. María González",
        definitiva: 16.2,
        logros: [
            { nombre: "Logro 1: HTML y CSS", calificacion: 18, porcentaje: 20 },
            { nombre: "Logro 2: JavaScript Básico", calificacion: 16, porcentaje: 20 },
            { nombre: "Logro 3: JavaScript Avanzado", calificacion: 15, porcentaje: 20 },
            { nombre: "Logro 4: Frameworks Frontend", calificacion: 16, porcentaje: 20 },
            { nombre: "Logro 5: Proyecto Final", calificacion: 16, porcentaje: 20 }
        ]
    },
    {
        id: 3,
        nombre: "Base de Datos",
        seccion: "C",
        profesor: "Lic. Ana Martínez",
        definitiva: 14.8,
        logros: [
            { nombre: "Logro 1: Modelado de Datos", calificacion: 15, porcentaje: 20 },
            { nombre: "Logro 2: SQL Básico", calificacion: 16, porcentaje: 20 },
            { nombre: "Logro 3: SQL Avanzado", calificacion: 14, porcentaje: 20 },
            { nombre: "Logro 4: Normalización", calificacion: 13, porcentaje: 20 },
            { nombre: "Logro 5: Proyecto de BD", calificacion: 16, porcentaje: 20 }
        ]
    },
    {
        id: 4,
        nombre: "Redes de Computadoras",
        seccion: "A",
        profesor: "MSc. Luis Fernández",
        definitiva: 17.3,
        logros: [
            { nombre: "Logro 1: Fundamentos de Redes", calificacion: 18, porcentaje: 20 },
            { nombre: "Logro 2: Protocolos TCP/IP", calificacion: 17, porcentaje: 20 },
            { nombre: "Logro 3: Enrutamiento", calificacion: 16, porcentaje: 20 },
            { nombre: "Logro 4: Seguridad en Redes", calificacion: 18, porcentaje: 20 },
            { nombre: "Logro 5: Proyecto de Red", calificacion: 18, porcentaje: 20 }
        ]
    }
];

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
                <h3 class="curso-nombre">${curso.nombre}</h3>
                <div class="curso-detalles">
                    <div>Sección: ${curso.seccion}</div>
                    <div class="curso-profesor">
                        <i class="fas fa-chalkboard-teacher"></i>
                        <span>${curso.profesor}</span>
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
                        ${curso.logros.map(logro => `
                            <tr>
                                <td>${logro.nombre}</td>
                                <td class="${logro.calificacion >= 14 ? 'calificacion-aprobada' : 'calificacion-reprobada'}">
                                    ${logro.calificacion.toFixed(1)}
                                </td>
                                <td>${logro.porcentaje}%</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    return card;
}

// Función para inicializar el dashboard
function inicializarDashboard() {
    const container = document.getElementById('cursos-container');
    
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