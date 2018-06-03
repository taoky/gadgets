"use strict"

var textConsole = document.getElementById("console");
var textConsole2 = document.getElementById("console2");
var workers = [];

const ipc = require('electron').ipcRenderer;

var n;
var fs, filename;
var grid;
var totalIndex = 0;

function writeLog(msg) {
    textConsole.textContent += msg + '\n';
}

ipc.on("message", (event, message) => {
    n = message;
    writeLog("Received n = " + n);
    if (n > 42) {
        writeLog("It's too much. To avoid taking up too much time & stack overflow problem, calculation is stopped.")
        return;
    }
    writeLog("Start calculating all solutions...")
    startWorker();
})

function closeWorker() {
    try {
        for (let i = 0; i < 5; i++)
            workers[i].terminate();
    }
    catch (TypeError) {
        // expected
    }
}

function startWorker() {
    closeWorker();
    dfsManager();
}

// function generateFormattedText(data) {
//     var str = "";
//     for (let j = 0; j < n; j++) {
//         for (let k = 0; k < n; k++) {
//             str += data[k][j] + " "
//         }
//         str += "\n";
//     }
//     return str;
// }

function initFile() {
    fs = require("fs");
    filename = "solution" + n + ".txt";
    fs.unlink(filename);
}

function generateFormattedText(data) {
    var str = "";
    for (let j = 0; j < n; j++) {
        for (let k = 0; k < n; k++) {
            str += data[k][j] + " "
        }
        str += "\n";
    }
    str += "\n";
    return str;
}


function writeFile(grid) {
    var str = generateFormattedText(grid);
    fs.appendFile(filename, str, (err) => {
        if (err) throw err;
    });
}

function dfsManager() {
    initFile();
    cleanGrid();
    grid[0][0] = 0;
    grid[1][2] = 1;
    const mx = [0, 2, 3, 3, 2];
    const my = [4, 4, 3, 1, 0];

    function modified(i) {
        var res = JSON.parse(JSON.stringify(grid)); // deepcopy
        res[mx[i]][my[i]] = 2;
        return res;
    }
    for (let i = 0; i < 5; i++) {
        workers[i] = new Worker("dfs_worker.js");
        workers[i].postMessage([n, modified(i), mx[i], my[i]]);
        workers[i].addEventListener("message", function (e) {
            if (typeof (e.data) !== "boolean") {
                totalIndex++;
                textConsole2.textContent = totalIndex;
                writeFile(e.data);
            }
            else if (e.data == true) {
                // end
                writeLog("Thread " + i + ": " + "Have discovered " + totalIndex + " solutions by far when n = " + n + ".")
            }
            else if (e.data == false) {
                writeLog("No solution!");
            }
        }, false);
    }
}

function cleanGrid() {
    grid = [...Array(n)].map(f => Array(n).fill(-1)); // create a n * n grid
}

window.onunload = closeWorker;