from db import db

class ReadingModel(db.Model):
	__tablename__ = 'readings'

	reading_id = db.Column(db.Integer, primary_key=True)
	live_test = db.Column(db.String(10))
	gw_date_time = db.Column(db.String(25))

#gateway diagnostics
	gw_id = db.Column(db.ForeignKey('gateways.gw_id'))
	gw_rssi = db.Column(db.Integer)
	ss_rssi = db.Column(db.Integer)
	gw_conn_att = db.Column(db.Integer)
	gw_encl_temp = db.Column(db.Float(precision=2))
	gw_batt = db.Column(db.Float(precision=2))
	gw_solar_vol = db.Column(db.Float(precision=2))

#sensor station diagnostics

	ss_id = db.Column(db.ForeignKey('stations.ss_id'))
	#ss_num = db.Column(db.ForeignKey('stations.ss_num'))
	#ss_id = db.Column(db.String(10))
	ss_num = db.Column(db.String(10)) # maybe remove...
	ss_conn_att = db.Column(db.Integer)
	ss_send_fail = db.Column(db.Integer)
	ss_encl_temp = db.Column(db.Float(precision=2))
	ss_batt = db.Column(db.Float(precision=2))
	ss_solar_vol = db.Column(db.Float(precision=2))

#Ambient Weather - (BME)
	ss_air_temp = db.Column(db.Float(precision=2))
	ss_baro_press = db.Column(db.Float(precision=2))
	ss_air_humid = db.Column(db.Float(precision=2))
	ss_alt = db.Column(db.Float(precision=2))

# readings
	soil_vwcShlw = db.Column(db.Float(precision=6))
	soil_vwcMid = db.Column(db.Float(precision=6))
	soil_vwcDeep = db.Column(db.Float(precision=6))
	soil_ph = db.Column(db.Float(precision=2))
	soil_temp = db.Column(db.Float(precision=2))
	soil_co2 = db.Column(db.Float(precision=2))

	def __init__(self, live_test, gw_date_time, gw_id, gw_rssi, ss_rssi, gw_conn_att, gw_encl_temp, gw_batt, gw_solar_vol, ss_id, ss_num, ss_conn_att, ss_send_fail, ss_encl_temp, ss_batt, ss_solar_vol, ss_air_temp, ss_baro_press, ss_air_humid, ss_alt, soil_vwcShlw, soil_vwcMid, soil_vwcDeep, soil_ph, soil_temp, soil_co2):
		self.live_test = live_test
		self.gw_date_time = gw_date_time

#gw diagnostics
		self.gw_id = gw_id
		self.gw_rssi = gw_rssi
		self.ss_rssi = ss_rssi
		self.gw_conn_att = gw_conn_att
		self.gw_encl_temp = gw_encl_temp
		self.gw_batt = gw_batt
		self.gw_solar_vol = gw_solar_vol

#ss diagnostics
		self.ss_id = ss_id
		self.ss_num = ss_num
		self.ss_conn_att = ss_conn_att
		self.ss_send_fail = ss_send_fail
		self.ss_encl_temp = ss_encl_temp
		self.ss_batt = ss_batt
		self.ss_solar_vol = ss_solar_vol

#ambient temp
		self.ss_air_temp = ss_air_temp
		self.ss_baro_press = ss_baro_press
		self.ss_air_humid = ss_air_humid
		self.ss_alt = ss_alt

#sensor readings
		self.soil_vwcShlw = soil_vwcShlw
		self.soil_vwcMid = soil_vwcMid
		self.soil_vwcDeep = soil_vwcDeep
		self.soil_ph = soil_ph
		self.soil_temp = soil_temp
		self.soil_co2 = soil_co2

	# return reading as json
	def json(self):
		return{'reading_id': self.reading_id, 'live_test': self.live_test, 'gw_date_time': self.gw_date_time, 'gw_id': self.gw_id, 'gw_rssi': self.gw_rssi, 'ss_rssi': self.ss_rssi, 'gw_conn_att': self.gw_conn_att, 'gw_encl_temp': self.gw_encl_temp, 'gw_batt': self.gw_batt, 'gw_solar_vol': self.gw_solar_vol,'ss_id': self.ss_id, 'ss_num': self.ss_num, 'ss_conn_att': self.ss_conn_att, 'ss_send_fail': self.ss_send_fail,'ss_encl_temp': self.ss_encl_temp, 'ss_batt': self.ss_batt,'ss_solar_vol': self.ss_solar_vol,'ss_air_temp': self.ss_air_temp,'ss_baro_press': self.ss_baro_press, 'ss_air_humid': self.ss_air_humid, 'ss_alt': self.ss_alt,'soil_vwcShlw': self.soil_vwcShlw, 'soil_vwcMid': self.soil_vwcMid,'soil_vwcDeep': self.soil_vwcDeep,'soil_ph': self.soil_ph, 'soil_temp': self.soil_temp, 'soil_co2': self.soil_co2}
#search for readings by reading_id
	@classmethod
	def find_by_id(cls, reading_id):
		return cls.query.filter_by(reading_id=reading_id).first()

#insert new reading
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

#delete reading
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
