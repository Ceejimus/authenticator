from app import db

from flask import json


# Simple User Model
class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.LargeBinary)
    salt = db.Column(db.LargeBinary)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, salt):
        self.email = email
        self.password = password
        self.salt = salt
        self.authenticated = False

    def __repr__(self):
        return '<User %r>' % self.email

    def json(self):
        return json.dumps({
            'email': self.email,
            # 'password': self.password,
            # 'salt': self.salt,
            'authenticated': self.authenticated
        })
