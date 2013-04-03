from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Table

# Defaults to SHA256-Crypt under 32 bit systems, SHA512-Crypt under 64 bit systems.
from passlib.apps import custom_app_context as pwd_context

from pychecker import db_session
from pychecker.database import Base

# http://docs.sqlalchemy.org/en/latest/orm/relationships.html#many-to-many
usersproducts_table = Table('userproducts', Base.metadata,
                            Column('username', Integer, ForeignKey('users.username')),
                            Column('url', Integer, ForeignKey('products.url')),
                            Column('userproduct_id', Integer, primary_key=True, nullable=False))


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)  # id, need to have even if null
    name = Column(String)  # name of product
    url = Column(String, unique=True)  # url of product/key
    currentPrice = Column(String)  # current price of product
    users = relationship("User", secondary=usersproducts_table)
    notifyPrice = Column(String)  # price at which a notification should be sent
    image = Column(String)  # path to the image

    def __init__(self, name, url, currentPrice, notifyPrice, image):
        self.name = name
        self.url = url
        self.currentPrice = currentPrice
        self.notifyPrice = notifyPrice
        self.image = image

    def __repr__(self):
        return "<Product ('%s', '%s','%s', '%s', '%s')>" % \
            (self.name, self.url, self.currentPrice, self.notifyPrice, self.image)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)  # id, need to have even if null...
    username = Column(String, unique=True)  # username/key
    password = Column(String)  # password
    email = Column(String)  # user's email
    phone = Column(String)  # user's phone number
    twitter = Column(String)  # user's twitter handle
    # accessTokens = Column() #dunnno what these are

    # list of products user is following, can also get user data by calling product.user
    products = relationship("Product", secondary=usersproducts_table)

    def __init__(self, username, password, email, phone, twitter):
        self.username = username
        self.password = pwd_context.encrypt(password)
        # encrypts password
        self.email = email
        self.phone = phone
        self.twitter = twitter

    def __repr__(self):
        return "<User ('%s', '%s','%s', '%s', '%s')>" % \
            (self.username, self.password, self.email, self.phone, self.twitter)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

    def is_active(self):
        'http://pythonhosted.org/Flask-Login/'
        return True

    def is_authenticated(self):
        'http://flask.pocoo.org/mailinglist/archive/2011/11/27/flask-login-question/'
        return db_session.query(User).filter(User.username == self.username).count() > 0

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


class RegEx(Base):
    __tablename__ = "regexes"
    id = Column(Integer, primary_key=True, nullable=False)  # id/key
    siteurl = Column(String)  # url of site, maybe make associated with product urls?
    regex = Column(String)  # regex

    def __init_(self, siteurl, regex):
        self.siteurl = siteurl
        self.regex = regex

    def __repr__(self):
        return "<Regex ('%s', '%s'>" % (self.siteurl, self.regex)
