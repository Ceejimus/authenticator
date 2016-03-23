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

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

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
    print("AUTH: geting url params")
    email = request.args['email']
    print("AUTH: got param %s" % (email))
    if (email != None):
        user = User.query.filter_by(email=email).first()
        print user

    return Response('ok', status=200)

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=8081, debug=True)