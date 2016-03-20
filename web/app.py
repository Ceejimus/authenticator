from flask import Flask
from psycopg2 import connect
from subprocess import check_output


app = Flask(__name__)

def getConn(dbname='db', dbhost = 'localhost', dbport=5432, dbuser='postgres', dbpass='postgres'):
	connStr = str.format("dbname='{0}' host='{1}' user='{2}' password='{3}'", dbname, dbhost, dbuser, dbpass)
	conn = connect(connStr)
	return conn

@app.route('/')
def hello():
	returnStr = ''

	try:
		conn = getConn(dbname='postgres', dbhost='db', dbuser='admin', dbpass='pass')
		returnStr += "connected"
	except Exception, e:
		return "Couldn't connect to database... %s" % str(e)

	try:
		cur = conn.cursor()
		returnStr +=' got cursor'
	except Exception, e:
		return "Couldn't get cursor... %s" % str(e)

	return "success"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)