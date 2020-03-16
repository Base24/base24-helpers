"""Convert .itermcolors to base24 scheme
"""

import sys
import defusedxml.ElementTree as ET
import yaml

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
		r = int(float(dicts[i][1].text) * 255.0)
		g = int(float(dicts[i][3].text) * 255.0)
		b = int(float(dicts[i][5].text) * 255.0)
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
		"base01": "Ansi 0 Color",
		"base02": "Ansi 8 Color",
		"base06": "Ansi 7 Color",
		"base07": "Ansi 15 Color",
		"base08": "Ansi 1 Color",
		"base09": "Ansi 3 Color",
		"base0A": "Ansi 12 Color",
		"base0B": "Ansi 2 Color",
		"base0C": "Ansi 6 Color",
		"base0D": "Ansi 4 Color",
		"base0E": "Ansi 5 Color",
		"base12": "Ansi 10 Color",
		"base13": "Ansi 12 Color",
		"base14": "Ansi 11 Color",
		"base15": "Ansi 14 Color",
		"base16": "Ansi 9 Color",
		"base17": "Ansi 13 Color",
	}

	# Keys apart from base03, base04, base05, base0F, base10, base11 can be
	# taken from iterm
	for key in base24lookup:
		base24[key] = iterm[base24lookup[key]]

	# Keys base03, base04, base05, base0F, base10, base11 can be calculated
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

	for index in range(10, 12):
		mult = 12 - index
		baseVal = []
		for section in range(0, 5, 2):
			baseVal.append("{:02x}".format(int(int(bg[0+section:2+section], 16) * mult / 3)
			))
		base24["base"+str(index)] = "".join(baseVal)

	baseVal = []
	for section in range(0, 5, 2):
		baseVal.append("{:02x}".format(int(int(base24["base08"][0+section:2+section], 16) / 2)
		))
	base24["base0F"] = "".join(baseVal)

	return base24


def main():
	''' Main entry point for cli '''
	if len(sys.argv) < 2:
		print("usage: ./convert_itermcolors.py file.itermcolors")
		sys.exit(1)

	filename = sys.argv[1]
	tree = ET.parse(filename)

	base24 = genBase24(filename, iterm2hex(tree.getroot()))


	with open(base24["scheme"]+".yml", "w") as outfile:
		yaml.dump(base24, outfile)

if __name__ == '__main__':
	main()
