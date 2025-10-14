// REPORTES CARGA DE TRABAJO PROFESORES

// Variables globales
let cargaTrabajoChart = null;
let profesorActual = null;
let datosCarga = null;

// Datos ficticios para demostración
const datosFicticios = {
    1: { // ID del profesor
        nombre: "Juan Pérez",
        secciones: [
            { curso: "Matemáticas I", seccion: "A", horas: 6 },
            { curso: "Matemáticas I", seccion: "B", horas: 6 },
            { curso: "Física II", seccion: "A", horas: 4 },
            { curso: "Cálculo", seccion: "C", horas: 8 }
        ]
    },
    2: {
        nombre: "María García",
        secciones: [
            { curso: "Química I", seccion: "A", horas: 5 },
            { curso: "Química I", seccion: "B", horas: 5 },
            { curso: "Biología", seccion: "A", horas: 6 }
        ]
    },
    3: {
        nombre: "Carlos López",
        secciones: [
            { curso: "Programación", seccion: "A", horas: 8 },
            { curso: "Base de Datos", seccion: "A", horas: 6 },
            { curso: "Redes", seccion: "B", horas: 4 },
            { curso: "Sistemas", seccion: "A", horas: 6 }
        ]
    }
};

const dataProfesor = async (id) => {
    try {
        const url = `/profesores/carga_profesor/${id}`;

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

        return data;

    } catch(e) {
        console.error(e);
        return null;
    }
}

async function mostrarCargaTrabajo(profesorId, nombreProfesor, profesorApellido) {
    profesorActual = profesorId;
    
    const datosReales = await dataProfesor(profesorId);
    
    datosCarga = {
        nombre: nombreProfesor,
        apellido: profesorApellido,
        secciones: datosReales.secciones,
        metricas: datosReales.metricas
    };
    
    // Actualizar título del modal
    document.getElementById('modalTitulo').textContent = `Carga de trabajo - ${datosCarga.nombre} ${datosCarga.apellido}`;
    
    // Actualizar métricas
    actualizarMetricas();
    
    // Crear o actualizar gráfico
    crearGraficaCargaTrabajo();
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('reporte-modal'));
    modal.show();
}

// Función para actualizar las métricas
function actualizarMetricas() {
    let totalSecciones, totalHoras, promedioHoras;

    // Si tenemos métricas del backend, usarlas
    if (datosCarga.metricas) {
        totalSecciones = datosCarga.metricas.total_secciones;
        totalHoras = datosCarga.metricas.total_horas;
        promedioHoras = datosCarga.metricas.promedio_horas_seccion;
    } else {
        // Calcular desde los datos ficticios
        totalSecciones = datosCarga.secciones.length;
        totalHoras = datosCarga.secciones.reduce((sum, seccion) => sum + seccion.horas, 0);
        promedioHoras = totalSecciones > 0 ? (totalHoras / totalSecciones).toFixed(1) : 0;
    }

    document.getElementById('total-secciones').textContent = totalSecciones;
    document.getElementById('total-horas').textContent = totalHoras;
}

// Función para crear el gráfico de carga de trabajo
function crearGraficaCargaTrabajo() {
    const ctx = document.getElementById('cargaTrabajoChart').getContext('2d');
    
    // Destruir gráfico anterior si existe
    if (cargaTrabajoChart) {
        cargaTrabajoChart.destroy();
    }

    const labels = datosCarga.secciones.map(seccion => 
        `${seccion.curso} - Sección ${seccion.seccion}`
    );

    const datosSecciones = datosCarga.secciones.map(() => 1); // Cada sección cuenta como 1
    const datosHoras = datosCarga.secciones.map(seccion => seccion.horas || seccion.horas_semanales);

    cargaTrabajoChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Cantidad de Secciones',
                    data: datosSecciones,
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Horas de Clase',
                    data: datosHoras,
                    backgroundColor: 'rgba(255, 99, 132, 0.8)',
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Distribución de Carga de Trabajo',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                if (context.dataset.label === 'Cantidad de Secciones') {
                                    label += `${context.parsed.y} sección(es)`;
                                } else {
                                    label += `${context.parsed.y} hora(s)`;
                                }
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Secciones'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Cantidad de Secciones'
                    },
                    min: 0,
                    max: Math.max(...datosSecciones) + 1,
                    ticks: {
                        stepSize: 1
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Horas de Clase'
                    },
                    min: 0,
                    max: Math.max(...datosHoras) + 2,
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });

    // Mostrar solo secciones por defecto
    cambiarDataset('secciones');
}

// Función para cambiar entre datasets
function cambiarDataset(tipo) {
    if (!cargaTrabajoChart) return;

    const datasets = cargaTrabajoChart.data.datasets;
    
    switch(tipo) {
        case 'secciones':
            datasets[0].hidden = false;
            datasets[1].hidden = true;
            cargaTrabajoChart.options.scales.y1.display = false;
            break;
        case 'horas':
            datasets[0].hidden = true;
            datasets[1].hidden = false;
            cargaTrabajoChart.options.scales.y1.display = true;
            break;
        case 'ambos':
            datasets[0].hidden = false;
            datasets[1].hidden = false;
            cargaTrabajoChart.options.scales.y1.display = true;
            break;
    }

    cargaTrabajoChart.update();
}

