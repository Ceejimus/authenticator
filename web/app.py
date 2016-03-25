from flask import Flask, json, request, render_template, redirect, url_for
from flask.ext.login import login_required
import requests

app = Flask(__name__)

# Simple User Model
class User():

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __init__(self, email, password, authenticated):
        self.email = email
        self.password = password
        self.authenticated = authenticated

# Views
@app.route('/')
def redirect_to_login():
    return redirect(url_for('login'))

@app.route('/user/create')
#@login_required
def create_user():
    url = 'http://auth:8081/user/create'
    form_data = request.get_json()
    response = requests.post(url, json=form_data)
    if response.status_code == 200:
        return "User Created"
    else:
        return "Something Bad Happend %d" % response.status_code


@app.route('/login')
def login():
    return "login"

@app.route('/user')
def get_user():
    url = 'http://auth:8081/user'
    payload = {'email' : request.args['email']}
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        user_data = response.json()
        return "User Got!\n Email: %s\nValid: %s" \
            % (user_data['email'], user_data['authenticated'])

    return "Something Bad Happened %d" % response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)