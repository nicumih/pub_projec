from app import db
from models import panourile,imagini
db.drop_all()
#database creating 
db.create_all()



db.session.add(panourile('1','0.0.0.1'))
db.session.add(imagini('0.0.0.1'))
db.session.add(panourile('2','0.0.0.2'))

#commit
db.session.commit()
 