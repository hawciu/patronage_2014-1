#!/usr/bin/python
# -*- coding: UTF-8 -*-
import io, json

class SuperherosDatabase(object):
	def __init__(self, filename = "superheros.json"):
		self.filename = filename
		
	def get_all(self):
		try:
			json_file = open(self.filename, 'r')
			data = json.load(json_file)
			json_file.close()
		except IOError:
			return self.create_new_file()
		return data
		
	def update(self, src):
		json_file = open(self.filename, 'w')
		json.dump(src, json_file, indent=4)
		json_file.close()
		
	def create_new_file(self):
		json_file = open(self.filename, 'w')
		json.dump([], json_file)
		json_file.close()
		return []
