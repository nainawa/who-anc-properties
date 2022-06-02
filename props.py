# WHO ANC Properties
# ==============================================================================
# A tool written in Python to help developers translate WHO ANC (Antenatal Care)
# mobile application easier.
# ------------------------------------------------------------------------------
# Author		https://github.com/nainawa
# Repository	https://github.com/nainawa/who-anc-properties
# Version		1.0 - June 2, 2022
# ==============================================================================

# [*] Imports
# ==============================================================================
import sys
import os
import shutil
import re
import csv

# [*] Global Variables
# ==============================================================================
langs = []
properties = []
generated_props = 0

# [*] Default Configuration
# ==============================================================================
default_lang = "en"
properties_dir = "opensrp-anc/src/main/resources/"
csv_dir = "csv/"
output_dir = "properties/"

# [*] Functions
# ==============================================================================

# [ Write .csv file ]
# This function will create .csv file according to the .properties
# file content


def write_csv(prop_name, dict):
	# CSV file configuration
	output_path = csv_dir + prop_name + ".csv"
	output_file = open(output_path, "w", newline="")
	csv_writer = csv.writer(output_file, delimiter=";")

	# Write CSV header row
	langs = []
	csv_header = ["key"]
	csv_rows = []

	# Sort keys alphabetically
	sorted_dict = sorted(dict.keys(), key=lambda x: x.lower())

	# Write CSV rows
	for key in dict:
		row = [key]
		for lang in dict[key]:
			if lang not in langs:
				langs += [lang]
			lang_index = langs.index(lang) + 1
			if len(row) <= lang_index:
				row += [""]
				row[lang_index] = dict[key][lang]
		csv_rows += [row]

	csv_header += langs
	
	csv_writer.writerow(csv_header)
	csv_writer.writerows(csv_rows)

def process_prop_file(dir, prop_name, properties, dict = {}, lang = "default"):
	file_path = dir + prop_name + ".properties"
	input_file = open(file_path, "r")
	file_lines = input_file.readlines()

	# Parse through lines to get property key
	for line in file_lines:

		if line != "\n" and line[0] != "#":
			# Get key and value
			splitted = line.strip().split("=")
			key = splitted[0].rstrip()
			value = ""
			if len(splitted) > 1:
				value = splitted[1].lstrip()

			# Add to dictionary
			if key not in dict:
				dict[key] = {}

			dict[key][lang] = value

	# Parse translation .properties
	for prop in properties:
		match = re.search(rf"{re.escape(prop_name)}_\w+", prop)
		if match:
			match_name = match.group()
			match_split = match_name.split("_")
			match_lang = match_split[len(match_split) - 1]
			properties.remove(match_name)
			process_prop_file(dir, match_name, properties, dict, match_lang)

def run_convert(source_dir):
	# Check source directory
	props_dir = source_dir + "/" + properties_dir
	
	# Directory doesn't exist
	if not os.path.isdir(props_dir):
		print("Directory '{}' doesn't exist.".format(props_dir))

	# Read .properties file
	else:
		with os.scandir(props_dir) as files:
			properties = []
			
			# Process files inside the directory
			for file in files:
				# Check file extension
				filename = file.name.split(".")
				if len(filename) > 1:
					prop_name = file.name.split(".")[0]
					ext = file.name.split(".")[1]
					
					# Only process .properties files
					if ext == "properties":
						properties += [prop_name]

			# Further checking before processing
			if len(properties) == 0:
				print("No .properties files found.")
			else:
				properties.sort()
				print("Found {} .properties file(s).".format(len(properties)))
				print("\nStart converting .properties to CSV...\n")
				for prop in properties:
					dict = {}
					process_prop_file(props_dir, prop, properties, dict)

					# Create CSV file
					write_csv(prop, dict)
					print("- {}.csv ~".format(prop), len(dict), "row(s)")

				print("\nGenerated {} CSV files.".format(len(properties)))

# [ Write .properties files ]
def write_properties(prop_name, dict):
	global generated_props

	print("- Converting '{}.csv' file to .properties file(s)...".format(prop_name))

	for lang in dict:
		if lang == default_lang:
			filename = prop_name + ".properties"
		else:
			filename = prop_name + "_" + lang + ".properties"

		with open(output_dir + filename, "w") as output:
			for row in dict[lang]:
				output.write(row[0])
				output.write(" = ")
				output.write(row[1])
				output.write("\n")
			output.close()
			generated_props += 1

def run_generate():
	if os.path.isdir(csv_dir):
		with os.scandir(csv_dir) as files:
			csv_count = 0
			csv_files = []
			# Process files inside the directory
			for file in files:
				# Check file extension
				filename = file.name.split(".")
				if len(filename) > 1:
					prop_name = file.name.split(".")[0]
					ext = file.name.split(".")[1]

					# Only process .csv files
					if ext == "csv":
						csv_count += 1
						csv_files += [{
							"prop_name": prop_name,
							"path": file.path
						}]

			# Stop processing if there's no CSV file inside the directory
			if csv_count == 0:
				print("No CSV files found inside '{}' directory.".format(csv_dir))
			# Start processing CSV files
			else:
				print("Found {} CSV file(s). Generating .properties files...\n".format(csv_count))
				missing_count = 0

				for cfile in csv_files:
					dict = {}
					missing_lines = []

					with open(cfile["path"]) as csv_file:
						csv_reader = csv.reader(csv_file, delimiter=";")
						line = 0
						header = []
						for row in csv_reader:
							missing = False
							# Set header row
							if line == 0:
								header = row
							# Process content rows
							else:
								key = row[0]

								# Process each row
								for x in range(0, len(row)):
									if x > 0:
										if row[x] == "":
											missing = True
										else:
											if header[x] not in dict:
												dict[header[x]] = []
											dict[header[x]] += [[key, row[x]]]

							if missing:
								missing_lines += [line + 1]

							line += 1

					# Don't write properties file if there's missing translation
					if (len(missing_lines) > 0):
						lines = ", ".join(str(v) for v in missing_lines)
						print("\n! " + prop_name)
						print("  {} missing translation(s) on following line(s):".format(
							len(missing_lines)))
						print("  {}".format(lines))
						print("\n")
						missing_count += 1

					# Write .properties file
					else:
						write_properties(cfile["prop_name"], dict)
				
				print("\nGenerated {} .properties file(s) successfully.".format(generated_props))
				if missing_count > 0:
					print("Failed because of missing translations:", missing_count)
	else:
		print("Directory '{}' is missing. Run the 'convert' command first to generate CSV files.".format(csv_dir))

# [*] Main Program
# ==============================================================================
def main():
	print("\n")
	args = sys.argv

	# Check user command
	if len(args) < 2:
		print("Please provide a command.")

	elif args[1] == "convert":
		if len(args) < 3:
			print("Please provide a path of WHO ANC Android app source code.")
			print("Usage	: python props.py <source_directory>")
			print("Example	: python props.py ~/who-anc-client")
		else:
			# Delete output folder if exists
			if (os.path.isdir(csv_dir)):
				shutil.rmtree(csv_dir)
			# Create output folder
			os.mkdir(csv_dir)
			run_convert(args[2])

	elif args[1] == "generate":
		# Delete output folder if exists
		if (os.path.isdir(output_dir)):
			shutil.rmtree(output_dir)
		# Create output folder
		os.mkdir(output_dir)
		run_generate()

	else:
		print("Invalid command '{}'.".format(args[1]))

	print("\n")

# ==============================================================================
main()