# fake-sh

A fake shell imitating `/bin/sh`, targeting CTF pwn.

Source from: [brenns10/lsh](https://github.com/brenns10/lsh/).

## Usage

Compile it, and put `sh` into (`chroot`ed) `/bin/`.

## Features

Modified from the original LSH:

- Supports being executed through `system("/bin/sh")` or `system("sh")`.

- Builtins are:

    - `ls` & `/bin/ls`: execute the real `/bin/ls`.

    - `cat` & `/bin/cat`: also execute the real `/bin/cat`, but allow `flag` as the second argument only.

    - `sh` & `/bin/sh`: show a fake error message. (Prevent someone keeping creating processes)

    - `exit`: exit the fake shell.

    - `cd` & `help` are NOT supported.

- Disallows executing other programs.
