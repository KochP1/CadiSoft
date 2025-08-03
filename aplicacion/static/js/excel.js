function excel() {
    const reportes = document.getElementById('tablaAlumnos');
    let tableExport = new TableExport(reportes, {
        exportButtons: false,
        filename: "Prueba",
        sheetname: "Tabla",
    });

    let datos = tableExport.getExportData();
    let pref = datos.tablaAlumnos.xlsx;
    tableExport.export2file(
            pref.data,
            pref.mimetype,
            pref.filename,
            pref.fileExtension,
            pref.merges,
            pref.RTL,
            pref.sheetname
        );
    window.location.reload();
}

function migrarExcel() {

    const btnsTabla = document.querySelectorAll('.tabla-btn')

    for (let i = 0; i < btnsTabla.length; i++) {
        btnsTabla[i].remove();
    }

    excel()
}

function imprimirReporte() {
    const btnsTabla = document.querySelectorAll('.tabla-btn');
    const menu = document.querySelectorAll('.alumnos-options__container');

    btnsTabla.forEach((element) => {
        element.remove();
    })

    menu.forEach((element) => {
        element.remove();
    })

    window.print();
    window.location.reload();
}

function imprimirFactura() {
    const facturaContainer = document.querySelector('#factura-modal .factura__container');
    const facturaClon = facturaContainer.cloneNode(true);
    
    const ventanaImpresion = window.open('', '_blank', 'width=800,height=600');
    
    ventanaImpresion.document.open();
    ventanaImpresion.document.write(`
        <html>
            <head>
                <title>Factura</title>
                <style>
                    @media print {
                        body {
                            font-family: sans-serif;
                            margin: 0;
                            width: 400px;
                            height: max-content;
                        }
                        .factura__container {
                            width: 96%;
                            height: max-content;
                            display: flex;
                            flex-direction: column;
                            border-radius: 4px;
                            padding: 20px;
                        }

                        .factura-presentacion__container {
                            width: 100%;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            gap: 10px;
                        }

                        .logo-factura__container {
                            width: 50px;
                            height: 50px;
                        }

                        .logo-factura__container img {
                            width: 100%;
                            height: 100%;
                        }

                        .factura-presentacion__container h2 {
                            margin: 0;
                            font-size: 1.6rem;
                            font-weight: bold;
                        }

                        .factura-presentacion__container h3 {
                            margin: 0;
                            font-size: 1.3rem;
                            font-weight: bold;
                        }

                        .factura-info__container {
                            width: 100%;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                        }

                        .factura-info {
                            width: 100%;
                            display: flex;
                            align-items: center;
                            justify-content: start;
                            padding-left: 10px;
                            gap: 5px;
                        }

                        .factura-info h3, .factura-info span {
                            margin: 0;
                            font-size: 1rem;
                        }

                        .factura-info h3 {
                            font-weight: bold;
                        }

                        .tabla-factura {
                            width: 100%;
                            border-collapse: collapse;
                            font-family: Arial, sans-serif;
                        }
                            
                        .tabla-factura th {
                            padding-bottom: 8px;
                            text-align: left;
                            border-bottom: 1px solid #ddd;
                        }
                            
                        .tabla-factura td {
                            padding: 6px 0;
                        }
                            
                        .tabla-factura tr:not(:first-child) td {
                            padding-top: 8px; /* Espacio adicional después de los encabezados */
                        }

                        .factura-total__container {
                            width: 100%;
                            display: flex;
                            justify-content: end;
                            align-items: center;
                            padding-right: 10px;
                            gap: 5px;
                        }

                        .factura-total__container h3, .factura-total__container span {
                            margin: 0;
                            font-size: 1rem;
                        }

                        .factura-total__container h3 {
                            font-weight: bold;
                        }

                        .separador-factura {
                            border: none;
                            border-top: 3px dashed #000;
                            height: 1px;
                            margin: 10px 0;   
                        }

                        .agadecimiento-compra {
                            font-size: 1.3rem;
                            font-weight: bold;
                            display: flex;
                            margin: auto;
                        }

                        @page {
                            size: 400px 700px;
                            margin: 10mm;
                        }
                    }
                </style>
            </head>
            <body>
                ${facturaClon.outerHTML}
                <script>
                    // Imprimir automáticamente cuando se cargue la ventana
                    window.onload = function() {
                        setTimeout(function() {
                            window.print();
                            window.close();
                        }, 200);
                    };
                </script>
            </body>
        </html>
    `);
    ventanaImpresion.document.close();
}