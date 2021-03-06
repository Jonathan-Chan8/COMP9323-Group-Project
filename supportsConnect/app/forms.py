from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import (BooleanField, PasswordField, StringField, SubmitField, 
                    IntegerField, TextField, TextAreaField, RadioField,
                    SelectField, DateTimeField, SelectMultipleField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional, InputRequired
from wtforms.fields.html5 import DateField, TimeField, DateTimeField



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
    

    clients = SelectField(u'Client: ', coerce=int, validators=[Optional()])
    client_submit = SubmitField('Apply')
    
    activities = SelectField(u'Activity: ', coerce=int, validators=[Optional()], validate_choice=False)
    activity_submit = SubmitField('Apply', validators=[Optional()])

    locations = SelectField(u'Location: ', coerce=int, validators=[Optional()], validate_choice=False)
    location_submit = SubmitField('Apply', validators=[Optional()])
    
class ClientReportForm(FlaskForm):
    
    workers = SelectField(u'Support Worker: ', coerce=int, validators=[Optional()])
    worker_submit = SubmitField('Apply')
    
    incident = SelectField(u'Incident?',choices=[('Yes','Yes'),('No','No')])
    incident_submit = SubmitField('Apply')
    
    moods = SelectField(u'Mood: ', choices=[('happy','happy'),('moderate','moderate'), ('sad', 'sad'), ('angry', 'angry'), ('hyperactive', 'hyperactive')])
    mood_submit = SubmitField('Apply')


class ReportingForm(FlaskForm):
    
    activities = SelectMultipleField(u'Activities', coerce=int, validators=[Optional()])
    locations = SelectMultipleField(u'Locations', coerce=int, validators=[Optional()])

    mood = RadioField(label="How was the client's mood",
                      validators=[DataRequired()],
                      choices=[('angry', 'Angry'),
                               ('sad', 'Sad'),
                               ('moderate', 'Moderate'),
                               ('happy', 'Happy'),
                               ('hyperactive', 'Hyperactive')])

    new_activity = StringField("Add new activity: ")
    new_location = StringField("Add new location: ")
    #incident = BooleanField("Were there any incidents?")
    incidents_text = TextAreaField("Incident Report")
    report_text = TextAreaField("Session Report")
    
    incident = RadioField(choices=[('Yes','Yes'),('No','No')], validators=[Optional()])
    # incident = SelectField(
    #             choices=[(True, 'Yes'), (False, 'No')],
    #             validators=[InputRequired()],
    #             coerce=lambda x: x == 'True'
    #         )
    
    
    incident_yes = SubmitField("Yes")
    incident_no = SubmitField("No")
    
    submit = SubmitField('Submit')

    #clients = SelectField('Clients', coerce=int)



class ClientAddShiftForm(FlaskForm):
    
    date = DateField('Choose a date', validators=[DataRequired()])
    start_time = DateTimeField('Start time (hours:mins)',format='%H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End time (hours:mins)', format='%H:%M', validators=[DataRequired()])
    frequency = SelectField('Frequency', choices = [('one-off', 'One-off'), ('daily', 'Daily'), ('weekly','Weekly'), ('fortnightly', 'Fortnightly'), ('monthly', 'Monthly')], validators=[DataRequired()])
    worker = SelectField('Support Workers', coerce=int)
    #activity = StringField('Activity', validators=[DataRequired()])
    #location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')

class WorkerAddShiftForm(FlaskForm):
    date = DateField('Choose a date', validators=[DataRequired()])
    start_time = DateTimeField('Start time (hours:mins)', format='%H:%M', validators=[DataRequired()])
    end_time = DateTimeField('End time (hours:mins)', format='%H:%M', validators=[DataRequired()])
    frequency = SelectField('Frequency', choices = [('one-off', 'One-off'), ('daily', 'Daily'), ('weekly','Weekly'), ('fortnightly', 'Fortnightly'), ('monthly', 'Monthly')], validators=[DataRequired()])
    client = SelectField('Clients', coerce=int)
    activity = StringField('Activity', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')




