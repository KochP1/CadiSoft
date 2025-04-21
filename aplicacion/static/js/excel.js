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