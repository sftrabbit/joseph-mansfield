#!/usr/bin/env python

import os
import re
import functools
import textwrap

def get_template_file_name(template_name):
	return "templates/" + template_name + ".htmt"

def apply_each(data, match):
	data_list = data[match.group(1)]
	text = match.group(2)
	result = ""
	for data_item in data_list:
		data_value_func = functools.partial(get_data_value, data_item)
		result += re.sub(r"\$({)?(\w+)(?(1)})", data_value_func, text)
	return result

def get_data_value(data, match):
	data_name = match.group(2)
	if data_name in data:
		return data[match.group(2)]
	return ""

def get_template_content(data, match):
	template_name = match.group(2)
	return expand_template(template_name, data).rstrip()

def expand_template(template_name, data):
	with open(get_template_file_name(template_name)) as template_file:
		template_content = template_file.read()

		while True:
			previous_content = template_content

			apply_each_func = functools.partial(apply_each, data)
			template_content = re.sub(r"{each \$(\w+):(.+)}", apply_each_func, template_content, flags = re.S)

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
			'bodyMicrodata': 'itemscope itemtype="Person"',
			'bodyMicrodataMeta': [{'name': 'jobTitle', 'content': 'Computer Science Student'},
			                      {'name': 'birthDate', 'content': '1990-09-15'}]
		}
		print(expand_template("root", home_data))
	except IOError as e:
		print("Template " + e.filename + " does not exist")

if __name__ == "__main__":
	build()
