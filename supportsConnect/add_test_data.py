from app import app, db
from app.models import *
from datetime import date, time, datetime


'''

Password = "test" (for all test users)

Clients - with guardian 
    
    -   jasonsmith@hotmail.com
    -   greg@gmail.com

Clients - no guardian 

    - jenny@hotmail.com

Support Workers 

    - rebecca@hotmail.com
    - steve@hotmail.com
    - dave@hotmail.com

'''

def get_or_create(session, model, **kwargs):
    print("- Instance Added")
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        print(instance)
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def add_users_to_database():
    
    ## CLIENTS - with guardian ##
    print("Adding test users:")
    get_or_create(db.session, Clients, email = 'jasonsmith@hotmail.com', accountType = 'client', asGuardian = True,
                    firstName = 'Jason', lastName = 'Smith', ndisNumber = '3453453', homeAddress = '123 Test St, Buckingham Palace',
                    age = 25, gender = 'male', contactNo = '047733333',
                    shortBio = 'Hi guys, I am  a client and this is my bio',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    guardianFirstName = 'Bethany',guardianLastName = 'Smith', ndisPlan = 'plan managed', 
                    planManager = 'plan partners', invoiceEmail = 'planpartners@hotmail.com')

    get_or_create(db.session, Clients, email = 'greg@hotmail.com', accountType = 'client', asGuardian = True,
                    firstName = 'Greg', lastName = 'Burrows', ndisNumber = '345324', homeAddress = '155 Test St, Crystal Palace',
                    age = 15, gender = 'male', contactNo = '04773234',
                    shortBio = 'Hi guys, I am  a client and this is my bio',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    guardianFirstName = 'Lina',guardianLastName = 'Burrows', ndisPlan = 'self managed')

    ## CLIENTS - no guardian ##

    get_or_create(db.session, Clients, email = 'jenny@hotmail.com', accountType = 'client', asGuardian = False,
                    firstName = 'Jenny', lastName = 'Davids', ndisNumber = '3453453', homeAddress = '123 Test St, Northern Beaches Ugh',
                    age = 20, gender = 'female', contactNo = '0423434234',
                    shortBio = 'Hi guys, I am  a client and this is my bio',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    ndisPlan = 'plan managed', planManager = 'plan partners', invoiceEmail = 'planpartners@hotmail.com')

    ## SUPPORT WORKERS ##

    get_or_create(db.session, SupportWorkers, email = 'rebecca@hotmail.com', accountType = 'support worker', 
                    firstName = 'Rebecca', lastName = 'Kutcha',  homeAddress = '123 Test St, Buckingham Palace',
                    age = 27, gender = 'female', contactNo = '047733333',
                    shortBio = 'Hi guys, I am  a support worker and this is my bio',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    languages = 'English, French', interests = 'Bike riding, walking, swimming, talking')

    get_or_create(db.session, SupportWorkers, email = 'steve@hotmail.com', accountType = 'support worker', 
                    firstName = 'Steve', lastName = 'Waters',  homeAddress = '123 Test St, Buckingham Palace',
                    age = 20, gender = 'male', contactNo = '04774443',
                    shortBio = 'Hi guys, I am  a support worker and this is my bio',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    languages = 'English, Spanish', interests = 'Football, tennis, swimming, talking')

    get_or_create(db.session, SupportWorkers, email = 'dave@hotmail.com', accountType = 'support worker', 
                    firstName = 'Dave', lastName = 'Young', homeAddress = '123 Test St, Buckingham Palace',
                    age = 20, gender = 'male', contactNo = '04774443',
                    shortBio = 'Hi guys, I am  a support worker and this is my bio',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    languages = 'English, Spanish', interests = 'Golf, cooking, swimming, talking')

def create_connections():

    print("Creating user connections:")

    # Connect greg and rebecca 
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 4, supportWorkerStatus = 'accepted',
                    clientId = 2, clientStatus = 'accepted')
    # Connect greg and steve
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 5, supportWorkerStatus = 'accepted',
                    clientId = 2, clientStatus = 'accepted')    
    # Greg send connection request to dave
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 6, supportWorkerStatus = 'sent',
                    clientId = 2)    
    # Connect Jason and Rebecca
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 4, supportWorkerStatus = 'accepted',
                    clientId = 1, clientStatus = 'accepted')        
    # Connect Jason and Dave
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 6, supportWorkerStatus = 'accepted',
                    clientId = 1, clientStatus = 'accepted')          
    # Steve send connection request to Jason
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 5, supportWorkerStatus = 'sent',
                    clientId = 1)  
    # Connect Jenny and Dave
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 6, supportWorkerStatus = 'accepted',
                    clientId = 3, clientStatus = 'accepted') 
    # Jenny send connections requests to Rebecca and Steve
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 4,
                    clientId = 3, clientStatus = 'sent')    
    get_or_create(db.session, ConnectedUsers, supportWorkerId = 5,
                    clientId = 3, clientStatus = 'sent')    

def add_shifts():
    
    print("Adding shifts")
    
    get_or_create(db.session, Shifts, workerId = 4, clientId = 1, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=31))
    get_or_create(db.session, Shifts, workerId = 5, clientId = 1, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=30))
    get_or_create(db.session, Shifts, workerId = 6, clientId = 1, startTime = time(1,24,12), endTime = time(2,24,12), date = date(year=2020, month=1, day=30))

    get_or_create(db.session, Shifts, workerId = 4, clientId = 2, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=31))
    get_or_create(db.session, Shifts, workerId = 5, clientId = 2, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=30))
    get_or_create(db.session, Shifts, workerId = 6, clientId = 2, startTime = time(1,24,12), endTime = time(2,24,12), date = date(year=2020, month=1, day=30))

    get_or_create(db.session, Shifts, workerId = 4, clientId = 3, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=31))
    get_or_create(db.session, Shifts, workerId = 5, clientId = 3, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=30))
    get_or_create(db.session, Shifts, workerId = 6, clientId = 3, startTime = time(1,24,12), endTime = time(2,24,12), date = date(year=2020, month=1, day=30))


def add_activities():
    
    print("Adding activities")
    get_or_create(db.session, Activities, name = 'Football', clientId = 1)  
    get_or_create(db.session, Activities, name = 'Golf', clientId = 1)  
    get_or_create(db.session, Activities, name = 'Hockey', clientId = 1)  
 
    get_or_create(db.session, Activities, name = 'Football', clientId = 2)  
    get_or_create(db.session, Activities, name = 'Golf', clientId = 2)  
    get_or_create(db.session, Activities, name = 'Hockey', clientId = 2)  
        
    get_or_create(db.session, Activities, name = 'Tennis', clientId = 3)  
    get_or_create(db.session, Activities, name = 'Golf', clientId = 3)  
    get_or_create(db.session, Activities, name = 'Hockey', clientId = 3)     


add_users_to_database()
create_connections()
add_shifts()
add_activities()

















