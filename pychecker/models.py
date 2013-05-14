import re
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime, Enum, Text, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Table
from passlib.apps import custom_app_context as pwd_context
from database import Base
from helpers import URLError, domain_for

# http://docs.sqlalchemy.org/en/latest/orm/relationships.html#many-to-many
usersproducts_table = Table('userproducts', Base.metadata,
                            Column('username', Integer, ForeignKey('users.username')),
                            Column('url', Integer, ForeignKey('products.url')),
                            Column('userproduct_id', Integer, primary_key=True, nullable=False))
# XXX link userproducts to selector_id so each user can choose which block on page to monitor?


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)  # id, need to have even if null
    name = Column(String)  # name of product
    url = Column(String, unique=True)  # url of product/key
    currentPrice = Column(String)  # current price of product
    users = relationship("User", secondary=usersproducts_table)
    image = Column(String)  # path to the image
    history = relationship("ScrapeHistory", backref="ScrapeHistory", lazy="dynamic")
    selector = relationship("Selector", backref="Selector", lazy="dynamic")

    def __init__(self, name, url, currentPrice, image):
        self.name = name
        self.url = url
        self.currentPrice = currentPrice
        self.image = image
        domain = domain_for(url)
        self.selector = Selector.query.filter(Selector.domain == domain)

    def __repr__(self):
        return "<Product ('%s', '%s','%s', '%s')>" % \
            (self.name, self.url, self.currentPrice, self.image)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)  # id, need to have even if null...
    username = Column(String, unique=True)  # username/key
    password = Column(String)  # password
    email = Column(String)  # user's email
    phone = Column(String)  # user's phone number
    twitter = Column(String)  # user's twitter handle

    # list of products user is following, can also get user data by calling product.user
    products = relationship("Product", secondary=usersproducts_table)

    def __init__(self, username, password, email, phone, twitter):
        self.username = username
        self.password = pwd_context.encrypt(password)  # encrypts password
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
        return User.query.filter(User.username == self.username).count() > 0

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


class Selector(Base):
    __tablename__ = "selectors"
    id = Column(Integer, primary_key=True)  # id/key
    domain = Column(String)
    selector = Column(String)  # selector/xpath
    date_added = Column(DateTime, default=sqlalchemy.func.now())
    product_id = Column(Integer, ForeignKey('products.id'))
    history = relationship("ScrapeHistory", backref="SelectorHistory", lazy="dynamic")

    def __init__(self, url, selector):
        domain = domain_for(url)
        self.domain = domain
        self.selector = selector

    def __repr__(self):
        return "<Selector ('%s', '%s'>" % (self.domain, self.selector)


class ScrapeHistory(Base):
    __tablename__ = "ScrapeHistory"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    selector_id = Column(Integer, ForeignKey('selectors.id'))
    created = Column(DateTime, default=sqlalchemy.func.now())
    status = Column(String)
    data = Column(String)

    def __init__(self, id, selector_id, status, data):
        self.product_id = id
        self.selector_id = selector_id
        self.data = data
        self.status = status

    def __repr__(self):
        return "<ScrapeHistory ('%s', '%s', '%s', '%s'>" % (self.product_id, self.selector_id, self.created, self.status)
