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
            salt = os.urandom(256)
            password = user_data['password']
            hashed_password = hash_password(password, salt)
            print("creating new user:\nemail: %s, pass: %s, salt: %s" % (user_data['email'], bytes_to_string(hashed_password), bytes_to_string(salt)))
            newUser = domain.User(user_data['email'], bytes_to_string(hashed_password), bytes_to_string(salt))
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

def create_user_from_user_data(user_data, salt):
    if ('email' not in user_data or 'password' not in user_data):
        return None

    if (user_data['email'] == None or user_data['password'] == None):
        return None

    password = string_to_bytes(user_data['password'])
    hashed_password = hash_password(password, salt)
    # print("creating new user:\nemail: %s, pass: %s, salt: %s" % (user_data['email'], bytes_to_string(hashed_password), bytes_to_string(salt)))
    newUser = domain.User(user_data['email'], hashed_password, salt)
    return newUser


@app.route('/user', methods=['GET'])
def get_user():
    email = request.args['email']
    if (email != None):
        user_data = get_user_from_email(email);
        if (user_data == None):
            return Response(status=404)
        else:
            user_data = {
                'email': user_data.email,
                'authenticated': user_data.authenticated
            }
            return json_response(user_data)
    else:
        return Response(status=400)

def get_user_from_email(email):
        user = domain.User.query.filter_by(email=email).first()
        if (user == None):
            return None
        else:
            return {
                'email': user.email,
                'authenticated': user.authenticated,
                'password': user.password,
                'salt': user.salt
            }

def json_response(data):
    return Response(json.dumps(data), status=200, mimetype='application/json')

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    user_data = request.get_json()
    email = user_data['email']
    password = user_data['password']
    user = domain.User.query.filter_by(email=email).first()
    if user == None:
        print("User not found %s" % email)
        return Response(
            json.dumps({'authenticated': False}),
            status=200,
            mimetype='application/json'
        )
    salt = string_to_bytes(user.salt)
    hashed_password = hash_password(password, salt)
    print("db\nemail: %s, pass: %s, salt: %s" % (user.email, user.password, user.salt))
    print("calc\nemail: %s, pass: %s" % (email, bytes_to_string(hashed_password)))
    if (hashed_password == string_to_bytes(user.password)):
        user.authenticated = True
    else:
        user.authenticated == False
    return Response(
        json.dumps({'authenticated': user.authenticated}),
        status=200,
        mimetype="application/json"
    )

def bytes_to_string(data):
    return data.decode('utf8')

def string_to_bytes(data):
    return data.encode('utf8')
    
### expects bytes ###
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        hashlib.sha256().name,
        password,
        salt,
        100000,
        None
    )