from flask import Flask
from flask.ext.login import LoginManager
app = Flask(__name__)

from pychecker.database import db_session
from pychecker.models import User
from pychecker.config import secret_key
from pychecker import database
from pychecker import views

# run this line when the models have changed
# database.init()

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.secret_key = secret_key

login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)


@app.teardown_request
def shutdown_session(exception=None):
    print "Teardown 1 {0!r}".format(exception)
    db_session.remove()
