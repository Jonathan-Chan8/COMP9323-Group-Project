from flask import flash, redirect, render_template, request
from flask.helpers import url_for
from flask_login import current_user, login_user, logout_user, login_required

#from flask_login.utils import login_required
from werkzeug.urls import url_parse

from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta

from app import app, db
from app.forms import (LoginForm, RegistrationForm, ConnectForm, 
                        ClientInformationForm, WorkerInformationForm, ConnectRequestForm,
                        AccountForm, AddShiftForm, WorkerReportForm, ReportingForm)
from sqlalchemy import desc
from app.models import *

from wtforms import StringField



#------------------------------------------------------------------------------
#                         Homepage and Login 
#------------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
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
            
            if user.accountType == 'support worker':
                return redirect(url_for('worker_dashboard', email=user.email))
            elif user.accountType == 'client':
                return redirect(url_for('client_dashboard', email=user.email))
            else:
                next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#------------------------------------------------------------------------------
#                                Sign Up 
#------------------------------------------------------------------------------

@app.route('/sign_up_user_type', methods=['GET', 'POST'])
def sign_up_user_type():
    form = RegistrationForm()

    if form.support_worker.data:
        return redirect(url_for('sign_up_support_worker'))
    if form.client.data:
        return redirect(url_for('sign_up_client_type'))
    
    return render_template('/sign_up_user_type.html', form=form)

@app.route('/sign_up_client_type', methods=['GET', 'POST'])
def sign_up_client_type():
    
    form = RegistrationForm()

    if form.client_self_managed.data:
        return redirect(url_for('sign_up_client'))
    if form.client_guardian.data:
        return redirect(url_for('sign_up_client_guardian'))
        
    return render_template('/sign_up_client_type.html', form=form)

@app.route('/sign_up_support_worker', methods=['GET', 'POST'])
def sign_up_support_worker():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():

        user = SupportWorkers(email=form.email.data)
        user.set_password(form.password.data)
        user.firstName = form.first_name.data
        user.lastName = form.last_name.data
        user.accountType = 'support worker'
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login', email=user.email))
    
    return render_template('sign_up_support_worker.html', title='Sign Up', form=form)

@app.route('/sign_up_client', methods=['GET', 'POST'])
def sign_up_client():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():

        user = Clients(email=form.email.data)
        user.set_password(form.password.data)
        user.firstName = form.first_name.data
        user.lastName = form.last_name.data
        user.asGuardian = False
        user.accountType = 'client'
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('sign_up_client.html', title='Sign Up', form=form)

@app.route('/sign_up_client_guardian', methods=['GET', 'POST'])
def sign_up_client_guardian():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        user = Clients(email=form.email.data)
        user.set_password(form.password.data)
        user.guardianFirstName = form.guardian_first_name.data
        user.guardianFirstName = form.guardian_last_name.data
        user.firstName = form.first_name.data
        user.lastName = form.last_name.data
        user.asGuardian = True
        user.accountType = 'client'
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('sign_up_client_guardian.html', title='Sign Up', form=form)


#------------------------------------------------------------------------------
#                             Dashboard 
#------------------------------------------------------------------------------

@app.route('/worker_dashboard/')
@login_required
def worker_dashboard():
    user_id = current_user.get_id()
    user = SupportWorkers.query.filter_by(id=user_id).first_or_404()
    return render_template('worker_dashboard.html', user=user)

@app.route('/client_dashboard/')
@login_required
def client_dashboard():
    user_id = current_user.get_id()
    user = Clients.query.filter_by(id=user_id).first_or_404()
    return render_template('client_dashboard.html', user=user)


#------------------------------------------------------------------------------
#                                   Reports
#------------------------------------------------------------------------------

class Report_Card:
    
    def __init__(self, client_name, worker_name, date, activities, incident): #locations,  
        
        self.client_name = client_name
        self.worker_name = worker_name
        self.date = date
        # self.locations = locations
        self.activities = activities
        self.incident = incident
        

