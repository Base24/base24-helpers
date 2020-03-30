#!/usr/bin/env python3
"""Convert .itermcolors to base24 scheme
"""

import os
import sys
import argparse
import defusedxml.ElementTree as ET
import yaml
from metprint import (
	LogType,
	Logger
)
import base24tools

def rgb_to_hex(rgb):
	''' Converts rgb to hex '''
	return '%02x%02x%02x' % rgb

def iterm2hex(root):
	"""Get hex codes from iterm xml

	Args:
		root (xmlroot): xmlroot

	Returns:
		dict: iterm keys to hex
	"""
	keys = root.findall("./dict/key")
	dicts = root.findall("./dict/dict")
	iterm = {}
	for i, _key in enumerate(keys):
		keyName = keys[i].text
		r = g = b = None
		for index, item in enumerate(dicts[i]):
			if "Red Component" in item.text:
				r = int(float(dicts[i][index+1].text) * 255.0)
			if "Green Component" in item.text:
				g = int(float(dicts[i][index+1].text) * 255.0)
			if "Blue Component" in item.text:
				b = int(float(dicts[i][index+1].text) * 255.0)
		iterm[keyName] = rgb_to_hex((r, g, b))
	return iterm


def genBase24(filename, iterm):
	"""Generate the base24 json object

	Args:
		filename (str): filename from args
		iterm (dict): iterm keys to hex

	Returns:
		dict: base24 dict to write to scheme file
	"""

	base24 = {"author": "Iterm2B24", "scheme": filename.split(".")[0]}
	base24lookup = {
		"base00": "Background Color",
		"base01": "Ansi 0 Color", #Black
		"base02": "Ansi 8 Color", #Bright black
		"base06": "Ansi 7 Color", #White
		"base07": "Ansi 15 Color", #Bright white
		"base08": "Ansi 1 Color", #Red
		"base09": "Ansi 3 Color", #Yellow
		"base0A": "Ansi 12 Color", #Bright yellow (variant 2)
		"base0B": "Ansi 2 Color", #Green
		"base0C": "Ansi 6 Color", #Cyan
		"base0D": "Ansi 4 Color", #Blue
		"base0E": "Ansi 5 Color", #Purple
		"base12": "Ansi 9 Color", #Bright red
		"base13": "Ansi 11 Color", #Bright yellow
		"base14": "Ansi 10 Color", #Bright green
		"base15": "Ansi 14 Color", #Bright cyan
		"base16": "Ansi 12 Color", #Bright blue
		"base17": "Ansi 13 Color", #Bright purple
	}

	return base24tools.process(base24, base24lookup, iterm, 2, 6)


def main():
	''' Main entry point for cli '''
	parser = argparse.ArgumentParser(
	description="Convert .itermcolors to base24 scheme")
	parser.add_argument("file", action="store",
	help="file.itermschemes")
	args = parser.parse_args()
	# Check for and report level8 errors
	if not os.path.isfile(args.file):
		Logger().logPrint(args.file + " is not a valid file", LogType.ERROR)
		sys.exit(1)

	filename = args.file
	tree = ET.parse(filename)

	base24 = genBase24(filename, iterm2hex(tree.getroot()))

	with open(base24["scheme"]+".yaml", "w") as outfile:
		Logger().logPrint("writing \"" + base24["scheme"] + "\" to file", LogType.SUCCESS)
		yaml.dump(base24, outfile)

if __name__ == '__main__':
	main()
