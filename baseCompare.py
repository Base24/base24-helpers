#!/usr/bin/env python3.8
"""Compare base16 and base24 windows terminal themes quickly
"""
import sys
import os
import argparse
import platform
import ctypes
import commentjson
from metprint import (
	LogType,
	Logger
)

def cPrint(colourHex):
	''' Print a hex colour '''
	colour = colourHex[1:]
	print("\033[48;2;"+ ";".join([str(int(colour[0:2], 16)),
	str(int(colour[2:4], 16)), str(int(colour[4:6], 16))]) +
	"m  \033[0m", end="")



def printColours(winTerm):
	''' Print the colours for a theme '''
	scheme = commentjson.loads(open(winTerm).read()[:-2])
	keys = ["background", "black", "brightBlack", "foreground", "white",
	"brightWhite", "red", "yellow", "brightYellow", "green", "cyan", "blue",
	"purple", "brightRed", "brightYellow", "brightGreen", "brightCyan",
	"brightBlue", "brightPurple"]
	for key in keys:
		cPrint(scheme[key])
	print()




def main():
	''' Main entry point for cli '''
	parser = argparse.ArgumentParser(
	description="Compare base16 and base24 windows terminal themes quickly")
	parser.add_argument("themes", action="store",
	help="directory containing generated windows terminal themes")
	parser.add_argument("--all", action="store_true",
	help="compare all schemes")
	args = parser.parse_args()
	# Check for and report level8 errors
	if not os.path.isdir(args.themes):
		Logger().logPrint(args.themes + " is not a valid directory", LogType.ERROR)
		sys.exit(1)

	# Windows has crap colour support to use this
	if platform.system() == "Windows":
		kernel32 = ctypes.windll.kernel32
		kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


	files = {}
	for theme in os.listdir(args.themes):
		key = theme.replace(".json", "").replace("base16-", "").replace("base24-", "")
		if key in files:
			files[key].append(theme)
		else:
			files[key] = [theme]


	# Check for b16 and b24 variant of a file
	for key in files:
		if len(files[key]) == 2: # Both variants
			Logger().logPrint(key, LogType.HEADER)
			Logger().logPrint("  B     W   R Y   G C B M ", LogType.BOLD)
			if "base16-" in files[key][0]: # First one is base16
				printColours(os.path.join(args.themes, files[key][0]))
				printColours(os.path.join(args.themes, files[key][1]))
			else:
				printColours(os.path.join(args.themes, files[key][1]))
				printColours(os.path.join(args.themes, files[key][0]))
		elif args.all:
			Logger().logPrint(files[key][0].replace(".json", ""), LogType.HEADER)
			Logger().logPrint("  B     W   R Y   G C B M ", LogType.BOLD)
			printColours(os.path.join(args.themes, files[key][0]))




if __name__ == "__main__":
	main()
