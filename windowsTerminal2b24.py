#!/usr/bin/env python3
"""Convert profiles.json to base24 scheme
"""
import os
import sys
import argparse
import yaml
import commentjson
from metprint import (
	LogType,
	Logger
)
import base24tools


def genBase24s(winTerm):
	"""Generate the base24 json object

	Args:
		winTerm (str): a dictionary representing the source theme

	Returns:
		dict[]: base24 dicts to write to scheme file
	"""
	base24s = []
	for scheme in winTerm:
		base24 = {"author": "WinTerm2B24", "scheme": scheme["name"]}
		base24lookup = {
			"base00": "background",
			"base01": "black", #Black
			"base02": "brightBlack", #Bright black
			"base05": "foreground", #Bright black
			"base06": "white", #White
			"base07": "brightWhite", #Bright white
			"base08": "red", #Red
			"base09": "yellow", #Yellow
			"base0A": "brightYellow", #Bright yellow
			"base0B": "green", #Green
			"base0C": "cyan", #Cyan
			"base0D": "blue", #Blue
			"base0E": "purple", #Purple
			"base12": "brightRed", #Bright red
			"base13": "brightYellow", #Bright yellow
			"base14": "brightGreen", #Bright green
			"base15": "brightCyan", #Bright cyan
			"base16": "brightBlue", #Bright blue
			"base17": "brightPurple", #Bright purple
		}

		base24s.append(base24tools.process(base24, base24lookup, scheme, 2, 5))

	return base24s


def winTerm2hex(filename):
	"""Generate the shemes (without #)

	Args:
		filename (str): filename from args

	Returns:
		dict: a dictionary representing the source theme
	"""
	profiles = commentjson.loads(open(filename).read())
	for scheme in profiles["schemes"]:
		for colour in scheme:
			scheme[colour] = scheme[colour].replace("#", "")

	return profiles["schemes"]



def main():
	''' Main entry point for cli '''
	parser = argparse.ArgumentParser(
	description="Convert profiles.json to base24 scheme")
	parser.add_argument("file", action="store",
	help="profiles.json")
	args = parser.parse_args()
	# Check for and report level8 errors
	if not os.path.isfile(args.file):
		Logger().logPrint(args.file + " is not a valid file", LogType.ERROR)
		sys.exit(1)

	filename = args.file


	base24s = genBase24s(winTerm2hex(filename))

	for base24 in base24s:
		with open(base24["scheme"]+".yaml", "w") as outfile:
			Logger().logPrint("writing \"" + base24["scheme"] + "\" to file", LogType.SUCCESS)
			yaml.dump(base24, outfile)

if __name__ == '__main__':
	main()
