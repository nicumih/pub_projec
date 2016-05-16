from flask import Flask, render_template, redirect, url_for,send_from_directory, request, session, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug import secure_filename
import os
app = Flask(__name__)

app.secret_key = "inteligent post"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///panourile.db'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'img/'
#functions 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



#create sqla object
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from models import *

@app.route('/')
def home():
	return 'server'

@app.route('/panouri')
def panouri():
	panour = panourile.query.all()
	return render_template('index.html',panouri=panour)

	
@app.route('/add',methods = ['GET', 'POST'])
def add():
	error = None
	if request.method == 'POST':
		p = request.form['name']
		idl = request.form['id']
		if p!='' and idl!='':
				db.session.add(panourile(p,idl))
				db.session.commit()
				return redirect(url_for('panouri'))
		else: error = 'complete every input'
	return render_template('panou.html',error=error)


@app.route('/temperature',methods = ['GET','POST'])
def temperature():
	if request.method == 'GET':
		name = request.args.get('name')
		temperature = request.args.get('t')
		c = panourile.query.filter_by(id_init = name).first()
		c.temperatura = temperature
	return redirect(url_for('panouri'))
@app.route('/<int:id>',methods = ['GET'])
def panou(id):
    q = panourile.query.filter_by(id = id).first()
    return render_template('panour.html',q = q)

@app.route('/upload',methods = ['GET','POST'])
def upload():
	if request.method == 'POST':
		ip = request.form['id']
		file = request.files['file']
		if file and allowed_file(file.filename):
			db.session.add(imagini(ip))
			db.session.commit()
			obj = imagini.query.order_by(imagini.id.desc()).first()
			name = str(obj.id) + '.' + file.filename.rsplit('.', 1)[1]
			obj.name = name
			filename = secure_filename(name)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			return redirect(url_for('uploaded_file',filename=filename))
	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
      	<input type="text" name=id placeholder=id />
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/accidente', methods = ['GET','POST'])
def accidente():
	if request.method == 'GET':
		a   = request.args.get('a')
		ip = request.args.get('ip')
		c = panourile.query.filter_by(id_init = ip).first()
		c.accident = a
		return redirect(url_for('panouri'))



#here goes slider
@app.route('/runer',methods = ['GET'])
def runer():
	r = request.args.get('r')
	img = imagini.query.filter_by(id_p = r).all()
	return render_template('slider.html',img=img)



@app.route('/delete',methods = ['GET'])
def delete():
	k = request.args.get('id')
	p = panourile.query.filter_by(id = k).first()
	imagini.query.filter_by(id_p = p.id_init).delete()
	panourile.query.filter_by(id=k).delete()
	return redirect(url_for('panouri'))


if __name__ == "__main__":
	app.run(debug=True)
 