#!/usr/bin/env python

import os
import re
import functools

def get_template_file_name(template_name):
	return "templates/" + template_name + ".htmt"

def get_data_value(data, match):
	data_name = match.group(2)
	if data_name in data:
		return data[match.group(2)]
	return match.group(0)

def get_template_content(data, match):
	template_name = match.group(2)
	return expand_template(template_name, data).rstrip()

def expand_template(template_name, data):
	with open(get_template_file_name(template_name)) as template_file:
		template_content = template_file.read()

		while True:
			previous_content = template_content

			template_content_func = functools.partial(get_template_content, data)
			template_content = re.sub(r"@({)?(\w+)(?(1)})", template_content_func, template_content)

			data_value_func = functools.partial(get_data_value, data)
			template_content = re.sub(r"\$({)?(\w+)(?(1)})", data_value_func, template_content)

			if template_content == previous_content:
				break

		return template_content

def build():
	project_directory = os.path.dirname(os.path.realpath(__file__));
	os.chdir(project_directory)
	try:
		home_data = {
			'page': 'home',
			'bodyMicrodata': 'itemscope itemtype="Person"'
		}
		print(expand_template("root", home_data))
	except IOError as e:
		print("Template " + e.filename + " does not exist")

if __name__ == "__main__":
	build()
