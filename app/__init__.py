import logging
from flask_cors import CORS
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate


"""
 Logging configuration
"""
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")

CORS(app)

# Initialize Flask-AppBuilder with SQLA
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

from . import views, api
