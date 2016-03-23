from flask import Flask, json, request
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
#@login_required
def home():
    url = 'http://auth:8081/user/create'
    data = {
        'email': 'cj@atmoscape.com',
        'password': 'woot'
    }
    response = requests.post(url, json=data)
    return response.json()['email'] + response.json()['password']

@app.route('/user')
def get():
    url = 'http://auth:8081/user'
    print("WEB: geting url params")
    payload = {'email' : request.args['email']}
    print("WEB: got param %s" % (payload['email']))
    response = requests.get(url, params=payload)
    print(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)