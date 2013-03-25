from flask import Flask
app = Flask(__name__)

import pychecker.views
import pychecker.database




# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()