@app.route('/worker_reports', methods=['GET', 'POST'])
@login_required
def worker_reports():

    # Current user 
    user_id = current_user.get_id()
    user = Users.query.filter_by(id=user_id).first_or_404()
    
    form = WorkerReportForm()
        
    # Retrieve all of the current user's clients
    connected_clients = db.session.query(Users).join(ConnectedUsers, ConnectedUsers.clientId == Users.id).filter(ConnectedUsers.supportWorkerId == user_id).filter(ConnectedUsers.supportWorkerStatus == 'accepted').all()
    
    connected_clients_ids = [row.id for row in connected_clients]
    print(connected_clients_ids)
    
    # Add these client's to the Client FILTER
    form.clients.choices = [(row.id, row.firstName) for row in connected_clients]
    
    
    # FILTER SELECTED
    if form.validate_on_submit():    
        
        print("GETS HERE")
        print(form.clients.data)
        # Client filter selected 
        if form.client_submit.data:
            
            # Retrieve the client instance
            client = Clients.query.filter_by(id=form.clients.data).first()
            
            # Update the list of activities 
            client_activities = Activities.query.filter_by(clientId = client.id).distinct().all()   
            form.activities.choices = [(row.id, row.name) for row in client_activities] 
            
            shifts = Shifts.query.filter_by(shiftStatus = 'completed').filter_by(clientId = form.clients.data).order_by(desc(Shifts.date)).order_by(desc(Shifts.startTime)).all()
        
        # Activity filter selected 
        if form.activity_submit.data:

            shifts = db.session.query(Shifts).filter(Shifts.shiftStatus == 'completed').order_by(desc(Shifts.date)).order_by(desc(Shifts.startTime))
            shifts_refined = []
            for shift in shifts:
                for activity in shift.activities:
                    if activity.id == form.activities.data:
                        shifts_refined.append(shift)
            
            shifts = shifts_refined
            
    # NO FILTER SELECTED
    else:
         
        # Retrieve all connected client activities 
        activities = db.session.query(Activities).filter(Activities.clientId.in_(connected_clients_ids)).distinct()
        form.activities.choices = [(row.id, row.name) for row in activities]
        
        # Retrieve all completed shifts (i.e. Shifts that have reports) 
        
        shifts = db.session.query(Shifts).filter(Shifts.shiftStatus == 'completed').filter(Shifts.clientId.in_(connected_clients_ids)).order_by(desc(Shifts.date)).order_by(desc(Shifts.startTime))
        
    reports = []

    for shift in shifts:
        
        # Grab the shift report
        report = Reports.query.filter_by(shift_id=shift.id).first()

        # Grab the client of the shift
        client = Clients.query.filter_by(id=shift.clientId).first()
        client_full_name = client.firstName + ' ' +  client.lastName
        
        # Grab the support worker of the shift
        support_worker = SupportWorkers.query.filter_by(id=shift.workerId).first()
        support_worker_full_name = support_worker.firstName + ' ' +  support_worker.lastName 
        
        # Shift Incidents?
        incident = 'No'
        if report: # GET RID OF THIS LINE ONCE FULLY IMPLIMENTED
            if report.incident:
                incident = 'Yes'
            else:
                incident = 'No'
        
        # Create the report card for the shift
        report_card = Report_Card(client_full_name,
                                  support_worker_full_name,
                                  shift.date,
                                  shift.activities,
                                  incident)
        
        reports.append(report_card)
                                
    return render_template('worker_reports.html', user=user, form=form, reports=reports)


    ## Append every activity to every shift ##
    
    # shifts = Shifts.query.all()
    
    # activities = Activities.query.all()
    
    # for shift in shifts:
    #     for activity in activities:
    #         shift.activities.append(activity)
    
    # db.session.commit()
    
    
    ## Creating activities and adding them to shifts ##
    
    # shift = Shifts.query.first()
    # activity = Activities(name = 'Tennis', clientId = 1)  
        
    # shift.activities.append(activity)
    # db.session.commit()
    
    
    ## Getting a shifts activities ##
    
    # shift = Shifts.query.first()
    # for activity in shift.activities:
    #     print(activity.name)
    
    ## Getting a client's activities ##
    
    # client_activities = Activities.query.filter_by(clientId = 1).distinct().all()
    
    # for activity in client_activities:
    #     print(activity.name)
    
    
    ## Filtering reports for a given activity ##
    
    # shifts_refined = []
    # shifts = Shifts.query.filter_by(clientId = 1).all() # Retrieve shifts for a given client
    # print(shifts)
    
    # for shift in shifts:
    #     for activity in shift.activities:
    #         print(activity.name)
    #         if activity.name == 'Tennis':       # Put the activity here
    #             shifts_refined.append(shift)
    # print(shifts_refined)

    
    ## Get a support worker's clients ##
    
    # clients = ConnectedUsers.query.filter_by(supportWorkerId = user_id).filter_by(clientStatus = 'accepted').all()
    # for client in clients:
    #     print(client.firstName)
        
    


