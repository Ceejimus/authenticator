from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
	UserMixin, RoleMixin, login_required

DATABASE_HOST = 'db'
DATABASE_PORT = 5432
DATABASE_NAME = 'postgres'
DATABASE_USER = 'admin'
DATABASE_PASS = 'pass'

CONNECTION_STR_FORMAT = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}"

def connectionStr():
	return str.format(
		CONNECTION_STR_FORMAT,
		DATABASE_USER,
		DATABASE_PASS,
		DATABASE_HOST,
		DATABASE_PORT,
		DATABASE_NAME
	);

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = connectionStr()

db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='cj@atmoscape.com', password='password')
    db.session.commit()

# Views
@app.route('/')
@login_required
def home():
    return "hello"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)