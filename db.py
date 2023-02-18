from main import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///alexalgr"
db = SQLAlchemy(app)