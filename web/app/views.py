from app import app, AUTH_SERVICE
import app.domain as domain
import app.forms as forms
from flask import json, request, render_template, redirect, url_for, flash
from flask.ext.login import login_required
import requests

# Views
@app.route('/')
def redirect_to_login():
    return redirect(url_for('login'))

@app.route('/account/create', methods=['GET', 'POST'])
#@login_required
def create_user():
    form = forms.CreateUserForm();
    if form.validate_on_submit():
        url = AUTH_SERVICE + 'user/create'
        email = request.form['email']
        password = request.form['password']
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return "User Created"
        else:
            return "Something Bad Happend %d" % response.status_code
    else:
        return render_template("create_user.html", title="Create Account", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        url = AUTH_SERVICE + 'authenticate'
        email = form.email.data;
        password = form.password.data;
        #remember_me = form.remember_me.data
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            user_data = response.json();
            if user_data['authenticated'] == True:
                print(url_for('login'))
                return redirect(url_for('login'))
            else:
                flash("Invalid Email/Password...")
        else:
            flash("Something Bad Happened: HTTP STATUS: %d" % response.status_code)
    else:
        return render_template("login.html", title="Login", form=form)

@app.route('/user')
def get_user():
    url = AUTH_SERVICE + 'user'
    payload = {'email' : request.args['email']}
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        user_data = response.json()
        return "User Got!\n Email: %s\nValid: %s" \
            % (user_data['email'], user_data['authenticated'])

    return "Something Bad Happened %d" % response.status_code