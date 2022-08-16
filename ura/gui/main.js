// Imports
const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const { PythonShell } = require('python-shell');
const path = require("path");
const EventEmitter = require('events');
const fs = require('fs');

// Constants
const secretRe = /c0VjUmVUX2NPZEUgYnkgd2hpX25l: (.+)/msg;
const pythonPath = ""
const scriptPath = "ura"
const po = {
    mode: 'text',
    pythonPath: pythonPath,
    pythonOptions: ['-u'],
    scriptPath: scriptPath,
    args: []
};

// Modal Functions
Date.prototype.timeNow = function () {
    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes() + ":" + ((this.getSeconds() < 10) ? "0" : "") + this.getSeconds() + "." + ((this.getMilliseconds() < 10) ? "00" : ((this.getMilliseconds() < 100) ? "0" : "")) + this.getMilliseconds();
}

// Derived Constants
const env = process.env.NODE_ENV || "production";
const loadingEvents = new EventEmitter()
const userDataPath = app.getPath('userData')
const logPath = path.join(userDataPath, 'log.txt');
const pyshell = new PythonShell('gui.py', po);

// Variable Init
var init = false;

// Functions

function log(...args) {
    console.log(...args)
}

function quit() {
    pyshell.childProcess.kill('SIGINT');
}

// App Init
app.whenReady().then(() => {
    // Init
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            nodeIntegration: true,
            contextIsolation: false,
        },
        autoHideMenuBar: true,
        backgroundColor: '#151723',
    });

    mainWindow.loadFile(path.join(__dirname, "loading.html"));

    if (env === 'development') {
        mainWindow.webContents.openDevTools()
    }

    // Event Listeners
    loadingEvents.on('finished', () => {
        mainWindow.loadFile(path.join(__dirname, "index.html"));
    })

    mainWindow.webContents.on('new-window', (event, url) => {
        event.preventDefault();
        require('electron').shell.openExternal(url);
    })

    ipcMain.on('logPath', function (event, arg) {
        event.sender.send('logPath', logPath);
    });

    ipcMain.on('cds', function (event, arg) {
        dialog.showOpenDialog(mainWindow, {
            properties: ['openDirectory']
        }).then(result => {
            if (!result.canceled) {
                event.sender.send('cdr', result.filePaths[0]);
            }
        }).catch(err => {
            log(err)
        })
    });
});

// Event Listeners
/// Python Shell
pyshell.on('message', function (message) {
    if (init == false) {
        var m = secretRe.exec(message)
        if (m !== null && m[1] === "Connected") {
            init = true;
            loadingEvents.emit('finished')
            log(m[1]);
            return;
        }
    }
    log(message);
});

pyshell.on('stderr', function (stderr) {
    log(stderr);
});

/// Electron
app.on("window-all-closed", function () {
    quit();
    app.quit();
});

app.on("quit", function () {
    quit();
    app.quit();
});