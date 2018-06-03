"use strict"

var n;
var grid;
const dmove = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]];
var isSolveable = false;

var totalCnt = 0;
var fs, filename;

self.addEventListener("message", function (e) {
    n = e.data;
    console.log("Worker received parameter n: " + n)
    if (typeof (n) !== "number") {
        throw new Error("Invalid parameter");
    }
    cleanGrid();
    isSolveable = warnsdorff();
    if (!isSolveable) {
        self.postMessage(false);
    }
    else {
        self.postMessage(true);
    }
    self.close()
}, false)

function cleanGrid() {
    grid = [...Array(n)].map(f => Array(n).fill(-1)); // create a n * n grid
}

function warnsdorff() {
    function availableSteps(i, j) {
        var cnt = 0;
        for (let k = 0; k < 8; k++) {
            var newi = i + dmove[k][0];
            var newj = j + dmove[k][1];
            if (newi >= 0 && newi < n && newj >= 0 && newj < n && grid[newi][newj] === -1) {
                cnt++;
            }
        }
        return cnt;
    }
    function distToCenter(i, j) {
        var nowx = i * 2 + 1;
        var nowy = j * 2 + 1;
        var center = n / 2;
        return (nowx - center) * (nowx - center) + (nowy - center) * (nowy - center);
    }
    function solve(isNaive) {
        var x = 0; var y = 0; var c = 0;
        while (availableSteps(x, y) != 0) {
            grid[x][y] = c;
            var minStep = 1e9; // just a num > 8
            var kmin = -1;
            var maxDis = -1;
            for (let k = 0; k < 8; k++) {
                var newx = x + dmove[k][0];
                var newy = y + dmove[k][1];
                if (newx >= 0 && newx < n && newy >= 0 && newy < n && grid[newx][newy] === -1) {
                    var nowSteps = availableSteps(newx, newy);
                    if (nowSteps <= minStep) {
                        if (nowSteps < minStep) maxDis = -1;
                        if (isNaive || (!isNaive && distToCenter(newx, newy) > maxDis)) {
                            minStep = nowSteps;
                            kmin = k;
                            maxDis = distToCenter(newx, newy);
                        }
                    }
                }
            }
            x += dmove[kmin][0];
            y += dmove[kmin][1];
            c++;
        }
        grid[x][y] = c;
        if (c !== n * n - 1)
            return false;
        else {
            self.postMessage(grid);
            return true;
        }
    }
    if (!solve(true)) {
        console.log("Naïve failed. Trying Arnd Roth's proposition.");
        cleanGrid();
        return solve(false);
    }
    else {
        return true;
    }
}