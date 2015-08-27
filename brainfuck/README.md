PyBeef
======

[Brainfuck](https://esolangs.org/wiki/Brainfuck)

Python interpreter for Brainfuck programs
By default, PyBeef will ask for input when using "," (see Config below):

- `value = ord(input[0])`
- If input begins by "#", interprets as number (use 0x for hex)


## Config

Use environment variables to configure PyBeef:

- `BF_STDIN`: read from stdin rather than asking for values
- `BF_DEBUG`: see Debug below


## Debug

If `BF_DEBUG` is enabled, use :

- `!`: prints all cells value
- `*`: prints current cell value, along with cursor value
