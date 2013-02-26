import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship, backref


engine = create_engine('sqlite:///pricechecker.db', echo=True)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key = True) #id/key
    name = Column(String) #name of product
    url = Column(String) #url of product
    currentPrice = Column(Numeric) #current price of product   

    def __init__(self,name, url, currentPrice):
        self.name = name
        self.url = url
        self.currentPrice = currentPrice

    def __repr__(self):
        return "<Product ('%s', '%s','%s')>" % (self.name, self.url, self.currentPrice)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True) # id/key
    username = Column(String) #username
    password = Column(String) #password
    #productsFollowed = Column(?) #I think a separate table should be used
    email = Column(String) #user's email
    phone = Column(String) #user's phone number
    twitter = Column(String) #user's twitter handle
    #accessTokens = Column() #dunnno what these are

    def __init__(self, username, password, email, phone, twitter):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.twitter = twitter

    def __repr__(self):
        return "<User ('%s', '%s','%s', '%s', '%s')>" % \
        (self.username, self.password, self.email, self.phone, self.twitter)


#need to fix foreign key stuff, can't add users because of TypeError: id() takes exactly one argument (0 given)
# class Following(Base):
#     __tablename__ = 'following'

#     user_id = Column(Integer, ForeignKey('users.id'), primary_key = True) #id of user following
#     product_id = Column(Integer, ForeignKey('products.id'), primary_key = True) #id of product being followed
#     notifyPrice = Column(Numeric) #price at which a notification should be sent

#     user = relationship("User", backref=backref('following', order_by=id))
#     product = relationship("Product", backref = backref('following', order_by =id))

#     def __init__(self, notifyPrice):
#         self.notifyPrice = notifyPrice

#     def __repr__(self):
#         return "<Following ('%s', '%s','%s')>" % \
#         (self.user_id, self.product_id, self.notifyPrice)


class RegEx(Base):
    __tablename__ = "regexes"
    id = Column(Integer, primary_key = True) # id/key
    siteurl = Column(String)    #url of site
    regex = Column(String)      #regex

    def __init_(self, siteurl, regex):
        self.siteurl = siteurl
        self.regex = regex 

    def __repr__(self):
        return "<Regex ('%s', '%s'>" % (self.siteurl, self.regex)


Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

test_user = User("testuser","password", "test@test.com", "555-555-555", "testuser")
session.add(test_user)

our_user = session.query(User).filter_by(username = 'testuser').first()

print our_user





