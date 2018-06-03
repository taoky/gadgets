"use strict"

var n;
var grid;
const dmove = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]];
var isSolveable = false;

self.addEventListener("message", function (e) {
    n = e.data[0];
    grid = e.data[1];
    var startx = e.data[2];
    var starty = e.data[3];
    if (typeof (n) !== "number") {
        throw new Error("Invalid parameter");
    }
    dfs(startx, starty, 3);
    if (!isSolveable) {
        self.postMessage(false);
    }
    else {
        self.postMessage(true);
    }
    self.close()
}, false)

function dfs(i, j, c) {
    if (c === n * n) {
        self.postMessage(grid);
        self.postMessage(transpose());
        isSolveable = true;
        return;
    }
    for (let k = 0; k < 8; k++) {
        var newi = i + dmove[k][0];
        var newj = j + dmove[k][1];
        if (newi >= 0 && newi < n && newj >= 0 && newj < n && grid[newi][newj] === -1) {
            grid[newi][newj] = c;
            dfs(newi, newj, c + 1);
            grid[newi][newj] = -1;
        }
    }
}

function transpose() {
    var res = [...Array(n)].map(f => Array(n).fill(-1));
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            res[j][i] = grid[i][j];
        }
    }
    return res;
}