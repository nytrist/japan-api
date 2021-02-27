from db import db

class GatewayModel(db.Model):
	__tablename__ = 'gateways'

	id = db.Column(db.Integer, primary_key=True)
	gw_id = db.Column(db.String(20))
	gw_site = db.Column(db.String(20))
	gw_locate = db.Column(db.String(20))

	stations = db.relationship('StationModel', lazy='dynamic')

	def __init__(self, gw_id, gw_site, gw_locate):
		self.gw_id = gw_id
		self.gw_site = gw_site
		self.gw_locate = gw_locate

	def json(self):
		return{'gw_id': self.gw_id, 'gw_site': self.gw_site, 'gw_locate': self.gw_locate, 'stations': [station.json() for station in self.stations.all()]} #may need to remove .all() if too slow

#search by gateway ID
	@classmethod
	def find_by_id(cls, gw_id):
		return cls.query.filter_by(gw_id=gw_id).first()

#insert new gateway, update existing gateway
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

#delete gateway
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
