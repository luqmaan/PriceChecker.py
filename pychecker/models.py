from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, Numeric
from sqlalchemy.orm import relationship, backref

from pychecker.database import engine
from pychecker.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer)  # id, need to have even if null
    name = Column(String)  # name of product
    url = Column(String, primary_key=True)  # url of product/key
    currentPrice = Column(String)  # current price of product
    user_id = Column(Integer, ForeignKey('users.username'), primary_key=True)  # id of user following
    notifyPrice = Column(String)  # price at which a notification should be sent

    def __init__(self, user_id, name, url, currentPrice, notifyPrice):
        self.user_id = user_id
        self.name = name
        self.url = url
        self.currentPrice = currentPrice
        self.notifyPrice = notifyPrice

    def __repr__(self):
        return "<Product ('%s',%s', '%s','%s', '%s')>" % \
            (self.user_id, self.name, self.url, self.currentPrice, self.notifyPrice)


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
        self.password = password
        self.email = email
        self.phone = phone
        self.twitter = twitter

    def __repr__(self):
        return "<User ('%s', '%s','%s', '%s', '%s')>" % \
            (self.username, self.password, self.email, self.phone, self.twitter)

    def check_password(self, password):
        return self.password == password

    def is_active(self):
        return True

    def get_id(self):
        return self.username


class RegEx(Base):
    __tablename__ = "regexes"
    id = Column(Integer, primary_key=True)  # id/key
    siteurl = Column(String)  # url of site, maybe make associated with product urls?
    regex = Column(String)  # regex

    def __init_(self, siteurl, regex):
        self.siteurl = siteurl
        self.regex = regex

    def __repr__(self):
        return "<Regex ('%s', '%s'>" % (self.siteurl, self.regex)

