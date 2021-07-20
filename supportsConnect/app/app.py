"""
Flask Server

 - Takes HTTP requests (GET, POST, ...) and returns a response to the client

"""

# Imports

from flask import Flask, redirect, url_for, render_template, request, session, flash
from psycopg2 import connect, Error
from datetime import timedelta

# User-defined imports
from modules.database import *
from modules.profiles import *
from modules.scheduling import *
from modules.reporting import *

#----------------------------------------------------------------------------#

## Flask Server ##

app = Flask(__name__)
app.secret_key = "key"  # necessary for session data
app.permanent_session_lifetime = timedelta(days=2)

#----------------------------------------------------------------------------#

## Home Page ##

@app.route("/")
def home():
	return render_template("index.html")


## Create Account Page ##

@app.route("/create_account", methods=["POST", "GET"])
def create_account():
	# User sends account details
	if request.method == "POST":		
		
		email = request.form["email"]
		first_name = request.form["first_name"]					
		last_name = request.form["last_name"]
		user_type = request.form.get("user_type")

		user_instance = Support_Worker(first_name, last_name, email)

		print(user_instance)

		session["name"] = first_name
		session["email"] = email
		session["account_created"] = True

		# Case 1: User already exists
		if user_already_exists(email):							
			return redirect(url_for("user"))	

		# Case 2: Add user to database
		else:
			add_user_to_database(email, first_name, last_name)  
			return redirect(url_for("user"))

	return render_template("create_account.html")


## Login Page ##

@app.route("/login", methods=["POST", "GET"])
def login():

	# User enter's credentials
	if request.method == 'POST':
		email = request.form["email"]

		if user_already_exists(email):
			return redirect(url_for("user"))
		else:
			flash("This account does not exist", "error")
			return redirect(url_for("login"))

	return render_template("login.html")


## User Profile Page ##

@app.route("/user", methods=["POST", "GET"])
def user():
	session.permanent = True  # Keeps the user logged in

	if request.method == "POST" and "logout" in request.form:	# Case 1: User click's logout

		flash("You have been logged out!", "info")
		session.pop("name", None)
		session.pop("email", None)
		return redirect(url_for("login"))

	else:
		if "account_created" in session:
			name = session["name"]
			flash("You have successfully created an account {0}".format(name), "info")
			session.pop("account_created", None)

		return render_template("user.html")


#----------------------------------------------------------------------------#

## Run the app ##

# DEBUG MODE -> means you can edit here with the server running, 
# and you just need to 'refresh' your web browser to see changes

if __name__ == "__main__":
	app.run(debug = True)   
	

	