@app.route('/worker_complete_shift_report', methods=['GET', 'POST'])
@login_required
def worker_complete_shift_report():
    
    # ASSUMES THAT A SHIFT OBJECT IS PASSED FROM shift_pending
    # Add 'shift' as an argument 
    
    # But in the mean time
    shift = Shifts.query.first()
    
    # Retrieve the client's name 
    client = Clients.query.filter_by(id=shift.clientId).first_or_404()
    client_full_name = client.firstName + ' ' +  client.lastName
    incidents_check = ''
    
    form = ReportingForm()
    
    # Retrieve the client's activities
    client_activities = Activities.query.filter_by(clientId = client.id).distinct().all()   
    form.activities.choices = [(row.id, row.name) for row in client_activities]
        
    if form.validate_on_submit():
        
    # Support Worker click's SUBMIT
        report = Reports(shift_id=shift.id,
                    mood=form.mood.data,
                    incident=form.incident.data,
                    incidentReport=form.incidents_text.data,
                    sessionReport=form.report_text.data)
        

        # User creates a new activity
        if form.new_activity.data:
            activity = Activities(name = form.new_activity.data, clientId = client.id)  
            shift.activities.append(activity)
            db.session.add(activity)
        
        # User chooses some activities
        for activity_id in form.activities.data:
            selected_activity = Activities.query.filter_by(id = activity_id).distinct().first() 
            shift.activities.append(selected_activity)
            
        shift.shiftStatus = 'completed'
        db.session.add(report)
        db.session.commit()
        return redirect(url_for('worker_reports')) # CHANGE THIS TO 'shifts_completed'
        
    
    return render_template('worker_complete_shift_report.html', shift=shift, 
                           form=form, client_full_name=client_full_name, incidents=incidents_check)
    

#------------------------------------------------------------------------------
#                        My Clients / Support Workers
#------------------------------------------------------------------------------

@app.route('/client_my_support_workers')
@login_required
def client_my_support_workers():

    # Current user = Client
    user_id = current_user.get_id()
    user = Users.query.filter_by(id=user_id).first_or_404()
    
    # Retrieve all of the client's connected support workers
    connections = ConnectedUsers.query.filter_by(clientId=user_id).all()
    connection_data = {}
    
    for connection in connections:
        # Obtain all user connections     
        if connection.supportWorkerStatus == 'accepted' and connection.clientStatus == 'accepted':
            
            support_worker_id = connection.supportWorkerId     
            support_worker = SupportWorkers.query.filter_by(id=support_worker_id).first_or_404()
            full_name = support_worker.firstName + ' ' +  support_worker.lastName
            connection_data[support_worker_id] = full_name

    
    return render_template('client_my_support_workers.html', connections = connection_data)


@app.route('/worker_my_clients')
@login_required
def worker_my_clients():
    
    # Current user = Support Worker
    user_id = current_user.get_id()
    user = Users.query.filter_by(id=user_id).first_or_404()

    # Retrieve all of the support worker's connected clients
    connections = ConnectedUsers.query.filter_by(supportWorkerId=user_id).all()
    connection_data = {}
    
    for connection in connections:
        # Obtain all user connections     
        if connection.clientStatus == 'accepted' and connection.supportWorkerStatus == 'accepted':
            
            client_id = connection.clientId     
            client = Clients.query.filter_by(id=client_id).first_or_404()
            full_name = client.firstName + ' ' +  client.lastName
            connection_data[client_id] = full_name
                
    return render_template('worker_my_clients.html', connections = connection_data)


