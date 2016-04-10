from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('devconfig.py')
db = SQLAlchemy(app)

from app import api
from app import domain