from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# flask instance
app = Flask(__name__)
# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemy instance
db = SQLAlchemy(app)


from .router import *
