"https://github.com/mitsuhiko/flask/blob/master/docs/patterns/sqlalchemy.rst"
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError
from clint.textui import colored

engine = create_engine('sqlite:///pychecker.db', echo=True)
# binds Session to db
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# main base class from which all other classes inherit
Base = declarative_base()
Base.query = db_session.query_property()

def init():
    "initializes the database"
    from pychecker import models
    Base.metadata.create_all(engine)

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

    new_product0 = models.Product(name="Toothbrush",
                                  url="http://google.com",
                                  currentPrice="50",
                                  image="/static/img/screenshot.jpg")

    new_product1 = models.Product(name="Chocolate",
                                  url="http://amazon.com",
                                  currentPrice="77",
                                  image="/static/img/screenshot.jpg")

    new_product0.users.append(u0)
    # u0.products.append(new_product0)
    add_to_db(new_product0, "Adding product toothbrush to john")

    new_product1.users.append(u1)
    # u1.products.append(new_product1)
    add_to_db(new_product1, "Adding product chocolate to jane")

    u0.products.append(new_product1)
    # new_product1.users.append(u0)
    add_to_db(title="Adding chocolate to john")

    # setup base regexes
    r = models.RegEx("http://www.amazon.com/gp/product/B0083PWAPW/ref=kin_dev_gw_dual_t?ie=UTF8&nav_sdd=aps&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=center-1&pf_rd_r=0AB6YEC5AMG4J1801183&pf_rd_t=101&pf_rd_p=1493999442&pf_rd_i=507846", "TABLE.product > TBODY > TR > TD > B.priceLarge")
    add_to_db(r, title="Adding amazon regex")

    r = models.RegEx("http://www.newegg.com/Product/Product.aspx?Item=N82E16827106352&cm_sp=DailyDeal-_-27-106-352-_-Homepage", "LI#singleFinalPrice > STRONG")
    add_to_db(r, title="Adding newegg regex")

    r = models.RegEx("http://www.gap.com/browse/product.do?cid=94150&vid=1&pid=289760382", "SPAN#priceText")
    add_to_db(r, title="Adding gap regex")

    r = models.RegEx("http://oldnavy.gap.com/browse/product.do?cid=93345&vid=1&pid=387523012", "SPAN#priceText")
    add_to_db(r, title="Adding oldnavy regex")

    r = models.RegEx("http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id=26872101&parentid=M_NEWARRIVALS", "DIV#content > DIV#productDetail > DIV#prodOptions > H2.price > SPAN")
    add_to_db(r, title="Adding urbanoutfitters regex")

    r = models.RegEx("http://www1.macys.com/shop/product/cuisinart-chw-12-coffee-maker-12-cup-programmable-with-hot-water-system?ID=466900&CategoryID=37460#fn=sp%3D1%26spc%3D189%26ruleId%3D18%26slotId%3Drec(3)", "DIV.standardProdPricingGroup > SPAN")
    add_to_db(r, title="Adding macys regex")

    r = models.RegEx("http://store.steampowered.com/app/216174/", "div.game_purchase_price")
    add_to_db(r, title="Adding steam regex")

    # then, load the Alembic configuration and generate the
    # version table, "stamping" it with the most recent rev:
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("pychecker/alembic.ini")
    command.stamp(alembic_cfg, "head")
    db_session.commit()

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


