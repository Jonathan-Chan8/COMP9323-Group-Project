from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import (BooleanField, PasswordField, StringField, SubmitField, 
                    IntegerField, TextField, TextAreaField, RadioField,
                    SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from wtforms.fields.html5 import DateField

from datetime import datetime
from datetime import date

from app.models import Users

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    guardian_first_name = StringField('First Name')
    guardian_last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])  
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    support_worker = SubmitField('I provide support')
    client = SubmitField('I receive support')
    client_guardian = SubmitField('Someone Else')
    client_self_managed = SubmitField('Myself')
    
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already in use.')

class ConnectForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])  
    send_request = SubmitField('Send Request')

class ConnectRequestForm(FlaskForm):
    
    sender_id = IntegerField('ID', validators=[Optional()])
    first_name = StringField('First Name')
    view_profile = SubmitField('View Profile')
    accept = SubmitField('Accept')
    decline = SubmitField('Decline')

class ConnectRequestForm2(FlaskForm):
    
    sender_id = IntegerField('ID', validators=[Optional()])
    first_name = StringField('First Name')
    view_profile = SubmitField('View Profile')
    accept = SubmitField('Accept')
    decline = SubmitField('Decline')

class ConnectRequestForm3(FlaskForm):
    
    sender_id = IntegerField('ID', validators=[Optional()])
    first_name = StringField('First Name')
    view_profile = SubmitField('View Profile')
    accept = SubmitField('Accept')
    decline = SubmitField('Decline')
    
class ConnectRequestForm4(FlaskForm):
    
    sender_id = IntegerField('ID', validators=[Optional()])
    first_name = StringField('First Name')
    view_profile = SubmitField('View Profile')
    accept = SubmitField('Accept')
    decline = SubmitField('Decline')


class ClientInformationForm(FlaskForm):
    
    # User Details
    guardian_first_name = StringField('First Name')
    guardian_last_name = StringField('Last Name')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Phone Number')
    age = IntegerField('Age', validators=[Optional()])
    gender = StringField('Gender')
    home_address = StringField('Home Address')
    short_bio = TextAreaField('Short Bio')
    
    # Client Details
    likes = StringField('Likes')
    dislikes = TextAreaField('Dislikes')
    allergies = TextAreaField('Allergies')
    health_needs = TextAreaField('Health Needs')
    
    # Payment Details Page
    ndis_number = IntegerField('NDIS Number', validators=[Optional()])
    ndis_plan = SelectField(u'NDIS Plan', choices = [('self managed', 'Self Managed'), ('plan managed', 'Plan Managed')],validators=[Optional()])
    plan_manager = StringField('Plan Manager')
    invoice_email = StringField('Invoice Email')
    
    # Submit buttons
    submit = SubmitField('Save')
    
    
class WorkerInformationForm(FlaskForm):
    
    # User Details
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Phone Number')
    date_of_birth = DateField('Date of Birth', validators=[Optional()]) 
    age = IntegerField('Age', validators=[Optional()])
    gender = StringField('Gender')
    home_address = StringField('Home Address')
    short_bio = TextAreaField('Short Bio')
    
    # Support Worker Details
    interests = TextAreaField('Interests')
    languages = StringField('Languages')
    
    # Work History 1
    location1 = StringField('Location')
    role1 = StringField('Role')
    work_start_date1 = DateField('Start Date', validators=[Optional()])
    work_end_date1 = DateField('End Date', validators=[Optional()])

    # Work History 2
    location2 = StringField('Location')
    role2 = StringField('Role')
    work_start_date2 = DateField('Start Date', validators=[Optional()])
    work_end_date2 = DateField('End Date', validators=[Optional()])


    # Work History 3
    location3 = StringField('Location')
    role3 = StringField('Role')
    work_start_date3 = DateField('Start Date', validators=[Optional()])
    work_end_date3 = DateField('End Date', validators=[Optional()])
    
    # Training 1
    course1 = StringField('Course')
    institution1 = StringField('Institution')
    training_start_date1 = DateField('Start Date', validators=[Optional()])
    training_end_date1 = DateField('End Date', validators=[Optional()])
 
    # Training 2
    course2 = StringField('Course')
    institution2 = StringField('Institution')
    training_start_date2 = DateField('Start Date', validators=[Optional()])
    training_end_date2 = DateField('End Date', validators=[Optional()])
    
    # Training 3
    course3 = StringField('Course')
    institution3 = StringField('Institution')
    training_start_date3 = DateField('Start Date', validators=[Optional()])
    training_end_date3 = DateField('End Date', validators=[Optional()])
    
    
    # Submit Buttons
    add_training2 = SubmitField('Add Training #2')
    add_training3 = SubmitField('Add Training #3')
    add_work_history2 = SubmitField('Add Work History #2')
    add_work_history3 = SubmitField('Add Work History #3')

    submit = SubmitField('Save Changes')
    
class AccountForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Save')
            

class WorkerReportForm(FlaskForm):
    
        clients = SelectField(u'Clients', coerce=int)


class AddShiftForm(FlaskForm):
    
    clients = SelectField(u'Support worker clients', choices = [( 'worker1', 'Darren'),('worker2','Steve')])







