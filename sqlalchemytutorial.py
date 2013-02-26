import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///:memory:', echo=True)

engine.execute("select 1").scalar()

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	password = Column(String)

	def __init__(self, name, fullname, password):
		self.name = name
	 	self.fullname = fullname
	 	self.password = password

	def __repr__(self):
		return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

    

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

ed_user = User('ed', 'Ed Jones', 'edspassword')
session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first() 

print our_user

print ed_user is our_user

session.add_all([
     User('wendy', 'Wendy Williams', 'foobar'),
     User('mary', 'Mary Contrary', 'xxg527'),
     User('fred', 'Fred Flinstone', 'blah')])

ed_user.password = 'f8s7ccs'

session.commit()

for name, fullname in session.query(User.name, User.fullname):
    print name, fullname

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref=backref('addresses', order_by=id))

    def __init__(self, email_address):
        self.email_address = email_address

    def __repr__(self):
        return "<Address('%s')>" % self.email_address

Base.metadata.create_all(engine) 

jack = User('jack', 'Jack Bean', 'gjffdd')

jack.addresses = [
Address(email_address='jack@google.com'),
Address(email_address='j25@yahoo.com')]
print jack.addresses[1]

session.add(jack)
session.commit()

for name, fullname in session.query(User.name, User.fullname):
    print name, fullname


