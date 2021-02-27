from flask_restful import Resource, reqparse, request
from models.gateway import GatewayModel

import csv
import string
import time

class Gateway(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('gw_site',
		type=str,
		required=True,
		help='The gateway site cannot be left blank'
		)

	parser.add_argument('gw_locate',
		type=str,
		required=True,
		help='The gateway location cannot be left blank'
		)

	def get(self, gw_id):
		gateway = GatewayModel.find_by_id(gw_id)
		if gateway:
			return gateway.json()
		return {'message': 'Gateway not found'}, 404

class GatewayMod(Resource):
	def post(self):
		#data sending as form
		data = request.form
		gw_id = data['gw_id']
		if GatewayModel.find_by_id(gw_id):
			return {'message': "Gateway with id '{}' already exists.".format(gw_id)}, 400

		data = Gateway.parser.parse_args()
		with open("metadata.csv", "a", ) as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([time.ctime(), gw_id, *data.values()])

		gateway = GatewayModel(gw_id, **data)

		try:
			gateway.save_to_db()
		except:
			return{'message': 'An error occurred while creating the gateway'}, 500

		return gateway.json(), 201


	def put(self):
		data = request.form
		gw_id = data['gw_id']

		gateway = GatewayModel.find_by_id(gw_id)

		if gateway is None:
			gateway = GatewayModel(gw_id, data['gw_site'], data['gw_locate'])
		else:
			gateway.gw_site = data['gw_site']
			gateway.gw_locate = data['gw_locate']

		gateway.save_to_db()

		return gateway.json()


	def delete(self):
		#gw_id sent via form
		data = request.form
		gw_id = data['gw_id']
		gateway = GatewayModel.find_by_id(gw_id)
		if gateway:
			gateway.delete_from_db()

		return {'message': 'Gateway deleted'}

class GatewayList(Resource):
	def get(self):
		return [gateway.json() for gateway in GatewayModel.query.all()]
