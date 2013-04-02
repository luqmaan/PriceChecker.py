"https://github.com/mitsuhiko/flask/blob/master/docs/patterns/sqlalchemy.rst"
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///pychecker.db', echo=True)
# binds Session to db
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# main base class from which all other classes inherit
Base = declarative_base()
Base.query = db_session.query_property()


def init():
    "adds new tables to the db"
    from pychecker import models
    Base.metadata.create_all(engine)
