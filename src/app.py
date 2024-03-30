from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from admin import admin
from models import db
from routes import get_response
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@"
    f"{environ.get('DB_HOST')}:{environ.get('DB_PORT')}/{environ.get('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = environ.get("DB_USER")

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

admin.init_app(app)

app.route("/api/chatrequest/get_response", methods=["GET", "POST", "OPTIONS"])(
    get_response
)

if __name__ == "__main__":
    app.run(debug=True)
