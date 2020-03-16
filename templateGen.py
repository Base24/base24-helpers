"""Base24 2020
Genrate a base24 template from a theme and a scheme
"""
import argparse
import re
import yaml

def get_yaml_dict(yaml_file):
	"""Return a yaml_dict from reading yaml_file. If yaml_file is empty or
	doesn't exist, return an empty dict instead."""
	try:
		with open(yaml_file, "r") as file_:
			yaml_dict = yaml.safe_load(file_.read()) or {}
		return yaml_dict
	except FileNotFoundError:
		return {}

def reverse_hex(hex_str):
	"""Reverse a hex foreground string into its background version."""
	hex_str = "".join([hex_str[i : i + 2] for i in range(0, len(hex_str), 2)][::-1])
	return hex_str


def fuzzReplaceOne(parts_fuzz, replaceWith, outText, mode):
	"""Find and replace for one enumerated colour

	Args:
		parts_fuzz (int[]): red (blue if reversed), green, blue (red if reversed)
		replaceWith (str): the colour id
		outText (str): text to find and replace
		mode (str): colour mode

	Returns:
		str: text with find and replace done
	"""
	if "hex" in mode:
		replaceText = re.compile(re.escape(
			"{:02x}".format(parts_fuzz[0])+"{:02x}".format(parts_fuzz[1])+"{:02x}".format(parts_fuzz[2])[2:4]
		), re.IGNORECASE)
		outText = replaceText.sub("{{"+replaceWith+"-hex}}", outText)
	elif "dec" in mode:
		# Round and do extras
		part0_dec = parts_fuzz[0]/255
		part1_dec = parts_fuzz[1]/255
		part2_dec = parts_fuzz[2]/255
		for decimalPlaces in range(2, 9):
			replaceText = re.compile(re.escape(
				str(round(part0_dec, decimalPlaces))+","+
				str(round(part1_dec, decimalPlaces))+","+
				str(round(part2_dec, decimalPlaces))
			), re.IGNORECASE)
		outText = replaceText.sub("{{"+replaceWith+"-dec-r}},{{"+
			replaceWith+"-dec-g}},{{"+replaceWith+"-dec-b}}", outText)

		# As with others
		replaceText = re.compile(re.escape(
			str(part0_dec)+","+str(part1_dec)+","+str(part2_dec)
		), re.IGNORECASE)
		outText = replaceText.sub("{{"+replaceWith+"-dec-r}},{{"+
		replaceWith+"-dec-g}},{{"+replaceWith+"-dec-b}}", outText)
	else:
		replaceText = re.compile(re.escape(
			str(parts_fuzz[0])+","+str(parts_fuzz[1])+","+str(parts_fuzz[2])
		), re.IGNORECASE)
		outText = replaceText.sub("{{"+replaceWith+"-rgb-r}},{{"+
		replaceWith+"-rgb-g}},{{"+replaceWith+"-rgb-b}}", outText)

	return outText


def fuzzReplace(schemeDict, key, fuzz, outText, mode):
	"""Replace colour(s) with a single base24 colour id

	Args:
		schemeDict (dict): scheme as a python dictionary
		key (str): colour id
		fuzz (int): +- by
		outText (str): text to do find and replace on
		mode (str): colour mode

	Returns:
		str: text with find and replace done
	"""
	if "reverse" in mode:
		colour = reverse_hex(schemeDict[key])
	else:
		colour = schemeDict[key]
	part0 = int(colour[0:2], 16) - fuzz
	part1 = int(colour[2:4], 16) - fuzz
	part2 = int(colour[4:6], 16) - fuzz

	for part0_fuzz in range(part0, part0 + fuzz * 2 + 1):
		for part1_fuzz in range(part1, part1 + fuzz * 2 + 1):
			for part2_fuzz in range(part2, part2 + fuzz * 2 + 1):
				outText = fuzzReplaceOne([part0_fuzz, part1_fuzz, part2_fuzz], key, outText, mode)

	return outText


def templateGen(scheme, theme, mode="hex", fuzz=0):
	"""Generate a template for a given file

	Args:
		scheme (file): yaml dictionary containing colours
		theme (file): file containing theme colours
		mode (str, optional): colour mode. Defaults to "hex".
		fuzz (int, optional): +- colors for themes that have slight shades.
		Defaults to 0.
	"""
	schemeDict = get_yaml_dict(scheme)

	outText = open(theme, "r").read()
	schemeDict.pop("scheme")
	schemeDict.pop("author")

	for key in schemeDict:
		outText = fuzzReplace(schemeDict, key, fuzz, outText, mode)

	print(outText)


if __name__ == "__main__":
	"""Main method, do argparsing and call templateGen
	"""
	parser = argparse.ArgumentParser("templateGen",
	description="Generate a base24 template from an existing scheme and a theme file")
	parser.add_argument("colour_scheme",
	help="relative or abs path to the base24 colour scheme")
	parser.add_argument("theme",
	help="relative or abs path to the theme file")
	parser.add_argument("--mode", action="store", default="hexhash",
	help="""color format: hex (ff00aa), reversehex (aa00ff), rgb (255,0,170),
	reversergb (170,0,255), dec (1.0,0,0.666), reversedec (0.666,0,1.0)""")
	parser.add_argument("--fuzz", action="store", default=0,
	help="find 'close' colours and replace these ((r,g,b)+-fuzz: default=0, max-recommended=5)")
	args = parser.parse_args()
	templateGen(args.colour_scheme, args.theme, args.mode, int(args.fuzz))
