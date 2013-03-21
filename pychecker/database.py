import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship, backref

#some basic info on how it works at line ~80

#set echo to False to get rid of detailed SQL info
engine = create_engine('sqlite:///pychecker.db', echo=True)

#main base class from which all other classes inherit
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer) #id, need to have even if null
    name = Column(String) #name of product
    url = Column(String, primary_key = True) #url of product/key
    currentPrice = Column(String) #current price of product   
    user_id = Column(Integer, ForeignKey('users.username'), primary_key = True) #id of user following
    notifyPrice = Column(String) #price at which a notification should be sent

    def __init__(self, user_id,name, url, currentPrice, notifyPrice):
        self.user_id = user_id
        self.name = name
        self.url = url
        self.currentPrice = currentPrice
        self.notifyPrice = notifyPrice

    def __repr__(self):
        return "<Product ('%s',%s', '%s','%s', '%s')>" % \
        (self.user_id,self.name, self.url, self.currentPrice, self.notifyPrice)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer) # id, need to have even if null...
    username = Column(String,  primary_key = True) #username/key
    password = Column(String) #password
    email = Column(String) #user's email
    phone = Column(String) #user's phone number
    twitter = Column(String) #user's twitter handle
    #accessTokens = Column() #dunnno what these are

    #list of products user is following, can also get user data by calling product.user
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
    siteurl = Column(String)    #url of site, maybe make associated with product urls?
    regex = Column(String)      #regex

    def __init_(self, siteurl, regex):
        self.siteurl = siteurl
        self.regex = regex 

    def __repr__(self):
        return "<Regex ('%s', '%s'>" % (self.siteurl, self.regex)

#adds new tables to the db
Base.metadata.create_all(engine)

#binds Session to db
Session = sessionmaker(bind = engine)
#creates an "instance" of session to let you interact with db
db_session = Session()

#to add things to db, first add to session, then commit

#User.following returns list of all products being followed
#product.user_id returns the username of the user following the product
#no explicit "following" table, is kept track of automatically

#when adding things to the db, make sure they are unique- query db before to make sure
#a row with the same key is not already there

#you can mess with the commented out code below to see how it works
#remember you can only add user/product to the db once, so second time it runs
#it will give error if you don't comment out/change the info

#check out http://docs.sqlalchemy.org/en/rel_0_8/orm/tutorial.html for more info



# session.add_all([
#     User("testuser2","password2", "test2@test.com", "555-555-555", "testuser2"),
#     User("testuser3","password3", "test3@test.com", "555-555-555", "testuser3"),
#     User("testuser4","password4", "test4@test.com", "555-555-555", "testuser4")])

# session.commit()

# for instance in session.query(User).order_by(User.id):
#     print instance.username, instance.password

#test_user = User("testuser10","password", "test@test.com", "555-555-555", "testuser")
#test_product = Product(test_user.username, "testproduct", "http://www.test.com", 1.50, 1.25)
#test_product2 = Product(test_user.username, "testproduct2", "http://www.test.com/2", 1.75, 1.50)

# session.add(test_user)
# session.add(test_product)
# session.add(test_product2)

#session.commit()

for instance in db_session.query(User).order_by(User.id):
    print instance.username, instance.following

#print test_user.following
#print test_product.user

#print test_follow

#our_user = session.query(User).filter_by(username = 'testuser').first()

#print our_user
