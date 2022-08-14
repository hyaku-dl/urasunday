window.addEventListener("error", errorLog);

// Imports
const { ipcRenderer } = require('electron')
const { io } = require("socket.io-client");
const fs = require('fs');

// Constants
const modals = ["stg", "info"]

// Modal Functions
Date.prototype.timeNow = function () {
    return ((this.getHours() < 10) ? "0" : "") + this.getHours() + ":" + ((this.getMinutes() < 10) ? "0" : "") + this.getMinutes() + ":" + ((this.getSeconds() < 10) ? "0" : "") + this.getSeconds() + "." + ((this.getMilliseconds() < 10) ? "00" : ((this.getMilliseconds() < 100) ? "0" : "")) + this.getMilliseconds();
}

// Document Selectors
const eraseBtn = document.querySelector('#erase-input');
const dlBtn = document.querySelector('#dl-btn');
const input = document.querySelector('#input');
const ddir = document.querySelector("#ddir");
const cdir = document.querySelector("#cdir");
const owTgl = document.querySelector('#ow-tgl');
const modalArea = document.getElementById('modalArea');
const closeModal = document.getElementById('closeModal');
const modalBg = document.getElementById('modalBg');

for (let i of modals) {
    const iBtn = document.getElementById(`${i}Btn`);
    const iModal = document.getElementById(`${i}Modal`);

    iBtn.addEventListener('click', function () {
        modalArea.classList.add('is-show');
        iModal.classList.add('is-show');
        bodyScrollPrevent(true);
    });

    for (let j of [closeModal, modalBg]) {
        j.addEventListener('click', function () {
            modalArea.classList.remove('is-show');
            iModal.classList.remove('is-show');
            bodyScrollPrevent(false, modalArea);
        });
    }
}

// Derived Constants
const socket = io("http://0.0.0.0:9173");

// Functions
function log(...args) {
    ipcRenderer.send("log", ...args);
    console.log(...args);
}

function errorLog(event) {
    let msg = source = lineno = colno = error = time = "";
    msg = event.message;
    source = event.filename;
    lineno = event.lineno;
    colno = event.colno;
    error = event.error;
    time = event.time;

    log(`Script Error was Found
    Message: ${msg}
    Source Info: ${source}
    Line No: ${lineno}
    Column No: ${colno}
    Error Info: ${error}`)
}

function emit(eventName, ...args) {
    callback = args.pop(-1);
    function opCallback(err, res) {
        log(`${eventName} (err): ${err}`);
        if (res != null && res.constructor == Object) {
            logRes = JSON.stringify(res);
        } else {
            logRes = res;
        }
        log(`${eventName} (res): ${logRes}`);
        log(args)
        callback(err, res);
    }
    socket.emit(eventName, ...args, opCallback);
}

function updateConfig() {
    emit('config', null, (err, res) => {
        ddir.textContent = res.download_dir;
        owTgl.checked = res.overwrite;
    })
}

function fadeOut(el) {
    el.style.opacity = 0;
};

function fadeIn(el) {
    el.style.opacity = 0;
    (function fade() {
        var val = parseFloat(el.style.opacity);
        if (!((val += .1) > 1)) {
            el.style.opacity = val;
            requestAnimationFrame(fade);
        }
    })();
};

function inputFn() {
    if (this.value != '') {
        eraseBtn.style.visibility = 'visible';
        if (this.checkValidity()) {
            fadeIn(dlBtn);
            this.classList.add("valid");
            this.classList.remove("invalid");
        } else {
            fadeOut(dlBtn);
            this.classList.add("invalid");
            this.classList.remove("valid");
        }
    } else {
        fadeOut(dlBtn);
        eraseBtn.style.visibility = 'hidden';
        this.classList.remove("valid");
        this.classList.remove("invalid");
    }
}

function eraseInput() {
    input.value = '';
    eraseBtn.style.visibility = 'hidden';
    fadeOut(dlBtn);
    input.classList.remove("valid");
    input.classList.remove("invalid");
}

