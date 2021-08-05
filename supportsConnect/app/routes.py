from flask import flash, redirect, render_template, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required

#from flask_login.utils import login_required
from werkzeug.urls import url_parse
from datetime import date
from dateutil.relativedelta import relativedelta

from app import app, db
from app.forms import LoginForm, RegistrationForm, ConnectForm, ClientInformationForm, WorkerInformationForm
from app.models import *

from app.test_data import add_test_data_to_database

from wtforms import StringField

#add_test_data_to_database()


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<email>')
@login_required
def user(email):
    user = Users.query.filter_by(email=email).first_or_404()
    return render_template('user.html', user=user)

@app.route('/support_worker/<email>')
@login_required
def support_worker(email):
    user = Users.query.filter_by(email=email).first_or_404()
    return render_template('support_worker.html', user=user)


@app.route('/worker_connect', methods=['GET', 'POST'])
@login_required
def worker_connect():

    user_id = current_user.get_id()
    user = SupportWorkers.query.filter_by(id=user_id).first_or_404()
    form = ConnectForm()
    
    if form.validate_on_submit():
        
        if form.send_request.data:

            client = Clients.query.filter_by(email = form.email.data).first()
            if client:
                connection_request = ConnectedUsers(supportWorkerId = user_id, 
                                                    clientId = client.id,
                                                    supportWorkerStatus = 'sent')
                db.session.add(connection_request)
                db.session.commit()
                flash("A request has been sent")
            else:
                flash("This user doesn't exist")
            
    return render_template('worker_connect.html', form=form, user=user)


@app.route('/client_profile_personal_info', methods=['GET', 'POST'])
@login_required
def client_profile_personal_info():
        
    user_id = current_user.get_id()
    user = Clients.query.filter_by(id=user_id).first_or_404()
    form = ClientInformationForm()
    
    if form.validate_on_submit():
        
        if form.guardian_first_name.data:
            user.guardianFirstName = form.guardian_first_name.data
        if form.guardian_last_name.data:
            user.guardianLastName = form.guardian_last_name.data
        if form.first_name.data:
            user.firstName = form.first_name.data
        if form.last_name.data:
            user.lastName = form.last_name.data
        if form.phone_number.data:
            user.contactNo = form.phone_number.data
        # if form.date_of_birth.data:
        #     current_user.dateOfBirth = form.date_of_birth.data
        #     age = relativedelta(date.today(), current_user.dateOfBirth)
        #     current_user.age = age.years
        if form.age.data: 
            user.age = form.age.data
        if form.gender.data: 
            user.gender = form.gender.data        
        if form.home_address.data: 
            user.homeAddress = form.home_address.data
        if form.likes.data: 
            user.likes = form.likes.data
        if form.dislikes.data: 
            user.dislikes = form.dislikes.data
        if form.allergies.data: 
            user.allergies = form.allergies.data
        if form.health_needs.data: 
            user.healthNeeds = form.health_needs.data
        if form.short_bio.data: 
            user.shortBio = form.short_bio.data
                 
        db.session.commit()
        
    print(form.errors)

    return render_template('client_profile_personal_info.html', form=form, user=user)
    

@app.route('/client_profile_payment_details', methods=['GET', 'POST'])
@login_required
def client_profile_payment_details():
    
    user_id = current_user.get_id()
    user = Clients.query.filter_by(id=user_id).first_or_404()
    form = ClientInformationForm()
    
    if form.validate_on_submit():
        
        if form.ndis_number.data: 
            user.ndisNumber = form.ndis_number.data
        if form.ndis_plan.data: 
            user.ndisPlan = form.ndis_plan.data
        if form.plan_manager.data: 
            user.planManager = form.plan_manager.data
        if form.invoice_email.data: 
            user.invoiceEmail = form.invoice_email.data
    
        db.session.commit()
    
    return render_template('client_profile_payment_details.html', form=form, user=user)



@app.route('/worker_profile_personal_info', methods=['GET', 'POST'])
@login_required
def worker_profile_personal_info():
        
    user_id = current_user.get_id()
    user = SupportWorkers.query.filter_by(id=user_id).first_or_404()
    form = WorkerInformationForm()
    
    
    if form.validate_on_submit():
        
        if form.first_name.data:
            user.firstName = form.first_name.data
        if form.last_name.data:
            user.lastName = form.last_name.data
        if form.phone_number.data:
            user.contactNo = form.phone_number.data
        if form.date_of_birth.data:
            user.dateOfBirth = form.date_of_birth.data
            age = relativedelta(date.today(), user.dateOfBirth)
            user.age = age.years
        if form.age.data: 
            user.age = form.age.data
        if form.gender.data: 
            user.gender = form.gender.data        
        if form.home_address.data: 
            user.homeAddress = form.home_address.data
        if form.short_bio.data: 
            user.shortBio = form.short_bio.data
        if form.interests.data: 
            user.interests = form.interests.data
        if form.languages.data: 
            user.languages = form.languages.data
        
        db.session.commit()
        
    #print(form.errors)
    
    return render_template('worker_profile_personal_info.html', form=form, user=user)
    
