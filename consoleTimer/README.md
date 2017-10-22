# consoleTimer
This is a timer working in console (both Windows and \*nix). This was indeed a experiment assignment, but teacher's intention was to write a console program working only in Windows. As a Mac user, I felt VERY UNHAPPY, so I wrote this cross-platform program.

## Feature

1. **TOO Colorful Time display! (Can be disabled by modifying source code)**

2. **One source file, many available platforms!**

## Install

1. Download consoleTimer.c (Also, clone the whole repository and use cmake is also OK.)

2. Then compile according to your platform:

```
if (WINDOWS) : cl consoleTimer.c 
or
gcc consoleTimer.c -o consoleTimer.exe

elif (*NIX) : gcc consoleTimer.c -lcurses -o consoleTimer
```

Notice that when compiling in \*nix, you need have `curses` installed. Use your favorite compiler.


You are neither Windows or \*nix user? I have nothing to say.

## About the color

If you don't want the color, just comment `#define ENABLE_COLOR`, and recompile.
