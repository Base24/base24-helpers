"""Generate a table to put in a scheme project readme
"""
import os
import sys
import argparse
import yaml
import pystache

# You may want to edit this to better suit your needs
template = '''
# base24-{{scheme-name-0}}-scheme

Base24 scheme for {{scheme-name}}

|baseNN|Colour|
|---|---|
|base00|![#](https://placehold.it/25/{{base00-hex}}/000000?text=+)
|base01|![#](https://placehold.it/25/{{base01-hex}}/000000?text=+)
|base02|![#](https://placehold.it/25/{{base02-hex}}/000000?text=+)
|base03|![#](https://placehold.it/25/{{base03-hex}}/000000?text=+)
|base04|![#](https://placehold.it/25/{{base04-hex}}/000000?text=+)
|base05|![#](https://placehold.it/25/{{base05-hex}}/000000?text=+)
|base06|![#](https://placehold.it/25/{{base06-hex}}/000000?text=+)
|base07|![#](https://placehold.it/25/{{base07-hex}}/000000?text=+)
|base08|![#](https://placehold.it/25/{{base08-hex}}/000000?text=+)
|base09|![#](https://placehold.it/25/{{base09-hex}}/000000?text=+)
|base0A|![#](https://placehold.it/25/{{base0A-hex}}/000000?text=+)
|base0B|![#](https://placehold.it/25/{{base0B-hex}}/000000?text=+)
|base0C|![#](https://placehold.it/25/{{base0C-hex}}/000000?text=+)
|base0D|![#](https://placehold.it/25/{{base0D-hex}}/000000?text=+)
|base0E|![#](https://placehold.it/25/{{base0E-hex}}/000000?text=+)
|base0F|![#](https://placehold.it/25/{{base0F-hex}}/000000?text=+)
|base10|![#](https://placehold.it/25/{{base10-hex}}/000000?text=+)
|base11|![#](https://placehold.it/25/{{base11-hex}}/000000?text=+)
|base12|![#](https://placehold.it/25/{{base12-hex}}/000000?text=+)
|base13|![#](https://placehold.it/25/{{base13-hex}}/000000?text=+)
|base14|![#](https://placehold.it/25/{{base14-hex}}/000000?text=+)
|base15|![#](https://placehold.it/25/{{base15-hex}}/000000?text=+)
|base16|![#](https://placehold.it/25/{{base16-hex}}/000000?text=+)
|base17|![#](https://placehold.it/25/{{base17-hex}}/000000?text=+)

proj-down

proj-community
'''

def get_yaml_dict(yaml_file):
	"""Return a yaml_dict from reading yaml_file. If yaml_file is empty or
	doesn't exist, return an empty dict instead."""
	try:
		with open(yaml_file, "r") as file_:
			yaml_dict = yaml.safe_load(file_.read()) or {}
		return yaml_dict
	except FileNotFoundError:
		return {}

def format_scheme(scheme):
	"""Change $scheme so it can be applied to a template."""
	scheme["scheme-name"] = scheme.pop("scheme")
	scheme["scheme-author"] = scheme.pop("author")
	scheme["scheme-name-0"] = scheme["scheme-name"].replace(" ", "-").replace("_", "-").lower()
	bases = ["base{:02X}".format(x) for x in range(0, 24)]
	for base in bases:
		scheme["{}-hex".format(base)] = scheme.pop(base)


def main():
	''' Main entry point for cli '''
	parser = argparse.ArgumentParser(
	description="Generate a table to put in a scheme project readme")
	parser.add_argument("scheme", action="store",
	help="base24 scheme file")

	args = parser.parse_args()
	# Check for and report level8 errors
	if not os.path.isfile(args.scheme):
		print(args.scheme + " is not a valid file")
		sys.exit(1)

	# Do the mustche template mangling and output to stdout
	scheme = get_yaml_dict(args.scheme)
	format_scheme(scheme)
	file_content = pystache.render(template, scheme)
	print(file_content)



if __name__ == "__main__":
	main()
