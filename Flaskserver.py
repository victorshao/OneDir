import os
import os.path as op
import shutil
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session, abort, g
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'templates/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'PNG' , 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download/<path:filename>')
def download(filename):
    path = filename.rpartition('/')
    return send_from_directory(app.config['UPLOAD_FOLDER']+path[0], path[2])

@app.route('/uploadfile/<path:filename>', methods=['POST'])
def upload(filename):
    filenamesplit = filename.rpartition("/")
    uploadfileinsub(filenamesplit[0])
    f = request.files['file']
    if f and allowed_file(f.filename):
        path = UPLOAD_FOLDER
        path += filenamesplit[0]
        f.save(os.path.join(path, filenamesplit[2]))

@app.route('/upload/<path:filename>/', methods=['POST'])
def uploadfileinsub(filename):
    filenamesplit = filename.split('/')
    path = UPLOAD_FOLDER
    for i in range(0,len(filenamesplit)):
        path += filenamesplit[i] + '/'
        if not os.path.exists(path):
            os.mkdir(path)

@app.route('/delete/<path:filename>', methods=['POST'])
def delete_file(filename):
    if not filename == "public/":
        path = UPLOAD_FOLDER + filename
        if op.exists(path):
            if op.isdir(path):
                shutil.rmtree(path)
                os.rmdir(path)
                print op.exists(path)
            os.remove(path)


if __name__ == '__main__':
    app.run()
