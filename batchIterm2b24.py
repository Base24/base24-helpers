"""Convert .itermcolors to base24 scheme in a directory
"""
import sys
import os
import yaml
import defusedxml.ElementTree as ET
import iterm2base24

def main():
	''' Main entry point for cli '''
	if len(sys.argv) < 2:
		print("usage: ./convert_itermcolors.py itermschemes")
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
		with open(os.path.join(directory, base24["scheme"]+".yml"), "w") as outfile:
			yaml.dump(base24, outfile)

if __name__ == "__main__":
	main()
