const { app, BrowserWindow } = require('electron');
const path = require('path');
const { exec } = require('child_process');

let mainWindow;

function createWindow() {
    // Crear la ventana principal
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    // Cargar la aplicación Flask
    mainWindow.setMenuBarVisibility(false); // Esto ocultará la barra de menú
    mainWindow.loadURL('http://localhost:5000');  // Cambia el puerto si es necesario

    // Abrir las herramientas de desarrollo (opcional)
    // mainWindow.webContents.openDevTools();

    // Manejar el cierre de la ventana
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// Iniciar la aplicación Flask cuando Electron esté listo
app.on('ready', () => {
    // Ejecutar el servidor Flask
    exec('python3 run.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error al iniciar Flask: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Error en Flask: ${stderr}`);
            return;
        }
        console.log(`Flask iniciado: ${stdout}`);
    });

    // Crear la ventana de Electron
    createWindow();
});

// Salir cuando todas las ventanas estén cerradas
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

// npm install electron --save-dev