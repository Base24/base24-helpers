[![Github top language](https://img.shields.io/github/languages/top/Base24/base24-helpers.svg?style=for-the-badge)](../../)
[![Codacy grade](https://img.shields.io/codacy/grade/[codacy-proj-id].svg?style=for-the-badge)](https://www.codacy.com/manual/Base24/base24-helpers)
[![Repository size](https://img.shields.io/github/repo-size/Base24/base24-helpers.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/Base24/base24-helpers.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/Base24/base24-helpers.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/Base24/base24-helpers.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/Base24/base24-helpers.svg?style=for-the-badge)](../../commits/master)

<!-- omit in TOC -->
# base24-helpers

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Helper programs to create templates and schemes.

- [base24tools.py](#base24toolspy)
- [baseCompare.py](#basecomparepy)
- [batchIterm2b24.py](#batchiterm2b24py)
- [iterm2base24.py](#iterm2base24py)
- [windowsTerminal2b24.py](#windowsterminal2b24py)
- [schemeSuggest.py](#schemesuggestpy)
- [templateGen.py](#templategenpy)
- [schemeTableGen.py](#schemetablegenpy)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Download](#download)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
- [How to run](#how-to-run)
	- [With VSCode](#with-vscode)
	- [From the Terminal](#from-the-terminal)
- [Changelog](#changelog)
- [Licence](#licence)


## base24tools.py

Lib file used by iterm2base24.py and windowsTerminal2b24.py with the following
function:

```python
def process(base24, base24lookup, sourceThemeDict, bgNumber, fgNumber):
	"""process a base24 dict using a lookup table to translate the source theme
	onto the base24 scheme

	Args:
		base24 (dict): a dictionary representing a base24 scheme
		base24lookup (dict): a dictionary mapping base24 colour ids to the
		respective key in the sourceThemeDict
		sourceThemeDict (dict): a dictionary representing the source theme/
		scheme
		bgNumber (int): lower base0N bound for the background 0-9
		fgNumber (int): upper base0N bound for the foreground 0-9. Must be
		greater than bgNumber

	Returns:
		dict: base24 dict to write to scheme file
	"""
```

## baseCompare.py

Compare base16 and base24 Windows terminal themes quickly

```bash
usage: baseCompare.py [-h] [--all] themes

Compare base16 and base24 windows terminal themes quickly

positional arguments:
  themes      directory containing generated windows terminal themes

optional arguments:
  -h, --help  show this help message and exit
  --all       compare all schemes
```

## batchIterm2b24.py

Convert a directory containing .itermcolors to base24 schemes

```bash
usage: batchIterm2b24.py [-h] itermschemes

Convert .itermcolors to base24 scheme in a directory

positional arguments:
  itermschemes  directory containing itermschemes

optional arguments:
  -h, --help    show this help message and exit
```

## iterm2base24.py

Convert a singular .itermcolors to a base24 scheme

```bash
usage: iterm2base24.py [-h] file

Convert .itermcolors to base24 scheme

positional arguments:
  file        file.itermschemes

optional arguments:
  -h, --help  show this help message and exit
```

## windowsTerminal2b24.py

Convert a profiles.json (such as your own) to a number of base24 schmes

```bash
usage: windowsTerminal2b24.py [-h] file

Convert profiles.json to base24 scheme

positional arguments:
  file        profiles.json

optional arguments:
  -h, --help  show this help message and exit
```

## schemeSuggest.py

Suggest scheme colours based on a base24 theme template and the theme file

```bash
usage: schemeSuggest [-h] [--mode MODE] template theme

Pair colours with base24 colour ids

positional arguments:
  template     relative or abs path to the base24 template
  theme        relative or abs path to the theme file

optional arguments:
  -h, --help   show this help message and exit
  --mode MODE  color format: hex (ff00aa), reversehex (aa00ff), rgb (255,0,170), reversergb (170,0,255), dec (1.0,0,0.666),
               reversedec (0.666,0,1.0)
```

## templateGen.py

Take and existing theme and a base24 scheme file and produces a base24 template
file

```bash
usage: templateGen [-h] [--mode MODE] [--fuzz FUZZ] colour_scheme theme

Generate a base24 template from an existing scheme and a theme file

positional arguments:
  colour_scheme  relative or abs path to the base24 colour scheme
  theme          relative or abs path to the theme file

optional arguments:
  -h, --help     show this help message and exit
  --mode MODE    color format: hex (ff00aa), reversehex (aa00ff), rgb (255,0,170), reversergb (170,0,255), dec (1.0,0,0.666),
                 reversedec (0.666,0,1.0)
  --fuzz FUZZ    find 'close' colours and replace these ((r,g,b)+-fuzz: default=0, max-recommended=5)
```


## schemeTableGen.py

Generate a table to put in a scheme project readme

```bash
usage: schemeTableGen.py [-h] scheme

Generate a table to put in a scheme project readme

positional arguments:
  scheme      base24 scheme file

optional arguments:
  -h, --help  show this help message and exit
```

## Language information
### Built for
This program has been written for Python 3 and has been tested with
Python version 3.8.0 <https://www.python.org/downloads/release/python-380/>.

## Install Python on Windows
### Chocolatey
```powershell
choco install python
```
### Download
To install Python, go to <https://www.python.org/> and download the latest
version.

## Install Python on Linux
### Apt
```bash
sudo apt install python3.8
```

## How to run
### With VSCode
1. Open the .py file in vscode
2. Ensure a python 3.8 interpreter is selected (Ctrl+Shift+P > Python:Select
3. Interpreter > Python 3.8)
4. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)
### From the Terminal
```bash
./[file].py
```

## Changelog
See the [CHANGELOG](/CHANGELOG.md) for more information.

## Licence
MIT License
Copyright (c) Base24
(See the [LICENSE](/LICENSE.md) for more information.)
