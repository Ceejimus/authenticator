from app import db

# Simple User Model
class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    salt = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, salt):
        self.email = email
        self.password = password
        self.salt = salt
        self.authenticated = False

    def __repr__(self):
        return '<User %r>' % self.email