from flask import Flask
app = Flask(__name__)

import pychecker.views

from pychecker.database import db_session

# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()
