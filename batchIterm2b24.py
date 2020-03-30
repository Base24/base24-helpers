#!/usr/bin/env python3
"""Convert .itermcolors to base24 scheme in a directory
"""
import sys
import os
import argparse
import yaml
import defusedxml.ElementTree as ET
from metprint import (
	LogType,
	Logger
)
import iterm2base24

def main():
	''' Main entry point for cli '''
	parser = argparse.ArgumentParser(
	description="Convert .itermcolors to base24 scheme in a directory")
	parser.add_argument("itermschemes", action="store",
	help="directory containing itermschemes")
	args = parser.parse_args()
	# Check for and report level8 errors
	if not os.path.isdir(args.itermschemes):
		Logger().logPrint(args.itermschemes + " is not a valid directory", LogType.ERROR)
		sys.exit(1)

	for file in os.listdir(args.itermschemes):
		# Generate scheme from file
		filename = os.path.join(args.itermschemes, file)
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
