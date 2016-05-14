import hashlib
import os

from app import app, db
import app.domain as domain

from flask import Response, json, request


@app.route('/user/create', methods=['POST'])
def create_user():
    if request.headers['content-type'] != 'application/json':
        return bad_content_type('application/json')

    user_data = request.get_json()

    if ('email' not in user_data or 'password' not in user_data):
        return bad_request('[ERROR] Expected email and password')

    if user_data['email'] is None or user_data['password'] is None:
        return bad_request('[ERROR] Expected email and password')

    new_user = create_user_from_user_data(user_data, os.urandom(256))
    db.session.add(new_user)
    db.session.commit()

    return json_response(new_user.json(), False)


@app.route('/user', methods=['GET'])
def get_user():
    email = request.args['email']

    if email is None:
        return bad_request("[ERROR] expected email")

    user_data = get_user_data_from_email(email)

    if user_data is None:
        return Response(status=404)

    user_data = {
        'email': user_data['email'],
        'authenticated': user_data['authenticated']
    }

    return json_response(user_data)


@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    if request.headers['content-type'] != 'application/json':
        return bad_content_type('application/json')

    request_data = request.get_json()

    if ('email' not in request_data or 'password' not in request_data):
        return bad_request('[ERROR] Expected email and password')

    if request_data['email'] is None or request_data['password'] is None:
        return bad_request('[ERROR] Expected email and password')

    email = request_data['email']
    supplied_password = string_to_bytes(request_data['password'])

    user_data = get_user_data_from_email(email)

    if user_data is None:
        return json_response({'authenticated': False})

    authenticated = authenticate_user_against_supplied_password(supplied_password, user_data)

    return json_response({'authenticated': authenticated})


def authenticate_user_against_supplied_password(supplied_password, user_data):
    salt = user_data.salt
    hashed_password = hash_password(supplied_password, salt)

    if (hashed_password == string_to_bytes(user_data.password)):
        return True

    return False


def create_user_from_user_data(user_data, salt):
    password = string_to_bytes(user_data['password'])
    hashed_password = hash_password(password, salt)
    new_user = domain.User(user_data['email'], hashed_password, salt)
    return new_user


def get_user_data_from_email(email):
    user = domain.User.query.filter_by(email=email).first()
    if user is None:
        return None
    else:
        return {
            'email': user.email,
            'authenticated': user.authenticated,
            'password': user.password,
            'salt': user.salt
        }


def json_response(data, dump=True):
    content = json.dumps(data) if dump else data
    return Response(content, status=200, mimetype='application/json')


def bad_request(message):
    return Response(message, status=400, mimetype='text/html')


def bad_content_type(expected_mimetype):
    content = "[ERROR] expected mimetype: {}".format(expected_mimetype)
    return Response(content, status=415, mimetype='text/html')


def bytes_to_string(data):
    return data.decode('utf8')


def string_to_bytes(data):
    return data.encode('utf8')


# expects bytes
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        hashlib.sha256().name,
        password,
        salt,
        100000,
        None
    )
