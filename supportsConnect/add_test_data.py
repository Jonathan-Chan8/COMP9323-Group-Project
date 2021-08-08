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
   
   ## SHIFTS COMPLETED ##
   # ID: 1,2,4,6,9
   
    #get_or_create(db.session, Shifts, shiftStatus = 'completed', workerId = 4, clientId = 1, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=31))
    shift1 = Shifts(shiftStatus = 'completed', workerId = 4, clientId = 1, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=31))
    shift2 = Shifts(shiftStatus = 'completed', workerId = 5, clientId = 1, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=30))
    shift4 = Shifts(shiftStatus = 'completed', workerId = 4, clientId = 2, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=31))
    shift6 = Shifts(shiftStatus = 'completed', workerId = 6, clientId = 2, startTime = time(1,24,12), endTime = time(2,24,12), date = date(year=2020, month=1, day=30))
    shift9 = Shifts(shiftStatus = 'completed', workerId = 6, clientId = 3, startTime = time(1,24,12), endTime = time(2,24,12), date = date(year=2020, month=1, day=30))
    db.session.add(shift1)
    db.session.add(shift2)
    db.session.add(shift4)
    db.session.add(shift6)
    db.session.add(shift9)
    
    print("Adding Activities")
    activity1 = Activities(name = 'Football', clientId = 1)
    activity2 = Activities(name = 'Golf', clientId = 1)    
    activity3 = Activities(name = 'Hockey', clientId = 1)
    
    activity4 = Activities(name = 'Tennis', clientId = 2)
    activity5 = Activities(name = 'Golf', clientId = 2)    
    activity6 = Activities(name = 'Rugby', clientId = 2)

    activity7 = Activities(name = 'Hockey', clientId = 3)
    activity8 = Activities(name = 'Badminton', clientId = 3)    
    activity9 = Activities(name = 'Ice Skating', clientId = 3)
    db.session.add(activity1)
    db.session.add(activity2)
    db.session.add(activity3)
    db.session.add(activity4)
    db.session.add(activity5)
    db.session.add(activity6)
    db.session.add(activity7)
    db.session.add(activity8)
    db.session.add(activity9)
    
    print("Appending shifts to activities")
    shift1.activities.append(activity1)
    shift1.activities.append(activity3) 
    
    shift2.activities.append(activity1)
    shift2.activities.append(activity2)
    
    shift4.activities.append(activity6)

    shift6.activities.append(activity4)
    shift6.activities.append(activity5)
    
    shift9.activities.append(activity8)
    shift9.activities.append(activity9)
    
    db.session.commit()
    

    get_or_create(db.session, Shifts, shiftStatus = 'pending', workerId = 6, clientId = 1, startTime = time(1,24,12), endTime = time(2,24,12), date = date(year=2020, month=1, day=30))
    get_or_create(db.session, Shifts, shiftStatus = 'scheduled', workerId = 5, clientId = 2, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2021, month=1, day=30))

    get_or_create(db.session, Shifts, shiftStatus = 'pending', workerId = 4, clientId = 3, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2020, month=1, day=31))
    get_or_create(db.session, Shifts, shiftStatus = 'scheduled', workerId = 5, clientId = 3, startTime = time(3,24,12), endTime = time(5,24,12), date = date(year=2021, month=1, day=30))
    

def add_reports():
    
    print("Adding reports")
    
    get_or_create(db.session, Reports, mood = 'sad', incident = True, incidentReport = 'He bit me.', sessionReport = 'Reall good fun', shift_id = 1)
    get_or_create(db.session, Reports, mood = 'hyperactive', incident = True, incidentReport = 'He ran at me.', sessionReport = 'Not very good', shift_id = 2)
    get_or_create(db.session, Reports, mood = 'happy', incident = False,  sessionReport = 'Such a good time', shift_id = 4)
    get_or_create(db.session, Reports, mood = 'happy', incident = False,  sessionReport = 'Really good session', shift_id = 6)
    get_or_create(db.session, Reports, mood = 'sad', incident = True, incidentReport = 'He cried the whole time',  sessionReport = 'Pretty embarrassing', shift_id = 9)

# def add_activities():
    
#     print("Adding activities")
#     get_or_create(db.session, Activities, name = 'Football', clientId = 1)  
#     get_or_create(db.session, Activities, name = 'Golf', clientId = 1)  
#     get_or_create(db.session, Activities, name = 'Hockey', clientId = 1)  
 
#     get_or_create(db.session, Activities, name = 'Football', clientId = 2)  
#     get_or_create(db.session, Activities, name = 'Golf', clientId = 2)  
#     get_or_create(db.session, Activities, name = 'Hockey', clientId = 2)  
        
#     get_or_create(db.session, Activities, name = 'Tennis', clientId = 3)  
#     get_or_create(db.session, Activities, name = 'Golf', clientId = 3)  
#     get_or_create(db.session, Activities, name = 'Hockey', clientId = 3)     

#def append_activities_to_shifts():
    
    #shift.activities.append(activity)


add_users_to_database()
create_connections()
add_shifts()
add_reports()


















