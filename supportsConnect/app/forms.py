from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class Sign_up_Client_Form(FlaskForm):

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])  
    password = PasswordField('Password', validators=[DataRequired()])
    account_type = StringField('Account Type', validators=[DataRequired()])  
    submit = SubmitField('Create Account')


class Login_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')





