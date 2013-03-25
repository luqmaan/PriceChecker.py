from pychecker import app
from pychecker.database import db_session
from pychecker.models import User
from flask import render_template
from flask import request



def debug():
    'http://flask.pocoo.org/snippets/21/'
    assert app.debug == False


@app.route('/')
def index():
    return render_template('index.html', name="ya")


@app.route('/register',  methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        u = User(request.form['username'], request.form['password'], "email", "phone", "twitter")
        db_session.add(u)
        db_session.commit()
        return render_template('register.html', error=error)
    elif request.method == 'GET':
        return render_template('register.html', error=error)
    else:
        return "error"


@app.route('/users')
def users():
    error = None
    db_users = User.query.all()
    return render_template('users.html', users=db_users, error=error)


@app.route('/login')
def login():
    return 'login'


@app.route('/logout')
def logout():
    return 'logout'


@app.route('/product/')
def product():
    return 'add new product or list all products'


@app.route('/product/<int:product_id>')
def product(product_id):
    return 'product %s' % (product_id)


@app.route('/user/')
def user():
    return 'add new user'


@app.route('/user/<username>')
def user(username):
    return 'user with name %s' % (username)
