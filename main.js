const { app, BrowserWindow } = require('electron')
const path = require('path');
// Habilitar la carga de URL externas
app.commandLine.appendSwitch('disable-web-security');
app.commandLine.appendSwitch('ignore-certificate-errors');

const createWindow =  () => {
    const window = new BrowserWindow({
        width: 1200,
        height: 720
    })

    window.setMenuBarVisibility(false);
    window.loadURL('http://127.0.0.1:5000/')
}

app.whenReady().then(() => {
    createWindow()
  })

// npm install electron --save-dev