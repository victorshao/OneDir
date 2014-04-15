import os
import os.path as op
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session, abort, g
from werkzeug.utils import secure_filename
import shutil
import sqlite3
app = Flask(__name__)
UPLOAD_FOLDER = 'templates/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'PNG' , 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/uploadfile/', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/upload/<filename>/', methods=['POST'])
def uploadfileinsub(filename):
    filenamesplit = filename.split('\\')
    path = UPLOAD_FOLDER
    for i in range(0,len(filenamesplit)):
        path += filenamesplit[i] + '/'
        if not os.path.exists(path):
            os.mkdir(path)
@app.route('/move/<filename>', methods=['POST'])
def move(filename):
    filenamesplit = filename.rpartition("\\")
    uploadfileinsub(filenamesplit[0])
    shutil.move(UPLOAD_FOLDER+filenamesplit[2], UPLOAD_FOLDER+filenamesplit[0]+filenamesplit[1])


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    path = UPLOAD_FOLDER + filename
    print path
    if op.exists(path):
        os.remove(path)

if __name__ == '__main__':
    app.run()
