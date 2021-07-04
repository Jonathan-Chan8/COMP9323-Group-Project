"""
Flask Server

 - Takes HTTP requests (GET, POST, ...) and returns a response to the client

"""

# Imports

from flask import Flask, redirect, url_for, render_template, request, session, flash
from psycopg2 import connect, Error
from datetime import timedelta

# User-defined imports
from utils.connect_to_db import connect_to_supportsconnect_database


#----------------------------------------------------------------------------#
## Database Queries ##

def user_already_exists(email):
	conn, cur = connect_to_supportsconnect_database() 
	query = "SELECT EXISTS(SELECT 1 FROM Users WHERE email = '{0}');".format(email)

	if cur != None:
		try:
			cur.execute(query)
			result = cur.fetchone()[0]
		except (Exception, Error) as error:
			print("\nexecute_sql() error:", error)
			conn.rollback()
	else:
		result = False
	cur.close()
	conn.close()

	return result
		
def add_user_to_database(email,first_name, last_name):
	conn, cur = connect_to_supportsconnect_database() 
	query = "INSERT INTO Users(email, givenName, familyName) VALUES ('{0}', '{1}', '{2}');".format(email, first_name, last_name)

	result = False
	if cur != None:
		try:
			cur.execute(query)
			print("SUCCESSFULLY ADDED")

		except (Exception, Error) as error:
			print("\nexecute_sql() error:", error)
			conn.rollback()
	else:
		result = False

	conn.commit()
	cur.close()
	conn.close()

	return result

#----------------------------------------------------------------------------#

## Flask Server ##

app = Flask(__name__)
app.secret_key = "key"  # necessary for session data
app.permanent_session_lifetime = timedelta(days=2)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/create_account", methods=["POST", "GET"])
def create_account():
	# User sends account details
	if request.method == "POST":		
		
		email = request.form["email"]
		first_name = request.form["first_name"]					
		last_name = request.form["last_name"]

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


@app.route("/login", methods=["POST", "GET"])
def login():

	# User enter's credentials
	if request.method == 'POST':
		email = request.form["email"]

		if user_already_exists(email):
			return redirect(url_for("user"))
		else:
			flash("This account does not exist")
			return redirect(url_for("user"))

	return render_template("login.html")


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
	

	


