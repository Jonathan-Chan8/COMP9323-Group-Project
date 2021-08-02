### models.py ###

from app import db
from datetime import datetime 
import enum

NameValue = db.VARCHAR(20)
Description = db.VARCHAR(50)


class Users(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.VARCHAR(20))
	accountType = db.Column(db.Enum('client', 'guardian', name = 'account_type'))
	firstName = db.Column(NameValue)
	lastName = db.Column(NameValue)
	dateOfBirth = db.Column(db.Date)
	age = db.Column(db.Integer)
	gender = db.Column(db.Enum('male', 'female', 'other', name = 'gender_type'))
	contactNo = db.Column(db.VARCHAR(15))
	homeAddress = db.Column(Description)
	shortBio = db.Column(db.VARCHAR(140))

	def __repr__(self):
		return '<User {}>'.format(self.email)


class Clients(Users):

	id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
	asGuardian = db.Column(db.BOOLEAN)
	allergies = db.Column(Description)
	likes = db.Column(Description)
	dislikes = db.Column(Description)
	healthNeeds = db.Column(Description)

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
	startDate = db.Column(db.Date)
	endDate = db.Column(db.Date)

	def __repr__(self):
		return '<Work History {}>'.format(self.location)


class Training (db.Model):

	id = db.Column(db.Integer, primary_key = True)
	worker = db.Column(db.Integer, db.ForeignKey('support_workers.id'))
	subject = db.Column(NameValue)
	institution = db.Column(NameValue)
	startDate = db.Column(db.Date)
	endDate = db.Column(db.Date)

	def __repr__(self):
		return '<Training {}>'.format(self.subject)


class ConnectedUsers(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	supportWorkerId = db.Column(db.Integer, db.ForeignKey('support_workers.id'))
	clientId = db.Column(db.Integer, db.ForeignKey('clients.id'))
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
	activity = db.Column(db.Integer, db.ForeignKey('activities.id'))
	mood = db.Column(db.Enum('angry', 'sad', 'moderate', 'happy', 'hyperactive', name = 'moods'))
	incident = db.Column(db.BOOLEAN, default = False)
	incidentReport = db.Column(db.Text)
	sessionReport = db.Column(db.Text)



