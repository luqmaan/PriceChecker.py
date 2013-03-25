from pychecker import app
from pychecker.database import db_session
from pychecker.models import User
from pychecker import LoginManager
from flask import render_template
from flask import request
from flask import flash
from sqlalchemy.exc import IntegrityError
from pychecker.forms import LoginForm
from flask.ext.login import login_user


def debug():
    'http://flask.pocoo.org/snippets/21/'
    assert app.debug is False


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', name="ya")


@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        u = User(request.form['username'],
                 request.form['password'],
                 request.form['email'],
                 request.form['phone'],
                 request.form['twitter'])
        db_session.add(u)
        try:
            db_session.commit()
        except IntegrityError, e:
            error = "Sorry, the username " + request.form['username'] + " is already taken."
        except Exception, e:
            error = e
        return render_template('register.html', error=error)
    elif request.method == 'GET':
        return render_template('register.html', error=error)
    else:
        error = "An unknown error has occurred."
        return render_template('register.html', error=error)


@app.route('/users')
def users():
    error = None
    db_users = User.query.all()
    return render_template('users.html', users=db_users, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    'http://pythonhosted.org/Flask-Login/'
    error = None
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form, error=error)
    elif request.method == 'POST':
        if form.validate():
            login_user(form.user)
            return render_template("dashboard.html", form=form, error=error)
        else:
            error = "Invalid username or password."
            return render_template('login.html', form=form, error=error)
    else:
        return "An unknown error has occurred."


@app.route('/logout')
def logout():
    return 'logout'


@app.route('/dashboard/')
def product():
    return 'User dashboard'


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
