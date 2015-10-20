#blog.py - serves as the controller in mvc


from flask import Flask, render_template, request, session, \
flash, redirect, url_for, g
import sqlite3

#configurations for the blog
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = '\xbb\x04\xeb\xea\xb0\xbel\xce\tDA\x84\xa1\xc8\xb4\x88\xb8(Z\xd8-b\xa3\x8e'


app = Flask(__name__)

#pulls all configurations; looks for uppercase variables
app.config.from_object(__name__)

#connect to db
def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

@app.route('/', methods = ['GET','POST'])
def login():
    error = None
    if request.method =='POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error ='Invalid Credentials. Please try again'
        else:
            session['loggin_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html',error = error)

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/logout')
def logout():
    session.pop('loggined_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)
