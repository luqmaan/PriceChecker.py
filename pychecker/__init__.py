from flask import Flask
from flask.ext.login import LoginManager
app = Flask(__name__)

from pychecker.database import db_session
from pychecker.models import User
from pychecker.config import secret_key

import pychecker.views

app.secret_key = secret_key


@app.teardown_request
def shutdown_session(exception=None):
    print "Teardown 1 {0!r}".format(exception)
    db_session.remove()

login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)
