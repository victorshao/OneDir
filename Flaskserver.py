import os
import os.path as op
import shutil
import sqlite3
import time
import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session, abort, g
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.expanduser('~/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'PNG' , 'jpg', 'jpeg', 'gif'])
DATABASE = 'history.db'

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
    os.mkdir(UPLOAD_FOLDER + 'public/')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download/<path:filename>')
def download(filename):
    filename = filename.replace("%20", " ")
    path = filename.rpartition('/')
    return send_from_directory(app.config['UPLOAD_FOLDER']+path[0], path[2])

@app.route('/uploadfile/<path:filename>', methods=['POST'])
def upload(filename):
    filename = filename.replace("%20", " ")
    type = "upload"
    time2 = time.time()
    time1 = datetime.datetime.fromtimestamp(time2).strftime('%Y-%m-%d %H:%M:%S')
    username = filename[:filename.find('/')]
    database = sqlite3.connect(UPLOAD_FOLDER + username + '\\' + DATABASE)
    with database:
        c = database.cursor()
        c.execute("INSERT INTO history VALUES(?,?,?,?)", (type, filename, time1, time2))

    filenamesplit = filename.rpartition("/")
    uploadfileinsub(filenamesplit[0])
    f = request.files['file']
    if f and allowed_file(f.filename):
        path = UPLOAD_FOLDER + filename
        with open(path, 'w+b') as f2:
            shutil.copyfileobj(f, f2)

@app.route('/upload/<path:filename>/', methods=['POST'])
def uploadfileinsub(filename):
    filename = filename.replace("%20", " ")
    type = "upload"
    filenamesplit = filename.split('/')
    username = filename[:filename.find('/')]
    database = sqlite3.connect(UPLOAD_FOLDER + username + '/' + DATABASE)
    path = UPLOAD_FOLDER
    with database:
        c = database.cursor()
        for i in filenamesplit:
            path += i + '/'
            if not os.path.exists(path):
                time2 = time.time()
                time1 = datetime.datetime.fromtimestamp(time2).strftime('%Y-%m-%d %H:%M:%S')
                c.execute("INSERT INTO history VALUES(?,?,?,?)", (type, path, time1, time2))
                os.mkdir(path)

@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    filename = filename.replace('%20', ' ')
    if not filename == "public/":
    	type = "delete"
    	username = filename[:filename.find('/')]
    	database = sqlite3.connect(UPLOAD_FOLDER + username + '\\' + DATABASE)
    	with database:
        	c = database.cursor
        	path = UPLOAD_FOLDER + filename
        	if op.exists(path):
            		time2 = time.time()
            		time1 = datetime.datetime.fromtimestamp(time2).strftime('%Y-%m-%d %H:%M:%S')
            		c.execute("INSERT INTO history VALUES(?,?,?,?)", (type, path, time1, time2))
            		if op.isdir(path):
                		shutil.rmtree(path)
            		else:
                		os.remove(path)

def create_table():
    database = sqlite3.connect(DATABASE)
    c = database.cursor()
    c.execute('''DROP TABLE IF EXISTS history''')
    c.execute('''CREATE TABLE history(type TEXT, file_name TEXT, formal_time TEXT, informal_time INT)''')
    c.close()


if __name__ == '__main__':
    create_table()
    app.run()
