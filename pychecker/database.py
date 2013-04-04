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
