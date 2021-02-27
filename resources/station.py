from flask_restful import Resource, reqparse, request
from models.station import StationModel

import csv
import string
import time


class Station(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('gw_id',
		type=str,
		required=True,
		help='The gw id cannot be left blank'
		)
	parser.add_argument('ss_site',
		type=str,
		required=True,
		help='The ss site cannot be left blank'
		)
	parser.add_argument('ss_num',
		type=int,
		required=True,
		help='The ss num cannot be left blank'
		)

	parser.add_argument('ss_locate',
		type=str,
		required=True,
		help='The ss locate cannot be left blank'
		)
	parser.add_argument('ss_vwcIdShlw',
		type=str,
		required=True,
		help='The ss vwcIdShlw cannot be left blank'
		)
	parser.add_argument('ss_vwcIdMid',
		type=str,
		required=True,
		help='The ss vwcIdMid cannot be left blank'
		)
	parser.add_argument('ss_vwcIdDeep',
		type=str,
		required=True,
		help='The ss vwcIdDeep cannot be left blank'
		)
	parser.add_argument('ss_phId',
		type=str,
		required=True,
		help='The ss phId cannot be left blank'
		)
	parser.add_argument('ss_co2Id',
		type=str,
		required=True,
		help='The ss co2Id cannot be left blank'
		)
	parser.add_argument('ss_tempId',
		type=str,
		required=True,
		help='The ss tempId cannot be left blank'
		)
	parser.add_argument('ss_bmeId',
		type=str,
		required=True,
		help='The ss bmeId cannot be left blank'
		)

	def get(self, ss_id):
		station = StationModel.find_by_id(ss_id)
		if station:
			return station.json()
		return {'message': 'Sensor Station not found'}, 404

class StationMod(Resource):
	#insert or update an item
	def post(self):
		#form data
		data = request.form
		ss_id = data['ss_id']
		if StationModel.find_by_id(ss_id):
			return {'message': "Sensor Station with id '{}' already exists.".format(ss_id)}, 400

		data = Station.parser.parse_args()
		with open("metadata.csv", "a", ) as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([time.ctime(), ss_id, *data.values()])

		station = StationModel(ss_id, **data)

		try:
			station.save_to_db()
		except:
			return{'message': 'An error occurred while creating the sensor station'}, 500

		return station.json(), 201
		#return {'message': 'Node added or updated'}, 201

	def put(self):
		data = request.form
		ss_id = data['ss_id']

		station = StationModel.find_by_id(ss_id)

		if station is None:
			station = StationModel(**data)
		else:
			station.ss_id = data['ss_id']
			station.gw_id = data['gw_id']
			station.ss_site = data['ss_site']
			station.ss_num = data['ss_num']
			station.ss_locate = data['ss_locate']
			station.ss_vwcIdShlw = data['ss_vwcIdShlw']
			station.ss_vwcIdMid = data['ss_vwcIdMid']
			station.ss_vwcIdDeep = data['ss_vwcIdDeep']
			station.ss_phId = data['ss_phId']
			station.ss_co2Id = data['ss_co2Id']
			station.ss_tempId = data['ss_tempId']
			station.ss_bmeId = data['ss_bmeId']

		station.save_to_db()

		return station.json()

	def delete(self):

		data = request.form
		station_id = data['ss_id']
		station = StationModel.find_by_id(station_id)
		if station:
			station.delete_from_db()
		return {'message': 'Sensor Station deleted.'}


class StationList(Resource):
	def get(self):
		return [station.json() for station in StationModel.query.all()]
