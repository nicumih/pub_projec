from app import db

class panourile(db.Model):
	__TABLENAME__="panourile"
	id = db.Column(db.Integer, primary_key=True)
	temperatura = db.Column(db.String, nullable=False)
	nume  = db.Column(db.String, nullable=False)
	id_init = db.Column(db.Integer, nullable=False)
	accident = db.Column(db.String, nullable=False)
	def __init__(self,nume,id_init):
		self.nume = nume
		self.temperatura = '1'
		self.id_init = id_init
		self.accident = '0'
	def __repr__(self):
		return 'nume ' 

class imagini(db.Model):
	__TABLENAME__="publicitate"   
	id = db.Column(db.Integer,primary_key=True)
	id_p = db.Column(db.Integer,nullable = False)
	name = db.Column(db.String)
	def __init__(self,id_p):
		self.id_p = id_p