#------------------------------------------------------------------------------
#                               Connect 
#------------------------------------------------------------------------------

@app.route('/worker_connect', methods=['GET', 'POST'])
@login_required
def worker_connect():

    user_id = current_user.get_id()
    user = SupportWorkers.query.filter_by(id=user_id).first_or_404()
    form = ConnectForm()
    
    if form.validate_on_submit():
        # Support Worker submits a connection request to a Client
        if form.send_request.data:
            client = Clients.query.filter_by(email = form.email.data).first()
            
            if client:
                # Check if connection request already exists
                connection_exists = ConnectedUsers.query.filter_by(supportWorkerId=user_id).filter_by(clientId=client.id).first()
                if connection_exists:
                    if connection_exists.clientStatus == 'accepted':
                        flash("You are already connected with this client")
                    else:
                        flash("A connection request has already been made")
                    return render_template('worker_connect.html', form=form, user=user)
                else:
                    # 
                    connection_request = ConnectedUsers(supportWorkerId = user_id, 
                                                        clientId = client.id,
                                                        supportWorkerStatus = 'sent')
                db.session.add(connection_request)
                db.session.commit()
                flash("A request has been sent")
            else:
                flash("This user doesn't exist")
            
    return render_template('worker_connect.html', form=form, user=user)


@app.route('/client_connect', methods=['GET', 'POST'])
@login_required
def client_connect():

    user_id = current_user.get_id()
    user = Clients.query.filter_by(id=user_id).first_or_404()
    form = ConnectForm()
    
    if form.validate_on_submit():
        # Client submits a connection request to a support worker
        if form.send_request.data:
            support_worker = SupportWorkers.query.filter_by(email = form.email.data).first()
            
            if support_worker:
                # Check if connection request already exists
                connection_exists = ConnectedUsers.query.filter_by(clientId=user_id).filter_by(supportWorkerId=support_worker.id).first()
                if connection_exists:
                    if connection_exists.supportWorkerStatus == 'accepted':
                        flash("You are already connected with this support worker")
                    else:
                        flash("A connection request has already been made")
                    return render_template('client_connect.html', form=form, user=user)
                else:
                    # 
                    connection_request = ConnectedUsers(clientId = user_id, 
                                                        supportWorkerId = support_worker.id,
                                                        clientStatus = 'sent')
                db.session.add(connection_request)
                db.session.commit()
                flash("A request has been sent")
            else:
                flash("This user doesn't exist")
            
    return render_template('client_connect.html', form=form, user=user)

@app.route('/client_connect_requests', methods=['GET', 'POST'])
@login_required
def client_connect_requests():

    user_id = current_user.get_id()
    user = Clients.query.filter_by(id=user_id).first_or_404()
    connections = ConnectedUsers.query.filter_by(clientId=user_id).all()
    requests = {}
    
    # Obtain all support worker connection requests 
    for connection in connections:
        if connection.supportWorkerStatus == 'sent':
                         
            support_worker_id = connection.supportWorkerId     
            support_worker = SupportWorkers.query.filter_by(id=support_worker_id).first_or_404()
            full_name = support_worker.firstName + ' ' +  support_worker.lastName
            requests[support_worker_id] = full_name
    
    return render_template('client_connect_requests.html', user=user, requests=requests)


@app.route('/worker_connect_requests', methods=['GET', 'POST'])
@login_required
def worker_connect_requests():

    user_id = current_user.get_id()
    user = SupportWorkers.query.filter_by(id=user_id).first_or_404()
    connections = ConnectedUsers.query.filter_by(supportWorkerId=user_id).all()
    requests = {}
    
    # Obtain all client connection requests 
    for connection in connections:
        if connection.clientStatus == 'sent':
                         
            client_id = connection.clientId     
            client = Clients.query.filter_by(id=client_id).first_or_404()
            full_name = client.firstName + ' ' +  client.lastName
            requests[client_id] = full_name
    
    return render_template('worker_connect_requests.html', user=user, requests=requests)

