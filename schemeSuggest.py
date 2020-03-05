
import argparse
import difflib
import diff_match_patch as dmp_module


def getColourMap(line1, line2):
	diff = difflib.SequenceMatcher(None, line1, line2)
	colourMap = []
	dmp = dmp_module.diff_match_patch()
	dmp.Diff_Timeout = 10
	diff = dmp.diff_main(line1, line2)
	dmp.diff_cleanupSemantic(diff)

	for index in range(len(diff)):
		if diff[index][0] == -1:
			colourMap = (tuple(diff[index][1].split(",")), tuple(diff[index+1][1].split(",")))

	return colourMap


def schemeSuggest(template, theme, mode):
	# Read lines and ignore blank lines (other different lines will cause issues)
	template_lines_d = open(template, "r").readlines()
	template_lines = [template_lines_d[i] for i in range(len(template_lines_d)) if len(template_lines_d[i].strip()) > 0]
	theme_lines_d = open(theme, "r").readlines()
	theme_lines = [theme_lines_d[i] for i in range(len(theme_lines_d)) if len(theme_lines_d[i].strip()) > 0]

	colours = []
	for index in range(len(theme_lines)):
		colours.append(getColourMap(template_lines[index], theme_lines[index]))

	unique = [list(x) for x in set(tuple(x) for x in colours)]
	for element in unique:
		if len(element) > 0:
			try:
				print(element[0][0][2:8], end=": ")
				if "reverse" in mode:
					colour = element[1][::-1]
				else:
					colour = element[1]

				if "rgb" in mode:
					colour = hex(int(colour[0]))[2:4]+hex(int(colour[1]))[2:4]+hex(int(colour[2]))[2:4]
				elif "dec" in mode:
					colour = hex(int(colour[0])*255)[2:4]+hex(int(colour[1])*255)[2:4]+hex(int(colour[2])*255)[2:4]

				print("\033["+ ";".join(["48","2",str(int(colour[0:2], 16)),str(int(colour[2:4], 16)),str(int(colour[4:6], 16))]) + "m     \033[0m #" + colour)
			except:
				pass


if __name__ == "__main__":
	"""Main method, do argparsing and call schemeSuggest
	"""
	parser = argparse.ArgumentParser("schemeSuggest",
	description="Pair colours with base24 colour ids")
	parser.add_argument("template",
	help="relative or abs path to the base24 template")
	parser.add_argument("theme",
	help="relative or abs path to the theme file")
	parser.add_argument("--mode", action="store", default="hexhash",
	help="color format: hex (ff00aa), reversehex (aa00ff), rgb (255,0,170), reversergb (170,0,255), dec (1.0,0,0.666), reversedec (0.666,0,1.0)")

	args = parser.parse_args()
	schemeSuggest(args.template, args.theme, args.mode)
