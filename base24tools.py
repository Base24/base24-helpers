"""process a base24 dict using a lookup table to translate the source theme
onto the base24 scheme
"""
import sys
from metprint import (
	LogType,
	Logger
)

def process(base24, base24lookup, sourceThemeDict, bgNumber, fgNumber):
	"""process a base24 dict using a lookup table to translate the source theme
	onto the base24 scheme

	Args:
		base24 (dict): a dictionary representing a base24 scheme
		base24lookup (dict): a dictionary mapping base24 colour ids to the
		respective key in the sourceThemeDict
		sourceThemeDict (dict): a dictionary representing the source theme/
		scheme
		bgNumber (int): lower base0N bound for the background 0-9
		fgNumber (int): upper base0N bound for the foreground 0-9. Must be
		greater than bgNumber

	Returns:
		dict: base24 dict to write to scheme file
	"""
	if fgNumber not in range(0, 10) or bgNumber not in range(0, 10):
		Logger().logPrint("fgNumber and bgNumber must be between 0 and 9", LogType.ERROR)
		sys.exit(1)
	if fgNumber < bgNumber:
		Logger().logPrint("fgNumber must be larger than bgNumber", LogType.ERROR)
		sys.exit(1)
	# Keys apart from base03, base04, base05, base0F, base10, base11 can be
	# taken from iterm
	for key in base24lookup:
		base24[key] = sourceThemeDict[base24lookup[key]]

	# Is it really a base16 theme? Compare red and bright red to find out
	if base24["base08"] == base24["base12"]:
		Logger().logPrint("\"" + base24["scheme"] + "\" is a base16 theme", LogType.WARNING)
		base24["scheme"] = "b16" + base24["scheme"]

	# Keys fg to fg (not including), base0F, base10, base11 can be calculated
	#Background through Foreground
	bg = base24["base0" + str(bgNumber)]
	fg = base24["base0" + str(fgNumber)]
	for index in range(bgNumber + 1, fgNumber):
		mult = index - bgNumber
		baseVal = []
		for section in range(0, 5, 2):
			baseVal.append("{:02x}".format(int(bg[0+section:2+section], 16) + int(
				(int(fg[0+section:2+section], 16) - int(bg[0+section:2+section], 16)) *
				mult / (fgNumber - bgNumber)
				)
			))
		base24["base0"+str(index)] = "".join(baseVal)

	#Darker and darkest backgrounds
	for index in range(10, 12):
		mult = 12 - index
		baseVal = []
		for section in range(0, 5, 2):
			baseVal.append("{:02x}".format(int(int(base24["base00"][0+section:2+section], 16) * mult / 3)
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
