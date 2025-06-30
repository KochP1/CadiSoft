const { app, BrowserWindow, globalShortcut } = require('electron')
const path = require('path')

const createWindow = () => {
    const window = new BrowserWindow({
        width: 1200,
        height: 720,
        webPreferences: {
            nodeIntegration: true
        }
    })

    window.setMenuBarVisibility(false)
    window.loadURL('http://127.0.0.1:5000/')

    // Atajos de teclado globales
    globalShortcut.register('Alt+Left', () => {
        if (window.webContents.canGoBack()) {
            window.webContents.goBack()
        }
    })

    globalShortcut.register('Alt+Right', () => {
        if (window.webContents.canGoForward()) {
            window.webContents.goForward()
        }
    })
}

app.whenReady().then(() => {
    createWindow()
})

// Limpiar atajos al cerrar
app.on('will-quit', () => {
    globalShortcut.unregisterAll()
})
// npm install electron --save-dev