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

# main base class froinm which all other classes inherit
Base = declarative_base()
Base.query = db_session.query_property()

def start_engine():
  Base.metadata.create_all(engine)
