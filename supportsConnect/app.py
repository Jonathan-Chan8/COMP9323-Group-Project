"""
Flask Server

 - Takes HTTP requests (GET, POST, ...) and returns a response to the client
"""

# Imports

from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy 
#from models import db
from psycopg2 import connect, Error

ENV = 'heroku'
#----------------------------------------------------------------------------#

## Business Logic ##

app = Flask(__name__)
app.secret_key = "key"  # necessary for session data

POSTGRES = {
    #'user': 'admin',
    'user': 'postgres',
  #  'pw': ";'",
    'pw': "support",
    'db': 'supportsConnect',
    'host': 'localhost',
    'port': '5432',
}

if ENV == 'local':
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES # USE THIS FOR LOCAL HOST
if ENV == 'heroku':
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tzyorblmmujtqn:78696e1fe5d8cbacb4fc2cbdde7b835d8960d8e347350cde074e90aab8f7a444@ec2-107-21-10-179.compute-1.amazonaws.com:5432/d37h70o640paa9'



db = SQLAlchemy(app)

#db.init_app(app)
#db = SQLAlchemy(app)

class users(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))

	def __init__(self, name, email):
		self.name = name
		self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
	return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":				# Case 1: User sends login details
		user = request.form["nm"]				# redirect to their profile
		session["user"] = user

		found_user = users.query.filter_by(name=user).first()
		if found_user:
			session["email"] = found_user.email
		else:
			usr = users(user, "")	# Add user to the database
			db.session.add(usr)
			db.session.commit()


		flash("Login Successful!")
		return redirect(url_for("user"))
	else:
		if "user" in session: 					# Case 2: User already logged in
			flash("Already logged in!")
			return redirect(url_for("user"))    # redirect to their profile
		
		return render_template("login.html")	# Case 3: User opens page for the first time


@app.route("/user", methods=["POST", "GET"])
def user():
	email = None

	if request.method == "POST" and "logout" in request.form:	# Case 1: User click's logout
		user = session["user"]
		flash(f"You have been logged out {user}!", "info")
		session.pop("user", None) 
		session.pop("email", None)
		return redirect(url_for("login"))

	elif "user" in session:
		user = session["user"]
		if request.method == "POST" and "email" in request.form:
			email = request.form["email"]
			session["email"] = email
			found_user = users.query.filter_by(name=user).first()
			found_user.email = email
			db.session.commit()
			flash("email was saved")
		else:
			if "email" in session:
				email = session["email"]

		user = session["user"]
		return render_template("user.html", email=email)
	else:
		return redirect(url_for("login"))


@app.route("/logout")
def logout():
	session.pop("user", None) 
	return redirect(url_for("login"))

#----------------------------------------------------------------------------#

# DEBUG MODE -> means you can edit here with the server running, 
# and you just need to 'refresh' your web browser to see changes

if __name__ == "__main__":
	db.create_all()
	app.run(debug = True)   
    
    
    


