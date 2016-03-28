from flask import Flask

AUTH_SERVICE = "http://auth:8081/"

app = Flask(__name__)
app.config.from_object('config')

from app import views
from app import domain
from app import forms