@app.route('/accept_request', methods=['GET', 'POST'])
@login_required
def accept_request():

    # Current user -> The user that received the request
    user_id = current_user.get_id()
    user = Users.query.filter_by(id=user_id).first_or_404()
    
    # Current user response to the request
    user_response = request.json
    response = user_response['response']
    
    # Sender -> The person who sent the request
    sender_id = user_response['sender_id']
    
    # Retrieve the connection object from the database
    # -> Current user is a client
    if user.accountType == 'client':
        connection = ConnectedUsers.query.filter_by(clientId=user_id).filter_by(supportWorkerId=sender_id).first()

    # -> Current user is a support worker
    elif user.accountType == 'support worker':
        connection = ConnectedUsers.query.filter_by(supportWorkerId=user_id).filter_by(clientId=sender_id).first()
        
    if connection:
        # -> Current user accepted the request
        if user_response['response'] == 'accept':
            connection.supportWorkerStatus = 'accepted'
            connection.clientStatus = 'accepted'
            flash("You are now connected")
        # -> Current user declined the request
        elif user_response['response'] == 'decline':
            db.session.delete(connection)  # Remove the connection object
            flash("You have successfully declined the request")
        db.session.commit()
        
    return render_template('accept_request.html')


#------------------------------------------------------------------------------
#                             View Profile 
#------------------------------------------------------------------------------

## Client viewing a support worker's profile ##

@app.route('/client_view_profile/<worker_id>', methods=['GET'])
@login_required
def client_view_profile(worker_id):
    
    support_worker = SupportWorkers.query.filter_by(id=worker_id).first_or_404()  

    work_history = WorkHistory.query.filter_by(worker=worker_id).all() 
    training = Training.query.filter_by(worker=worker_id).order_by(Training.id).all()
    
    actual_work_history = []
    actual_training = []
    
    # Iterate through the 3 user work history instances 
    # and obtain those that the user has added to
    for work in work_history:
        if work.location or work.role:
            actual_work_history.append(work)
   
    # Iterate through the 3 user training instances 
    # and obtain those that the user has added to
    for t in training:
        if t.course or t.institution:
            actual_training.append(t)

    return render_template('client_view_profile.html', support_worker=support_worker, training=actual_training, work_history=actual_work_history)


## Support Worker viewing a client's profile ##

@app.route('/worker_view_profile/<client_id>', methods=['GET'])
@login_required
def worker_view_profile(client_id):
    
    print(client_id)        
    client = Clients.query.filter_by(id=client_id).first_or_404()    
    
    return render_template('worker_view_profile.html', client=client)


#------------------------------------------------------------------------------
#                             Edit Profile 
#------------------------------------------------------------------------------

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
        flash("Your personal information was successfully updated")
        
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
        flash("Your payment details were successfully updated")
    
    return render_template('client_profile_payment_details.html', form=form, user=user)


@app.route('/worker_profile_personal_info', methods=['GET', 'POST'])
@login_required
def worker_profile_personal_info():
        
    user_id = current_user.get_id()
    print(user_id)
    user = SupportWorkers.query.filter_by(id=user_id).first_or_404()
    print("GETS TO HERE")
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
    # Create 3 new training instance
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
    # Create 3 new work_history instance
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


#------------------------------------------------------------------------------
#                                 Account
#------------------------------------------------------------------------------


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    # Current user
    user_id = current_user.get_id()
    user = Users.query.filter_by(id=user_id).first_or_404()
    
    form = AccountForm()

    if form.validate_on_submit():
        
        # Check if user provides the right email address
        if user.email == form.email.data:
            
            # Update the users password
            user.set_password(form.password.data)
            db.session.commit()
            flash("Your password has been updated!")
        else:
            flash("Error: Email Address not found. Please provide the email address used to login to this account.")

    return render_template('account.html', user=user, form=form)










