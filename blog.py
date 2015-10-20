#blog.py - serves as the controller in mvc


from flask import Flask, render_template, request, session, \
flash, redirect, url_for, g
import sqlite3
from functools import wraps


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
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/', methods = ['GET','POST'])
def login():
    error = None
    if request.method =='POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error ='Invalid Credentials. Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html',error = error)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/add', methods = ['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("Please enter a title and text")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('insert into posts (title, post) values (?, ?)', [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash('New post created')
        return redirect(url_for('main'))


@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], post = row[1]) for row in cur.fetchall()]
    g.db.close()

    return render_template('main.html', posts = posts)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True)
