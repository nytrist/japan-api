from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister

from resources.reading import Reading, ReadingAdd, ReadingList
from resources.station import Station, StationMod, StationList
from resources.gateway import Gateway, GatewayMod, GatewayList

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "jc"
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

#auth - if needed to implement
jwt = JWT(app, authenticate, identity)

#allow cross domain requests
CORS(app)

#GET
api.add_resource(Gateway, '/gateway/<string:gw_id>') #returns specific gateway
api.add_resource(Station, '/station/<string:ss_id>') #returns individual sensor stations
api.add_resource(Reading, '/reading/<string:reading_id>') #gets, deletes a specific reading

#GET ALL
api.add_resource(GatewayList, '/') # returns all gateways
api.add_resource(StationList, '/stations') # returns all sensor stations, index page of api
api.add_resource(ReadingList, '/readings') #returns all readings

#Add reading, add, delete gateway and sensor statoin
api.add_resource(ReadingAdd, '/reading') #posts reading with data in body
api.add_resource(GatewayMod, '/gateway') #adds, deletes a gw
api.add_resource(StationMod, '/station') #adds, deletes a station

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(host='0.0.0.0', port=5000, debug=True)
