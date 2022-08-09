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

app.whenReady().then(() => {
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

    mainWindow.once('ready-to-show', () => {
        mainWindow.loadFile(path.join(__dirname, "index.html"));
    })

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

    mainWindow.once('ready-to-show', () => {
        mainWindow.show()
    })
});

function quit() {
    pyshell.childProcess.kill('SIGINT');
}

app.on("window-all-closed", function () {
    quit();
    app.quit();
});

app.on("quit", function () {
    quit();
    app.quit();
});