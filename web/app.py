from flask import Flask, redirect, render_template, request, url_for
# from flask.ext.login import login_required
import requests

AUTH_SERVICE = "http://auth:8081/"

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


# @login_required
@app.route('/user/create', methods=['POST'])
def create_user():
    print("hello")
    url = AUTH_SERVICE + 'user/create'
    email = request.form['email']
    password = request.form['password']
    data = {'email': email, 'password': password}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return "User Created"
    else:
        return "Something Bad Happend %d" % response.status_code


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        url = AUTH_SERVICE + 'authenticate'
        email = request.form['email']
        password = request.form['password']
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            user_data = response.json()
            if user_data['authenticated'] is True:
                return redirect(url_for('login'))
            else:
                error = "Invalid Email/Password..."
        else:
            error = "Something Bad Happened: HTTP STATUS: %d" \
                % response.status_code
    return render_template('login.html', title="Login", error=error)


@app.route('/user')
def get_user():
    url = AUTH_SERVICE + 'user'
    payload = {'email': request.args['email']}
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        user_data = response.json()
        return "User Got!\n Email: %s\nValid: %s" \
            % (user_data['email'], user_data['authenticated'])

    return "Something Bad Happened %d" % response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
