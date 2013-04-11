from flask import Flask
from flask.ext.login import LoginManager
app = Flask(__name__)
login_manager = LoginManager()
login_manager.setup_app(app)

from pychecker.database import db_session
from pychecker.config import secret_key
from pychecker import models
from pychecker import database
from pychecker import views

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.secret_key = secret_key

database.init()


@login_manager.user_loader
def load_user(username):
    return db_session.query(models.User).filter(models.User.username == username).first()


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
