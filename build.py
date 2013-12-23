#!/usr/bin/env python

import os
import re

BUILD_DIR = os.getcwd()
SITE_DIR = BUILD_DIR + "/site"

def get_template_file_name(template_name):
	return "templates/" + template_name + ".htmt"

def apply_each(match, data):
	data_key = match.group(1)
	if data_key in data:
		data_list = data[match.group(1)]
		text = match.group(2)
		result = ""
		for data_item in data_list:
			result += re.sub(r"\$({)?(\w+)(?(1)})",
			                 lambda match: get_data_value(match, data_item),
			                 text)
		return result
	return ""

def get_data_value(match, data):
	data_name = match.group(2)
	if data_name in data:
		return data[match.group(2)]
	return ""

def get_template_content(match, data):
	template_name = match.group(2)
	return expand_template(template_name, data).rstrip()

def expand_template(template_name, data):
	with open(get_template_file_name(template_name)) as template_file:
		template_content = template_file.read()

		while True:
			previous_content = template_content

			# Iterative data substitution
			template_content = re.sub(r"{each \$(\w+):(.+)}",
			                          lambda match: apply_each(match, data),
			                          template_content, flags = re.S)

			# Data substitution
			template_content = re.sub(r"@({)?(\w+)(?(1)})", 
			                          lambda match: get_template_content(match, data),
			                          template_content)

			# Template inclusion
			template_content = re.sub(r"\$({)?(\w+)(?(1)})",
			                          lambda match: get_data_value(match, data),
			                          template_content)

			if template_content == previous_content:
				break

		return template_content

def build():
	project_directory = os.path.dirname(os.path.realpath(__file__));
	os.chdir(project_directory)
	try:
		home_data = {
			'page': 'home',
			'bodyMicrodata': 'itemscope itemtype="Person"',
			'bodyMicrodataMeta': [{'name': 'jobTitle', 'content': 'Computer Science Student'},
			                      {'name': 'birthDate', 'content': '1990-09-15'}]
		}
		home_content = expand_template("root", home_data)

		if not os.path.exists(SITE_DIR):
			os.mkdir(SITE_DIR)

		home_file = open(SITE_DIR + "/index.htm", "w")
		home_file.write(home_content)
	except IOError as e:
		print("Template " + e.filename + " does not exist")

if __name__ == "__main__":
	build()
