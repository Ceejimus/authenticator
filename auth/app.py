from flask import Flask, request, json, Response
from flask.ext.sqlalchemy import SQLAlchemy

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
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/user/create', methods=['POST'])
def create_user():
    if request.headers['content-type'] == 'application/json':
        user_data = request.get_json()
        return Response(
            json.dumps(user_data),
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            'Poo on you',
             status=415,
             mimetype="text/html"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)