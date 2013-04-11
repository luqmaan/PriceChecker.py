from pychecker import app
from pychecker.database import db_session
from pychecker import models
from pychecker import login_manager
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
from clint.textui import colored

from pychecker.scraper import update


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
        import pdb
        # pdb.set_trace()
        return render_template('login.html', form=form, error=error)
    elif request.method == 'POST':
        if form.validate():
            # import pdb
            # pdb.set_trace()
            login_user(form.user)
            return redirect(request.args.get("next") or url_for("dashboard"))
        else:
            return render_template('login.html', form=form, error=error, user=current_user)
    else:
        return "An unknown error has occurred."


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for("index"))


@login_required
@app.route('/dashboard/')
def dashboard(message=None, form=None):
    if not current_user.is_authenticated():
        return login_manager.unauthorized()
    if form is None:
        form = forms.ProductForm()
    products = current_user.products
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
            # get product data from le scraper
            try:
                price, img = update(form.url.data)
            except Exception as e:
                return dashboard(form=form, message=str(e))
            else:
                new_product = models.Product(name=form.name.data,
                                             url=form.url.data,
                                             currentPrice=price,
                                             image=img)

                new_product.users.append(current_user)

                try:
                    db_session.add(new_product)
                    db_session.commit()
                except (IntegrityError) as e:
                    # XXX maybe add the current_user to users and continue?
                    message = "A product with this URL already exists: " + request.form['url'] + "\n\n" + str(e)
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
    message = "current_user.is_authenticated: " + str(current_user.is_authenticated()) + "\n" + str(vars(current_user))
    return render_template("debug.html", message=message)


@app.route('/sites/')
def sites():
    message = ""
    if app.debug:
        regexes = db_session.query(models.RegEx).all()
        for r in regexes:
            message += str(r) + "\n"
    return render_template("debug.html", message=message)


@app.route('/init/')
def init():
    "initializes the database"

    u0 = models.User('john',
                     'doe',
                     'johndoe@yahoo.com',
                     '8131234567',
                     '@jdoe')
    u1 = models.User('jane',
                     'doe',
                     'johndoe@yahoo.com',
                     '8131234567',
                     '@jdoe')

    add_to_db(u0, "Adding user john")
    add_to_db(u1, "Adding user jane")

    # setup base regexes
    r = models.RegEx(
        "http://www.amazon.com/gp/product/B0083PWAPW/ref=kin_dev_gw_dual_t?ie=UTF8&nav_sdd=aps&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=center-1&pf_rd_r=0AB6YEC5AMG4J1801183&pf_rd_t=101&pf_rd_p=1493999442&pf_rd_i=507846",
        "TABLE.product > TBODY > TR > TD > B.priceLarge")
    add_to_db(r, title="Adding amazon regex")

    r = models.RegEx(
        "http://www.newegg.com/Product/Product.aspx?Item=N82E16827106352&cm_sp=DailyDeal-_-27-106-352-_-Homepage", "LI#singleFinalPrice > STRONG")
    add_to_db(r, title="Adding newegg regex")

    r = models.RegEx("http://www.gap.com/browse/product.do?cid=94150&vid=1&pid=289760382", "SPAN#priceText")
    add_to_db(r, title="Adding gap regex")

    r = models.RegEx("http://oldnavy.gap.com/browse/product.do?cid=93345&vid=1&pid=387523012", "SPAN#priceText")
    add_to_db(r, title="Adding oldnavy regex")

    r = models.RegEx("http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id=26872101&parentid=M_NEWARRIVALS",
                     "DIV#content > DIV#productDetail > DIV#prodOptions > H2.price > SPAN")
    add_to_db(r, title="Adding urbanoutfitters regex")

    r = models.RegEx(
        "http://www1.macys.com/shop/product/cuisinart-chw-12-coffee-maker-12-cup-programmable-with-hot-water-system?ID=466900&CategoryID=37460#fn=sp%3D1%26spc%3D189%26ruleId%3D18%26slotId%3Drec(3)",
        "DIV.standardProdPricingGroup > SPAN")
    add_to_db(r, title="Adding macys regex")

    r = models.RegEx("http://store.steampowered.com/app/216174/", "div.game_purchase_price")
    add_to_db(r, title="Adding steam regex")


    url1 = "http://www.amazon.com/Programming-Python-Mark-Lutz/dp/0596158106/ref=sr_1_2?ie=UTF8&qid=1365687660&sr=8-2&keywords=python"
    url2 = "http://www.amazon.com/Accoutrements-11884-Squirrel-Underpants/dp/B004I03BCM/ref=sr_1_1?ie=UTF8&qid=1365687697&sr=8-1&keywords=squirrel+underpants"
    price1, img1 = update(url1)
    price2, img2 = update(url2)

    new_product0 = models.Product(name="Python Programming",
                                  url=url1,
                                  currentPrice="93.32",
                                  image=img1)

    new_product1 = models.Product(name="Squirrel Underpants",
                                  url=url2,
                                  currentPrice="127.32",
                                  image=img2)

    new_product0.users.append(u0)
    # u0.products.append(new_product0)
    add_to_db(new_product0, "Adding product toothbrush to john")

    new_product1.users.append(u1)
    # u1.products.append(new_product1)
    add_to_db(new_product1, "Adding product chocolate to jane")

    u0.products.append(new_product1)
    # new_product1.users.append(u0)
    add_to_db(title="Adding chocolate to john")


    # then, load the Alembic configuration and generate the
    # version table, "stamping" it with the most recent rev:
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("pychecker/alembic.ini")
    command.stamp(alembic_cfg, "head")
    db_session.commit()
    return render_template("debug.html", message="Success!")


def add_to_db(o=None, title=""):
    if o is not None:
        db_session.add(o)
    try:
        db_session.commit()
    except (IntegrityError, SQLAlchemyError, InvalidRequestError, Exception) as e:
        error = "Sorry, there was an error \n\n" + str(e)
        db_session.rollback()
        print colored.red("@Error: " + title + " -> " + str(error))
    else:
        print colored.green("@Success: " + title)