function bodyScrollPrevent(flag, modal) {
    let scrollPosition;
    const body = document.getElementsByTagName('body')[0];
    const ua = window.navigator.userAgent.toLowerCase();
    const isiOS = ua.indexOf('iphone') > -1 || ua.indexOf('ipad') > -1 || ua.indexOf('macintosh') > -1 && 'ontouchend' in document;
    const scrollBarWidth = window.innerWidth - document.body.clientWidth;

    if (flag) {
        body.style.paddingRight = scrollBarWidth + 'px';

        if (isiOS) {
            scrollPosition = -window.pageYOffset;
            body.style.position = 'fixed';
            body.style.width = '100%';
            body.style.top = scrollPosition + 'px';
        } else {
            body.style.overflow = 'hidden';
        }
    } else if (!flag) {
        addEventListenerOnce(modal, 'transitionend', function () {
            body.style.paddingRight = '';

            if (isiOS) {
                scrollPosition = parseInt(body.style.top.replace(/[^0-9]/g, ''));
                body.style.position = '';
                body.style.width = '';
                body.style.top = '';
                window.scrollTo(0, scrollPosition);
            } else {
                body.style.overflow = '';
            }
        });
    }

    function addEventListenerOnce(node, event, callback) {
        const handler = function (e) {
            callback.call(this, e);
            node.removeEventListener(event, handler);
        };

        node.addEventListener(event, handler);
    }
}

// Toast function
function toast({ title = "", message = "", type = "info", duration = 3000 }) {
    const main = document.getElementById("toast");
    if (main) {
        const toast = document.createElement("div");

        // Auto remove toast
        const autoRemoveId = setTimeout(function () {
            main.removeChild(toast);
        }, duration + 1000);

        // Remove toast when clicked
        toast.onclick = function (e) {
            if (e.target.closest(".toast__close")) {
                main.removeChild(toast);
                clearTimeout(autoRemoveId);
            }
        };

        const icons = {
            success: "fas fa-check-circle",
            info: "fas fa-info-circle",
            warning: "fas fa-exclamation-circle",
            error: "fas fa-exclamation-circle"
        };
        const icon = icons[type];
        const delay = (duration / 1000).toFixed(2);

        toast.classList.add("toast", `toast--${type}`);
        toast.style.animation = `slideInLeft ease .3s, fadeOut linear 1s ${delay}s forwards`;

        toast.innerHTML = `
            <div class="toast__icon">
                <i class="${icon}"></i>
            </div>
            <div class="toast__body">
                <h3 class="toast__title">${title}</h3>
                <p class="toast__msg">${message}</p>
            </div>
            <div class="toast__close">
                <i class="fas fa-times"></i>
            </div>
        `;
        main.appendChild(toast);
    }
}


// Event Listeners
input.addEventListener('input', inputFn);
eraseBtn.addEventListener('click', eraseInput);
owTgl.addEventListener('change', () => {
    emit('write_config', stg = "overwrite", value = owTgl.checked, (err, res) => {
        if (err) {
            var title = "Settings updated"
            var message = `${owTgl.checked ? "Enabled" : "Disabled"} overwrite successfully`
            var type = "success"
        } else {
            var title = "Settings did not update"
            var message = `Unsuccessfuly tried to ${owTgl.checked ? "enable" : "disable"} overwrite`
            var type = "error"
        }
        toast({
            title: title,
            message: message,
            type: type,
            duration: 1000
        });
    });
});

dlBtn.addEventListener('click', () => {
    emit('dl', url = input.value, (err, res) => {
        if (err) {
            var title = "Settings updated"
            var message = `Sucessfully downloaded "${input.value}" to "${res}"`
            var type = "success"
        } else {
            var title = "Settings did not update"
            var message = `Unsuccessfuly downloaded "${input.value}"`
            var type = "error"
        }
        toast({
            title: title,
            message: message,
            type: type,
            duration: 5000
        });
    });
});

cdir.addEventListener('click', function () { ipcRenderer.send("cds") })

// IPC Listeners
ipcRenderer.on('logPath', function (event, path) {
    window.logPath = path;
    log("Log Path:", path);
});
ipcRenderer.on('cdr', function (event, cdr) {
    ddir.textContent = cdr;
    emit('write_config', stg = "download_dir", value = cdr, (err, res) => {
        if (err) {
            var title = "Settings updated"
            var message = `Sucessfully updated the Download directory to "${cdr}"`
            var type = "success"
        } else {
            var title = "Settings did not update"
            var message = `Unsuccessfuly updated the Download directory to "${cdr}"`
            var type = "error"
        }
        toast({
            title: title,
            message: message,
            type: type,
            duration: 2500
        });
    });
});

emit('cfg_path', null, (err, res) => {
    log(res);
    fs.watchFile(res, () => {
        updateConfig();
    });
})

// Initialize

updateConfig();
ipcRenderer.send("logPath");