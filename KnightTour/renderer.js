"use strict"
// import { BrowserWindow } from "electron";
const BrowserWindow = require('electron').remote.BrowserWindow;
const path = require('path');
const url = require('url');

// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

// deal with spinner
$("input[type='number']").InputSpinner();

var worker;
var ctx = document.getElementById("canvas").getContext("2d");
var data;
var gridWidth;
var n;

var btn_run = document.getElementById("btn-run");
var spinner = document.getElementById("spinner");
var btn_all = document.getElementById("btn-all");
var loading = document.getElementById("loading");
var speedNum = document.getElementById("speed");
var speedRes = document.getElementById("speedRes");
var anim_id;
var check_id;
var isFailed;

const canvasLen = 550;
var interval;

function startWorker() {
    closeWorker();
    n = getSpinnerNumber();
    worker = new Worker("worker.js");
    isFailed = false;
    worker.addEventListener("message", function (e) {
        if (typeof (e.data) != "boolean") {
            data = e.data;
        }
        else if (e.data == false) {
            alert("Failed to find a solution!");
            isFailed = true;
        }
    }, false);
    worker.postMessage(n);
}

function closeWorker() {
    try {
        worker.terminate();
    }
    catch (TypeError) {
        // expected
    }
}

function drawInit() {
    ctx.clearRect(0, 0, canvasLen, canvasLen);
    gridWidth = canvasLen / n;
    // draw lines
    ctx.beginPath();
    ctx.moveTo(0, 0);
    for (let i = 0; i <= n; i++) { // n + 1 times
        ctx.lineTo(canvasLen, i * gridWidth);
        ctx.moveTo(i * gridWidth, 0);
        ctx.lineTo(i * gridWidth, canvasLen);
        ctx.moveTo(0, (i + 1) * gridWidth);
    }
    ctx.stroke();
    ctx.closePath();
    ctx.moveTo(0, 0);
}

function fillRect(i, j, c, isPast) {
    var x = i * gridWidth, y = j * gridWidth;
    if (isPast) {
        ctx.fillStyle = "orange";
    }
    else {
        ctx.fillStyle = "blue";
    }
    ctx.fillRect(x, y, gridWidth, gridWidth);
    if (n < 15) {
        ctx.font = "24px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "white";
        ctx.fillText(c, x + gridWidth / 2, y + gridWidth / 2);
    }
}

function animateShow() {
    drawInit();
    if (data === undefined) {
        return;
    }
    fillRect(0, 0, 0, false); // start from (0, 0)
    var drawQueue = new Array(data.length);
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            drawQueue[data[i][j]] = [i, j];
        }
    }

    function animStep(i) {
        fillRect(drawQueue[i - 1][0], drawQueue[i - 1][1], i - 1, true);
        fillRect(drawQueue[i][0], drawQueue[i][1], i, false);
        if (i == drawQueue.length - 1) {
            stopAnimation();
        }
        else if (anim_id != undefined) {
            anim_id = setTimeout(() => animStep(i+1), interval)
        }
    }

    anim_id = setTimeout(() => animStep(1), interval);
}

function stopAnimation() {
    btn_run.disabled = false;
    if (anim_id != undefined) {
        clearTimeout(anim_id);
        anim_id = undefined;
    }
}


function getSpinnerNumber() {
    return parseInt(spinner.value);
}

n = getSpinnerNumber();
interval = speedNum.value;
speedRes.innerHTML = interval;
startWorker();
drawInit();

function checkAndLoad() {
    if (data === undefined && isFailed === false) {
        return;
    }
    if (check_id !== undefined) {
        clearInterval(check_id);
    }
    loading.hidden = true;
    if (isFailed === false)
        animateShow();
}

btn_run.addEventListener("click", function () {
    stopAnimation();
    if (n != getSpinnerNumber()) {
        n = getSpinnerNumber();
        startWorker();
        loading.hidden = false;
        check_id = setInterval(checkAndLoad, 100);
    }
    else {
        loading.hidden = true;
        animateShow();
    }
}, false);

btn_all.addEventListener("click", function() {
    var popup = new BrowserWindow({ 
        width: 512, height: 512
    });
    popup.webContents.on('did-finish-load', ()=>{
        popup.webContents.send("message", getSpinnerNumber());
        popup.show();
        popup.focus();
    });
    popup.on('closed', () => {
        popup = null;
    })
    popup.loadURL(url.format({
        pathname: path.join(__dirname, 'all.html'),
        protocol: 'file:',
        slashes: true
      }))
}, false)

speedNum.addEventListener("input", function() {
    interval = speedNum.value;
    speedRes.innerHTML = interval;
});