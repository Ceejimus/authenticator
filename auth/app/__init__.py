from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

CONNECTION_STRING = \
    "postgresql+psycopg2://admin:pass@db:5432/postgres"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING

db = SQLAlchemy(app)

from app import api
from app import domain