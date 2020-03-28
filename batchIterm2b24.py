#!/usr/bin/env python3
"""Convert .itermcolors to base24 scheme in a directory
"""
import sys
import os
import yaml
import defusedxml.ElementTree as ET
from metprint import (
	LogType,
	Logger
)
import iterm2base24

def main():
	''' Main entry point for cli '''
	# Check for and report level8 errors
	if len(sys.argv) < 2:
		Logger().logPrint("usage: ./iterm2base24.py itermschemes", LogType.ERROR)
		sys.exit(1)
	if not os.path.isdir(sys.argv[1]):
		Logger().logPrint(sys.argv[1] + " is not a valid directory", LogType.ERROR)
		sys.exit(1)

	for file in os.listdir(sys.argv[1]):
		# Generate scheme from file
		filename = os.path.join(sys.argv[1], file)
		tree = ET.parse(filename)
		base24 = iterm2base24.genBase24(file, iterm2base24.iterm2hex(tree.getroot()))

		# Write schemes
		directory = "batchSchemes"
		if not os.path.exists(directory):
			os.makedirs(directory)
		with open(os.path.join(directory, base24["scheme"]+".yaml"), "w") as outfile:
			Logger().logPrint("writing \"" + base24["scheme"] + "\" to file", LogType.SUCCESS)
			yaml.dump(base24, outfile)

if __name__ == "__main__":
	main()
