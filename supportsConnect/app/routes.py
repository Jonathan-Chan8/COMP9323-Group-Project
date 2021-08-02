from flask import render_template, flash, redirect
from flask.helpers import url_for
from app import app, db
from app.forms import Login_Form, Sign_up_Client_Form
from app.models import *
from app.database import *
from app.database_queries import *
from app.test_data import add_test_data_to_database

add_test_data_to_database()


@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/sign_up_client', methods=['GET', 'POST'])
def sign_up_client():
	form = Sign_up_Client_Form()
	if form.validate_on_submit():
		flash(f'Create account requested for {form.email.data}')

		if user_already_exists(form.email.data):
			flash(f'User email already exists')

		else:
			add_user_to_database(form.first_name.data, form.last_name.data, form.email.data, form.password.data,form.account_type.data)
			flash(f'User added to database')
			return redirect(url_for('index'))

	return render_template('sign_up_client.html', title='Sign Up Client Form', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = Login_Form()
	if form.validate_on_submit():

		flash(f'Login requested for user {form.email.data}, remember_me={form.remember_me.data}')
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)








































