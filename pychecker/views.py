from pychecker import app
from pychecker.database import db_session
from pychecker import models
from pychecker import LoginManager
from pychecker import forms
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from flask.ext.login import current_user


def debug():
    'http://flask.pocoo.org/snippets/21/'
    assert app.debug is False


@app.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated():
        return redirect(url_for("dashboard"))
    else:
        return render_template('index.html', name="ya")


@app.route('/register/', methods=['POST', 'GET'])
def register():
    error = None
    db_users = db_session.query(models.User).all()
    if request.method == 'POST':
        already_exists = db_session.query(models.User).filter(
            models.User.username == request.form['username'])
        if (already_exists.count() > 0):
            error = "Sorry, the username " + request.form['username'] + \
                    " is already taken. \n"
        else:
            u = models.User(request.form['username'],
                            request.form['password'],
                            request.form['email'],
                            request.form['phone'],
                            request.form['twitter'])
            db_session.add(u)
            try:
                db_session.commit()
            except (IntegrityError, SQLAlchemyError, Exception) as e:
                error = "Sorry, the username " + request.form['username'] + \
                        " is already taken. \n" + str(e)
                db_session.rollback()
            db_users = db_session.query(models.User).all()
        return render_template('register.html',
                               error=error,
                               user=current_user,
                               users=db_users)
    elif request.method == 'GET':
        return render_template('register.html',
                               error=error,
                               user=current_user,
                               users=db_users)
    else:
        error = "An unknown error has occurred."
        return render_template('register.html',
                               error=error,
                               user=current_user,
                               users=db_users)


@app.route('/users/')
def users():
    error = None
    db_users = models.User.query.all()
    return render_template('users.html', users=db_users, error=error, user=current_user)


@app.route('/login/', methods=['GET', 'POST'])
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
            # raise
            return redirect(request.args.get("next") or url_for("dashboard"))
        else:
            return render_template('login.html', form=form, error=error, user=current_user)
    else:
        return "An unknown error has occurred."


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for("index"))


@app.route('/dashboard/')
def dashboard(message=None, form=None):
    products = current_user.products
    if form is None:
        form = forms.ProductForm()
    return render_template('dashboard.html',
                           user=current_user,
                           products=products,
                           form=form,
                           message=message)


@app.route('/product/', methods=['GET', 'POST'])
@login_required
def product():
    message = None
    form = forms.ProductForm()
    if request.method == 'GET':
        return redirect(request.args.get("next") or url_for("dashboard"))
    if request.method == 'POST':
        if form.validate():
            new_product = models.Product(name="ProductName",
                                         url=form.url.data,
                                         currentPrice="Test price",
                                         notifyPrice=form.notify_price.data,
                                         image="/static/img/screenshot.jpg")

            # new_product.users.append(current_user)
            # current_user.append(new_product)

            try:
                db_session.add(new_product)
                db_session.commit()
            except (IntegrityError) as e:
                message = "A product with this URL already exists: " + request.form['url']
                db_session.rollback()
            except (InvalidRequestError, Exception) as e:
                message = "Sorry, there was an error." + str(e)
                db_session.rollback()
            else:
                message = "Your product has been succesfully added."

            return dashboard(message=message, form=form)

        else:
            return render_template('dashboard.html', form=form)
    else:
        return 'An unknown error has occurred.'


@app.route('/product/<int:product_id>/')
def product_id(product_id):
    return 'product %s' % (product_id)


@app.route('/user/')
def user_route():
    return "current_user.is_authenticated: " + str(current_user.is_authenticated()) + "\n" + str(vars(current_user))
