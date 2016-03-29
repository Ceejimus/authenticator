from app import app, db
import app.domain as domain
from flask import request, json, Response
import hashlib
import os
import binascii

@app.route('/user/create', methods=['POST'])
def create_user():
    if request.headers['content-type'] == 'application/json':
        user_data = request.get_json()
        if (user_data['email'] != None and user_data['password'] != None):
            salt = binascii.hexlify(os.urandom(256))
            hashed_password = hash_password(user_data['password'], salt)
            newUser = domain.User(user_data['email'], hashed_password, salt)
            db.session.add(newUser)
            db.session.commit()
        return Response(
            newUser.json(),
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
    user = domain.User.query.filter_by(email=email).first()
    if user == None:
        return Response(
            json.dumps({'authenticated': False}),
            status=200,
            mimetype='application/json'
        )
    salt = user.salt
    hashed_password = hash_password(password, salt)
    if (hashed_password == user.password):
        user.authenticated = true
    else:
        user.authenticated == False
    return Response(
        json.dumps({'authenticated': user.authenticated}),
        status=200,
        mimetype="application/json"
    )
    
def hash_password(password, salt):
    digest = hashlib.sha256
    if (type(password) is str):
        password = bytearray(password, 'utf8')
    if (type(salt) is str):
        salt = bytearray(salt, 'utf8')
    return hashlib.pbkdf2_hmac(
        digest().name,
        password,
        salt,
        100000,
        None
    )