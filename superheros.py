#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.restful import Api, Resource, reqparse, fields, types
from datetime import datetime
from datasource import SuperherosDatabase

app = Flask(__name__)
api = Api(app)

# load superheros from file
db = SuperherosDatabase()
db_superheros = db.get_all()

superhero_fields = {
	'name': fields.String,
	'real_name': fields.String,
	'appearance_date': fields.DateTime,
	'web_page': fields.Url
}

class Superhero(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('name', required = True, type = superhero_name, location = 'json')
		self.reqparse.add_argument('real_name', required = True, type = superhero_real_name, location = 'json')
		self.reqparse.add_argument('appearance_date', required = True, type = superhero_appearance_date, location = 'json')
		self.reqparse.add_argument('web_page', type=types.url, help='web_page is not a valid URL', location = 'json')
		super(Superhero, self).__init__()

	def put(self, name):
		superhero = filter(lambda s: s['name'] == name, db_superheros)
		if len(superhero) == 0:
			abort(404)
		superhero = superhero[0]
		args = self.reqparse.parse_args()
		if (superhero_name_exist(name, args['name'])):
			return { 'message': "Invalid name, a superhero with the same name already exists" }, 400
		for k, v in args.iteritems():
			if v != None:
				superhero[k] = v
		db.update(db_superheros)
		return superhero, 200

	def delete(self, name):
		superhero = filter(lambda s: s['name'] == name, db_superheros)
		if len(superhero) == 0:
			abort(404)
		db_superheros.remove(superhero[0])
		db.update(db_superheros)
		return '', 204
         
	def get(self, name):
		superhero = filter(lambda s: s['name'] == name, db_superheros)
		if len(superhero) == 0:
			abort(404)
		return superhero[0]
   
class SuperheroList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('name', required = True, type = new_superhero_name, location = 'json')
		self.reqparse.add_argument('real_name', required = True, type = superhero_real_name, location = 'json')
		self.reqparse.add_argument('appearance_date', required = True, type = superhero_appearance_date, location = 'json')
		self.reqparse.add_argument('web_page', type=types.url, help='web_page is not a valid URL', location = 'json')
		super(SuperheroList, self).__init__()
		
	def post(self):
		args = self.reqparse.parse_args()
		superhero = {
			'name': args['name'],
			'real_name': args['real_name'],
			'appearance_date': args['appearance_date'],
			'web_page': args['web_page']
		}
		db_superheros.append(superhero)
		db.update(db_superheros)
		return superhero, 201
		 
	def get(self):
		return db_superheros
       
api.add_resource(Superhero, '/superheros/<string:name>')
api.add_resource(SuperheroList, '/superheros/')        

def superhero_name_exist(name, new_name):
	new_superhero = filter(lambda s: s['name'] == new_name, db_superheros)
	if (name != new_name and len(new_superhero)) > 0:
		return True
	return False  
	
# RequestParser custom types 
def new_superhero_name(value):
	if len(value) > 20:
		raise ValueError("Invalid name, the name should be less than 20 characters")
	superhero = filter(lambda s: s['name'] == value, db_superheros)
	if (len(superhero) > 0):
		raise ValueError("Invalid name, a superhero with the same name already exists")
	return value

def superhero_real_name(value):
	if len(value) > 50:
		raise ValueError("Invalid real_name, the real_name should be less than 50 characters")
	return value

def superhero_appearance_date(value):
	try:
		datetime.strptime(value, '%m-%Y')
	except ValueError:
		raise ValueError("Invalid appearance_date Incorrect data format, should be mm-yyyy")
	return value 

def superhero_name(value):
	if len(value) > 20:
		raise ValueError("Invalid name, the name should be less than 20 characters")
	return value

if __name__ == '__main__':
	app.run(debug=True)
