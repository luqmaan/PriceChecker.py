from pychecker import app
from pychecker.database import db_session
from pychecker.models import User
from pychecker import LoginManager
from pychecker import forms
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from sqlalchemy.exc import IntegrityError
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from flask.ext.login import current_user


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
    if current_user.is_authenticated():
        return redirect(request.args.get("next") or url_for("dashboard"))
    error = None
    form = forms.LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form, error=error)
    elif request.method == 'POST':
        if form.validate():
            login_user(form.user)
            return redirect(request.args.get("next") or url_for("dashboard"))
        else:
            return render_template('login.html', form=form, error=error)
    else:
        return "An unknown error has occurred."


@app.route('/logout')
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for("index"))


@app.route('/dashboard/')
@login_required
def dashboard():
    error = None
    products = current_user.following
    form = forms.ProductForm()
    return render_template('dashboard.html',
			   user=current_user,
			   products=products,
			   form=form,
			   error=error)


@app.route('/product/', methods=['GET', 'POST'])
def product():
    form = forms.ProductForm()
    if request.method == 'GET':
	return render_template('dashboard.html', form=None)
    if request.method == 'POST':
	if form.validate():
	    message = "Your product has been succesfully added."
	    return render_template('dashboard.html', message=message)
	else:
	    return render_template('dashboard.html')
    else:
	return 'add new product or list all products'


@app.route('/product/<int:product_id>')
def product_id(product_id):
    return 'product %s' % (product_id)


@app.route('/user/')
def user():
    return 'add new user'


@app.route('/user/<username>')
def user_username(username):
    return 'user with name %s' % (username)