@app.route('/worker_profile_past_experience', methods=['GET', 'POST'])
@login_required
def worker_profile_past_experience():
        
    user_id = current_user.get_id()
    user = SupportWorkers.query.filter_by(id=user_id).first_or_404()
    user_training = Training.query.filter_by(worker=user_id).order_by(Training.id).all()
    user_work_history = WorkHistory.query.filter_by(worker=user_id).order_by(WorkHistory.id).all()

    # Variables to inform the front-end if the user has clicked 
    # 'Add Training' or 'Add Work History' Buttons
    add_training2 = False
    add_training3 = False
    add_work_history2 = False
    add_work_history3 = False   
    
    # If user has no training data
    # Create new training instance
    if not user_training:
        training1 = Training(worker = user_id)
        training2 = Training(worker = user_id)
        training3 = Training(worker = user_id)
        db.session.add(training1)
        db.session.add(training2)
        db.session.add(training3)
        db.session.commit()
        
    else:
        training1 = user_training[0]
        training2 = user_training[1]
        training3 = user_training[2]
        
    # If user has no work history data
    # Create new work_history instance
    if not user_work_history:
        
        work_history1 = WorkHistory(worker = user_id)  
        work_history2 = WorkHistory(worker = user_id)  
        work_history3 = WorkHistory(worker = user_id)  
        db.session.add(work_history1)
        db.session.add(work_history2)
        db.session.add(work_history3)
        db.session.commit()
        
    else:
        work_history1 = user_work_history[0]
        work_history2 = user_work_history[1]
        work_history3 = user_work_history[2]
    
    form = WorkerInformationForm()
    
    
    if form.validate_on_submit():
        
        # Add Work History and Training buttons
        if form.add_work_history2.data:
            add_work_history2 = True
        elif form.add_work_history3.data:
            add_work_history3 = True
        elif form.add_training2.data:
            add_training2 = True
        elif form.add_training3.data:
            add_training3 = True

        
        # Work History 1
        if form.location1.data:
            work_history1.location = form.location1.data
        if form.role1.data:
            work_history1.role = form.role1.data
        if form.work_start_date1.data:
            work_history1.startDate = form.work_start_date1.data           
        if form.work_end_date1.data:
            work_history1.endDate = form.work_end_date1.data           
        
        # Work History 2
        if form.location2.data:
            work_history2.location = form.location2.data
        if form.role2.data:
            work_history2.role = form.role2.data
        if form.work_start_date2.data:
            work_history2.startDate = form.work_start_date2.data           
        if form.work_end_date2.data:
            work_history2.endDate = form.work_end_date2.data 

        
        # Work History 3
        if form.location3.data:
            work_history3.location = form.location3.data
        if form.role3.data:
            work_history3.role = form.role3.data
        if form.work_start_date3.data:
            work_history3.startDate = form.work_start_date3.data           
        if form.work_end_date3.data:
            work_history3.endDate = form.work_end_date3.data 

        # Training 1
        if form.course1.data:
            training1.course = form.course1.data
        if form.institution1.data:
            training1.institution = form.institution1.data
        if form.training_start_date1.data:
            training1.startDate = form.training_start_date1.data           
        if form.training_end_date1.data:
            training1.endDate = form.training_end_date1.data   

        # Training 2
        if form.course2.data:
            training2.course = form.course2.data
        if form.institution2.data:
            training2.institution = form.institution2.data
        if form.training_start_date2.data:
            training2.startDate = form.training_start_date2.data           
        if form.training_end_date2.data:
            training2.endDate = form.training_end_date2.data  

        # Training 3
        if form.course3.data:
            training3.course = form.course3.data
        if form.institution3.data:
            training3.institution = form.institution3.data
        if form.training_start_date3.data:
            training3.startDate = form.training_start_date3.data           
        if form.training_end_date3.data:
            training3.endDate = form.training_end_date3.data  

        db.session.commit()
        
    #print(form.errors)
    
    return render_template('worker_profile_past_experience.html', 
                           form=form, user=user, 
                           add_training2 = add_training2, add_training3 = add_training3, 
                           add_work_history2 = add_work_history2, add_work_history3 = add_work_history3, 
                           work_history1 = work_history1, work_history2 = work_history2, work_history3 = work_history3,
                           training1 = training1, training2 = training2, training3 = training3)




