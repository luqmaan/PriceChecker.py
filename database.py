import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship, backref


engine = create_engine('sqlite:///pricechecker.db', echo=True)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer) #id
    name = Column(String) #name of product
    url = Column(String, primary_key = True) #url of product/key
    currentPrice = Column(Numeric) #current price of product   
    user_id = Column(Integer, ForeignKey('users.username'), primary_key = True) #id of user following
    notifyPrice = Column(Numeric) #price at which a notification should be sent

    def __init__(self,name, url, currentPrice, notifyPrice):
        self.name = name
        self.url = url
        self.currentPrice = currentPrice
        self.notifyPrice = notifyPrice

    def __repr__(self):
        return "<Product ('%s', '%s','%s', '%s')>" % \
        (self.name, self.url, self.currentPrice, self.notifyPrice)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer) # id
    username = Column(String,  primary_key = True) #username/key
    password = Column(String) #password
    email = Column(String) #user's email
    phone = Column(String) #user's phone number
    twitter = Column(String) #user's twitter handle
    #accessTokens = Column() #dunnno what these are

    #list of products user is following
    following = relationship("Product", order_by ='Product.id', backref="user")

    def __init__(self, username, password, email, phone, twitter):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.twitter = twitter

    def __repr__(self):
        return "<User ('%s', '%s','%s', '%s', '%s')>" % \
        (self.username, self.password, self.email, self.phone, self.twitter)

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



session.add_all([
    User("testuser2","password2", "test2@test.com", "555-555-555", "testuser2"),
    User("testuser3","password3", "test3@test.com", "555-555-555", "testuser3"),
    User("testuser4","password4", "test4@test.com", "555-555-555", "testuser4")])

session.commit()

for instance in session.query(User).order_by(User.id):
    print instance.username, instance.password

test_user = User("testuser","password", "test@test.com", "555-555-555", "testuser")
test_product = Product("testproduct", "http://www.test.com", 1.50, 1.25)
test_product2 = Product("testproduct2", "http://www.test.com/2", 1.75, 1.50)

test_user.following.append(test_product)
test_user.following.append(test_product2)
session.commit()

print test_user.following

#print test_follow

#our_user = session.query(User).filter_by(username = 'testuser').first()

#print our_user
