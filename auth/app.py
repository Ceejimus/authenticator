from flask import Flask, request, json, Response
from flask.ext.sqlalchemy import SQLAlchemy
import hashlib
import os
import binascii

CONNECTION_STRING = \
    "postgresql+psycopg2://admin:pass@db:5432/postgres"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING

db = SQLAlchemy(app)

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

def hash_password(password, salt):
    digest = hashlib.sha256
    return hashlib.pbkdf2_hmac(
        digest().name,
        password,
        salt,
        100000,
        None
    )

def salt(n):
    salt = binascii.hexlify(os.urandom(n))

@app.route('/user/create', methods=['POST'])
def create_user():
    if request.headers['content-type'] == 'application/json':
        user_data = request.get_json()
        if (user_data['email'] != None and user_data['password'] != None):
            newUser = User(user_data['email'], user_data['password'])
            db.session.add(newUser)
            db.session.commit()

        return Response(
            json.dumps(newUser),
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            'Poo on you',
             status=415,
             mimetype="text/html"
        )

@app.route('/user', methods=['GET'])
def get_user():
    email = request.args['email']
    if (email != None):
        user = User.query.filter_by(email=email).first()
        if (user == None):
            return Response(status=404)
        else:
            user_data = {
                'email': user.email,
                'authenticated': user.authenticated
            }
            return Response(
                json.dumps(user_data),
                status=200,
                mimetype="application/json"
            )
    else:
        return Response(status=400)

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    user_data = request.get_json()
    email = user_data['email']
    password = user_data['password']
    user = User.query.filter_by(email=email).first()
    hashed_password = hash_password(password, salt)
    if (hashed_password == user.password):
        user.authenticated = true
    else:
        user.authenticated == False
    return Response(
        json.dumps({'authenticated': user.authenticated}),
        status = 200,
        mimetype="application/json"
    )

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=8081, debug=True)