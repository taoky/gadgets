# gadgets

This is a gadget collection of taoky.

You may see something useful or useless here.

ABSOLUTELY NO WARRANTY.

Every gadget is under Apache License unless specially claimed.

## Index

- BeepPlayConverter: Python, unstable. Converts music sheets to [BeepPlay](https://github.com/iBug/CGadgets/tree/master/BeepPlay)'s format.
- Bilibili OST Downloader: Python & Shell, unstable. Helps download & arrange OSTs from Bilibili.
- KnightTour: Electron, homework assignment. Demonstrates the Knight Tour problem. Supports multi-thread DFS & optimized Warnsdorff algorithm.
- PyQt-Sudoku: Python & Qt, homework assignment. A playable sudoku program. Uses optimized & randomized DFS algorithm.
- WallpaperReplacer: C++/CLR, Windows, stable. See [This link](https://github.com/taoky/WallpaperReplacer). A small program helping you change wallpapers at regular intervals for Windows XP and above.
- consoleTimer: C, cross-platform, homework assignment. A timer working in Windows & *nix consoles. Requires `ncurses` in *nix environments.
- fake-sh: C. A fake shell imitating `/bin/sh`. For CTF pwn environment.
- myBank: C, homework assignment. A program to store bills. Features linked list & user input check.
- pwn-dockerfile: Dockerfile, unstable. A `Dockerfile` for pwn environment using `socat`.

## Using sparse-checkout to clone a part of this repo

```sh
git init
git remote add -f origin git@github.com:taoky/gadgets.git
git config core.sparsecheckout true
echo "this_is_a_directory" >> .git/info/sparse-checkout # change it to the directory you want to clone
git pull origin master
```
