from flask import Flask
app = Flask(__name__)

from pychecker.database import db_session
import pychecker.views

@app.teardown_request
def shutdown_session(exception=None):
    print "Teardown 1 {0!r}".format(exception)
    db_session.remove()
