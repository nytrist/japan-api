from db import db

class StationModel(db.Model):
	__tablename__ = 'stations'

	id = db.Column(db.Integer, primary_key=True)

#Sensor Station Meta data - device id, site location, station number, location and sensor ids
	ss_id = db.Column(db.String(20))
	gw_id = db.Column(db.ForeignKey('gateways.gw_id'))
	ss_site = db.Column(db.String(20))
	ss_num = db.Column(db.Integer)
	ss_locate = db.Column(db.String(20))
	ss_vwcIdShlw = db.Column(db.String(20))
	ss_vwcIdMid = db.Column(db.String(20))
	ss_vwcIdDeep = db.Column(db.String(20))
	ss_phId = db.Column(db.String(20))
	ss_co2Id = db.Column(db.String(20))
	ss_tempId = db.Column(db.String(20))
	ss_bmeId = db.Column(db.String(20))

	readings = db.relationship('ReadingModel', lazy='dynamic') # check timing - maybe better to remove lazy dynamic

	def __init__(self, ss_id, gw_id, ss_site, ss_num, ss_locate, ss_vwcIdShlw, ss_vwcIdMid, ss_vwcIdDeep, ss_phId, ss_co2Id, ss_tempId, ss_bmeId):
		self.ss_id = ss_id
		self.gw_id = gw_id
		self.ss_site = ss_site
		self.ss_num = ss_num
		self.ss_locate = ss_locate
		self.ss_vwcIdShlw = ss_vwcIdShlw
		self.ss_vwcIdMid = ss_vwcIdMid
		self.ss_vwcIdDeep = ss_vwcIdDeep
		self.ss_phId = ss_phId
		self.ss_co2Id = ss_co2Id
		self.ss_tempId = ss_tempId
		self.ss_bmeId = ss_bmeId


	def json(self):
		return{'ss_id': self.ss_id, 'gw_id':self.gw_id, 'ss_site': self.ss_site, 'ss_num': self.ss_num,'ss_locate': self.ss_locate,'ss_vwcIdShlw': self.ss_vwcIdShlw, 'ss_vwcIdMid': self.ss_vwcIdMid,'ss_vwcIdDeep': self.ss_vwcIdDeep,'ss_phId': self.ss_phId, 'ss_co2Id': self.ss_co2Id,'ss_tempId': self.ss_tempId,'ss_bmeId': self.ss_bmeId, 'readings': [reading.json() for reading in self.readings.all()]}
#search by serial number
	@classmethod
	def find_by_id(cls, ss_id):
		return cls.query.filter_by(ss_id=ss_id).first()

#insert new node
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

#delete node
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
