import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime, Enum, Text, Numeric
from sqlalchemy.orm import relationship, backref

#Defaults to SHA256-Crypt under 32 bit systems, SHA512-Crypt under 64 bit systems.
from passlib.apps import custom_app_context as pwd_context

from pychecker import db_session
from pychecker.database import engine
from pychecker.database import Base


class Product(Base):
	__tablename__ = "products"

	# I kind of think the product.id should be primary so it autoincrements
	# or use sqlite rowid?
	id = Column(Integer)  # id, need to have even if null
	name = Column(String)  # name of product
	url = Column(String, primary_key=True)  # url of product/key
	currentPrice = Column(String)  # current price of product
	user_id = Column(Integer, ForeignKey('users.username'), primary_key=True)  # id of user following
	regex_id = Column(Integer, ForeignKey('regexes.id')) 
	notifyPrice = Column(String)  # price at which a notification should be sent
	history = relationship("ScrapeHistory", backref="ScrapeHistory", lazy="dynamic")

	def __init__(self, user_id, name, url, currentPrice, notifyPrice):
		self.user_id = user_id
		self.name = name
		self.url = url
		self.currentPrice = currentPrice
		self.notifyPrice = notifyPrice

	def __repr__(self):
        	return "<Product ('%s', '%s', '%s', '%s', '%s')>" % \
		(self.user_id, self.name, self.url, self.currentPrice, self.notifyPrice)

# UserSession
# UserAuth type=password, nonce tokens

class User(Base):
    __tablename__ = "users"

    id = Column(Integer)  # id, need to have even if null...
    username = Column(String, primary_key=True)  # username/key
    password = Column(String)  # password
    email = Column(String)  # user's email
    phone = Column(String)  # user's phone number
    twitter = Column(String)  # user's twitter handle
    # accessTokens = Column() #dunnno what these are

    # list of products user is following, can also get user data by calling product.user
    following = relationship("Product", order_by='Product.id', backref="user")


    def __init__(self, username, password, email, phone, twitter):
        self.username = username
        self.password = pwd_context.encrypt(password); # encrypts password
        self.email = email
        self.phone = phone
        self.twitter = twitter

    def __repr__(self):
        return "<User ('%s', '%s','%s', '%s', '%s')>" % \
            (self.username, self.password, self.email, self.phone, self.twitter)

    def check_password(self, password):
        return pwd_context.verify(password,self.password)

    def is_active(self):
        'http://pythonhosted.org/Flask-Login/'
        return True

    def is_authenticated(self):
        'http://flask.pocoo.org/mailinglist/archive/2011/11/27/flask-login-question/'
        return db_session.query(User).get(self.username) is not None

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

class ScrapeHistory(Base):
       __tablename__ = "ScrapeHistory"
       id = Column(Integer, primary_key=True)
       product_id = Column(Integer, ForeignKey('products.id'))
       regex_id = Column(Integer, ForeignKey('regexes.id'))
       created = Column(DateTime, default=sqlalchemy.func.now())
       status = Column(Enum, Enum('Success', 'Failed'))
       data = Column(String)

       def __init__(self, id, regex_id, status, data):
               self.product_id = id
               self.regex_id = regex_id
               self.data = data
               self.status = status

class RegEx(Base):
	__tablename__ = "regexes"
	id = Column(Integer, primary_key=True)  # id/key
	siteurl = Column(String)  # url of site, maybe make associated with product urls?
	regex = Column(String)  # regex/xpath
	type = Column(String, Enum('regex', 'xpath'))
	meta = Column(String)
	title = Column(String)
	text = Column(String)
	name = Column(String)
	date_added = Column(DateTime, default=sqlalchemy.func.now())
	history = relationship("ScrapeHistory", backref="RegexHistory", lazy="dynamic")
	products = relationship("Product", backref="Product", lazy="dynamic")

	def __init__(self, siteurl, regex, rorx, meta, title, text, name):
		self.siteurl = siteurl
		self.regex = regex
		self.type = rorx
		self.meta = meta
		self.title = title
		self.name = name
		self.text = text

	def __repr__(self):
		return "<Regex ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'>" % (self.siteurl, self.regex, self.type, self.meta, self.title, self.name, self.date_added, self.text)


