### models.py ###

from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

NameValue = db.VARCHAR(30)
Description = db.VARCHAR(50)


class Users(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    accountType = db.Column(db.Enum('client', 'support worker', name = 'account_type'))
    firstName = db.Column(NameValue)
    lastName = db.Column(NameValue)
    dateOfBirth = db.Column(db.Date)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female', 'other', name = 'gender_type'))
    contactNo = db.Column(db.VARCHAR(15))
    homeAddress = db.Column(Description)
    shortBio = db.Column(db.VARCHAR(140))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

class Clients(Users):

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    asGuardian = db.Column(db.BOOLEAN)
    guardianFirstName = db.Column(NameValue)
    guardianLastName = db.Column(NameValue)
    allergies = db.Column(Description)
    likes = db.Column(Description)
    dislikes = db.Column(Description)
    healthNeeds = db.Column(Description)
    ndisNumber = db.Column(db.Integer)
    ndisPlan = db.Column(db.Enum('self managed', 'plan managed', name = 'ndisPlan'))
    planManager = db.Column(NameValue)
    invoiceEmail = db.Column(db.String(120))

    def __repr__(self):
        return '<Client {}>'.format(self.id)


class SupportWorkers(Users):

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    languages = db.Column(Description)
    interests = db.Column(Description)

    def __repr__(self):
        return '<Client {}>'.format(self.id)


class WorkHistory (db.Model):

    id = db.Column(db.Integer, primary_key = True)
    worker = db.Column(db.Integer, db.ForeignKey('support_workers.id'))
    location = db.Column(Description)
    role = db.Column(NameValue)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)

    def __repr__(self):
        return '<Work History {}>'.format(self.role)


class Training (db.Model):

    id = db.Column(db.Integer, primary_key = True)
    worker = db.Column(db.Integer, db.ForeignKey('support_workers.id'))
    course = db.Column(NameValue)
    institution = db.Column(NameValue)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)

    def __repr__(self):
        return '<Training {}>'.format(self.course)


class ConnectedUsers(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    supportWorkerId = db.Column(db.Integer, db.ForeignKey('support_workers.id'))
    supportWorkerStatus = db.Column(db.Enum('sent', 'accepted', name = 'supportWorkerStatus'))
    clientId = db.Column(db.Integer, db.ForeignKey('clients.id'))
    clientStatus = db.Column(db.Enum('sent', 'accepted','declined', name = 'clientStatus'))
    dateConnected = db.Column(db.Date)

    def __repr__(self):
        return '<Connected Pairs {}>'.format(self.supportWorkerId)


class Shifts(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    connectedId = db.Column(db.Integer, db.ForeignKey('connected_users.id'))
    shiftStatus = db.Column(db.BOOLEAN, default = True)
    workerStatus = db.Column(db.BOOLEAN, default = True)
    clientStatus = db.Column(db.BOOLEAN, default = True)
    startTime = db.Column(db.TIMESTAMP)
    endTime = db.Column(db.TIMESTAMP)
    duration = db.Column(db.Interval)
    frequency = db.Column(db.Enum('daily', 'weekly', 'fortnightly', 'monthly', name = 'frequencies'))


class Activities(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    shift = db.Column(db.Integer, db.ForeignKey('shifts.id'))
    location = db.Column(Description)


class Reports(db.Model):

    id = db.Column(db.Integer, primary_key = True)	
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'))
    activity = db.Column(db.Integer, db.ForeignKey('activities.id'))
    mood = db.Column(db.Enum('angry', 'sad', 'moderate', 'happy', 'hyperactive', name = 'moods'))
    incident = db.Column(db.BOOLEAN, default = False)
    incidentReport = db.Column(db.Text)
    sessionReport = db.Column(db.Text)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))









