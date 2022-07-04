// Imports
const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const { PythonShell } = require('python-shell');
const path = require("path");

// Constants
const pythonPath = ""
const scriptPath = "ura"
const po = {
    mode: 'text',
    pythonPath: pythonPath,
    pythonOptions: ['-u'],
    scriptPath: scriptPath,
    args: []
};

// Derived Constants
const env = process.env.NODE_ENV || "production";

// Python Init
const pyshell = new PythonShell('gui.py', po);
pyshell.on('message', function (message) {
    console.log(message);
});
pyshell.on('stderr', function (stderr) {
    console.log(stderr);
});

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            nodeIntegration: true,
            contextIsolation: false,
        },
        autoHideMenuBar: true,
    });

    mainWindow.loadFile(path.join(__dirname, "index.html"));

    mainWindow.webContents.on('new-window', (event, url) => {
        event.preventDefault();
        require('electron').shell.openExternal(url);
    })

    if (env === 'development') {
        mainWindow.webContents.openDevTools()
    }

    ipcMain.on('cds', function (event, arg) {
        dialog.showOpenDialog(mainWindow, {
            properties: ['openDirectory']
        }).then(result => {
            if (!result.canceled) {
                event.sender.send('cdr', result.filePaths[0]);
            }
        }).catch(err => {
            console.log(err)
        })
    });
}

function quit() {
    pyshell.end(function (err, code, signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
    });
}

app.whenReady().then(() => {
    createWindow();
});

app.on("window-all-closed", function () {
    quit();
    app.quit();
});

app.on("quit", function () {
    quit();
    app.quit();
});