#!/usr/bin/env python3
"""Convert .itermcolors to base24 scheme
"""

import os
import sys
import defusedxml.ElementTree as ET
import yaml
from metprint import (
	LogType,
	Logger
)

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

	# Keys apart from base03, base04, base05, base0F, base10, base11 can be
	# taken from iterm
	for key in base24lookup:
		base24[key] = iterm[base24lookup[key]]

	# Is it really a base16 theme? Compare red and bright red to find out
	if base24["base08"] == base24["base12"]:
		Logger().logPrint("\"" + base24["scheme"] + "\" is a base16 theme", LogType.WARNING)
		base24["scheme"] = "b16" + base24["scheme"]

	# Keys base03, base04, base05, base0F, base10, base11 can be calculated
	#Background through Foreground
	bg = base24["base02"]
	fg = base24["base06"]
	for index in range(3, 6):
		mult = index - 2
		baseVal = []
		for section in range(0, 5, 2):
			baseVal.append("{:02x}".format(int(bg[0+section:2+section], 16) + int(
				(int(fg[0+section:2+section], 16) - int(bg[0+section:2+section], 16)) * mult / 4
				)
			))
		base24["base0"+str(index)] = "".join(baseVal)

	#Darker and darkest backgrounds
	for index in range(10, 12):
		mult = 12 - index
		baseVal = []
		for section in range(0, 5, 2):
			baseVal.append("{:02x}".format(int(int(bg[0+section:2+section], 16) * mult / 3)
			))
		base24["base"+str(index)] = "".join(baseVal)

	#Dark red (variant 2)
	baseVal = []
	for section in range(0, 5, 2):
		baseVal.append("{:02x}".format(int(int(base24["base08"][0+section:2+section], 16) / 2)
		))
	base24["base0F"] = "".join(baseVal)

	# Have the other colours been calculated correctly? Count the number of
	# 000000s
	listOf000000s = [base24[key] for key in base24 if base24[key] == "000000"]
	if len(listOf000000s) > 2: # 2 seems a sensible threshold
		Logger().logPrint("\"" + base24["scheme"].replace("b16", "") + "\" is probably corrupted",
		LogType.WARNING)
		base24["scheme"] = "warn0s" + base24["scheme"]

	return base24


def main():
	''' Main entry point for cli '''
	# Check for and report level8 errors
	if len(sys.argv) < 2:
		Logger().logPrint("usage: ./iterm2base24.py file.itermcolors", LogType.ERROR)
		sys.exit(1)
	if not os.path.isfile(sys.argv[1]):
		Logger().logPrint(sys.argv[1] + " is not a valid file", LogType.ERROR)
		sys.exit(1)

	filename = sys.argv[1]
	tree = ET.parse(filename)

	base24 = genBase24(filename, iterm2hex(tree.getroot()))

	with open(base24["scheme"]+".yaml", "w") as outfile:
		Logger().logPrint("writing \"" + base24["scheme"] + "\" to file", LogType.SUCCESS)
		yaml.dump(base24, outfile)

if __name__ == '__main__':
	main()
