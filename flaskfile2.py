import os
import os.path as op
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session, abort, g
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, 'server.db'),
#     DEBUG=True,
#     SECRET_KEY='development key',
#     USERNAME='admin',
#     PASSWORD='default'
# ))
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
UPLOAD_FOLDER = 'templates/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'PNG' , 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()

# @app.route('/')
# def show_entries():
#     db = get_db()
#     cur = db.execute('select title, text from entries order by id desc')
#     entries = cur.fetchall()
#     return render_template('show_entries.html', entries=entries)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)
#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))
#
# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))
#
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/directory')
# def dirtree():
#     path = os.path.expanduser(u'~/PycharmProjects/Project OneDir/templates/uploads')
#     return render_template('directory.html', tree=make_tree(path))

# Route that will process the file upload
@app.route('/upload/<filename>/', methods=['POST'])
def uploadfileinsub(filename):
    filenamesplit = filename.split('/')
    path = UPLOAD_FOLDER
    for i in range(0,len(filenamesplit)):
        path += filenamesplit[i] + '/'
        if not os.path.exists(path):
            os.mkdir(path)
    # Check if the file is one of the allowed types/extensions
    #
    # if file and allowed_file(file.filename):
    #     # Make the filename safe, remove unsupported chars
    #     filename = secure_filename(file.filename)
    #     # Move the file form the temporal folder to
    #     # the upload folder we setup
    #     app.config['UPLOAD_FOLDER']=path
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
@app.route('/uploadsa', methods=['POST'])
def upload():

    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions

    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basically show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))


# def make_tree(path):
#     tree = dict(name=os.path.basename(path), children=[])
#     try: lst = os.listdir(path)
#     except OSError:
#         pass #ignore errors
#     else:
#         for name in lst:
#             fn = os.path.join(path, name)
#             if os.path.isdir(fn):
#                 tree['children'].append(make_tree(fn))
#             else:
#                 tree['children'].append(dict(name=name))
#         itemlist = []
#         for item in tree['children']:
#             if(item!=None):
#                 itemlist.append(item['name'])
#         for item in itemlist:
#             print(item)
#     return tree
#
#
#

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/delete', methods=['POST'])
def delete():
    # Get the name of the uploaded file
    print request.data
    file = request.data
    print file
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)

        return redirect(url_for('delete_file',
                                filename=filename))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    path = UPLOAD_FOLDER + filename
    print path
    if op.exists(path):
        os.remove(path)



if __name__ == '__main__':
    app.run()