// Función para descargar el gráfico
function descargarGraficaCarga() {
    if (!cargaTrabajoChart) return;

    const canvas = document.getElementById('cargaTrabajoChart');
    const enlace = document.createElement('a');
    enlace.href = canvas.toDataURL('image/png');
    enlace.download = `carga-trabajo-${datosCarga.nombre.replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.png`;
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
}

// FIN REPORTES CARGA DE TRABAJO PROFESORES

// GRAFICOS DE CALIFICACIONES E ASISTENCIAS VS INASISTENCIAS

let chartCalificaciones = null;
let chartAsistencias = null;

// Función para descargar una gráfica individual
function descargarGrafica(canvasId, nombreArchivo) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        alert('No se pudo encontrar la gráfica');
        return;
    }

    // Crear un enlace temporal para la descarga
    const enlace = document.createElement('a');
    
    // Convertir canvas a imagen PNG
    enlace.href = canvas.toDataURL('image/png');
    enlace.download = `${nombreArchivo}-${new Date().toISOString().split('T')[0]}.png`;
    
    // Simular click en el enlace
    document.body.appendChild(enlace);
    enlace.click();
    document.body.removeChild(enlace);
}

// Función para preparar datos de calificaciones
function prepararDatosCalificaciones() {
    const graficosWrapper = document.querySelector('.graficos__wrapper');
    const calificacionesJson = graficosWrapper.getAttribute('data-calificaciones');
    const calificaciones = JSON.parse(calificacionesJson);
    
    const definitivas = calificaciones.map(record => {
        return record.definitiva || 0;
    });

    const rangos = {
        '0-9': 0,
        '10-13': 0,
        '14-17': 0,
        '18-20': 0
    };

    definitivas.forEach(nota => {
        if (nota >= 0 && nota <= 9) rangos['0-9']++;
        else if (nota >= 10 && nota <= 13) rangos['10-13']++;
        else if (nota >= 14 && nota <= 17) rangos['14-17']++;
        else if (nota >= 18 && nota <= 20) rangos['18-20']++;
    });

    return {
        labels: Object.keys(rangos),
        datos: Object.values(rangos)
    };
}

// Función para preparar datos de asistencias vs inasistencias
function prepararDatosAsistencias() {
    const graficosWrapper = document.querySelector('.graficos__wrapper');
    const calificacionesJson = graficosWrapper.getAttribute('data-calificaciones');
    const calificaciones = JSON.parse(calificacionesJson);
    
    let totalAsistencias = 0;
    let totalInasistencias = 0;

    calificaciones.forEach(record => {
        totalAsistencias += record.asistencia || 0;
        totalInasistencias += record.inasistencia || 0;
    });

    return {
        totalAsistencias: totalAsistencias,
        totalInasistencias: totalInasistencias
    };
}

// Crear ambas gráficas cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Gráfica 1: Distribución de Calificaciones (Bar Chart)
    const datosCalificaciones = prepararDatosCalificaciones();
    const ctx1 = document.getElementById('calificacionesChart').getContext('2d');
    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: datosCalificaciones.labels,
            datasets: [{
                label: 'Cantidad de Estudiantes',
                data: datosCalificaciones.datos,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',    // Rojo para 0-9
                    'rgba(255, 205, 86, 0.7)',    // Amarillo para 10-13
                    'rgba(75, 192, 192, 0.7)',    // Verde claro para 14-17
                    'rgba(54, 162, 235, 0.7)'     // Azul para 18-20
                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(54, 162, 235)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: [
                        'Calificaciones Finales',
                        document.getElementById('curso-nombre').textContent, 
                        document.getElementById('periodo-seccion').textContent
                    ],
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Cantidad de Estudiantes'
                    },
                    ticks: {
                        stepSize: 1
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Rangos de Calificación'
                    }
                }
            }
        }
    });

    // Gráfica 2: Asistencias vs Inasistencias (Doughnut Chart)
    const datosAsistencias = prepararDatosAsistencias();
    const ctx2 = document.getElementById('asistenciasChart').getContext('2d');
    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Asistencias', 'Inasistencias'],
            datasets: [{
                data: [datosAsistencias.totalAsistencias, datosAsistencias.totalInasistencias],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.8)',  // Verde azulado para asistencias
                    'rgba(255, 99, 132, 0.8)'   // Rojo para inasistencias
                ],
                borderColor: [
                    'rgb(75, 192, 192)',
                    'rgb(255, 99, 132)'
                ],
                borderWidth: 2,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text:  [
                        'Asistencias vs Inasistencias',
                        document.getElementById('curso-nombre').textContent,
                        document.getElementById('periodo-seccion').textContent
                    ],
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = datosAsistencias.totalAsistencias + datosAsistencias.totalInasistencias;
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) + '%' : '0%';
                            return `${label}: ${value} (${percentage})`;
                        }
                    }
                }
            },
            cutout: '60%' // Hace el gráfico tipo anillo
        }
    });
});

// FIN GRAFICOS DE CALIFICACIONES E ASISTENCIAS VS INASISTENCIAS