from app import app, db
from app.models import *


def get_or_create(session, model, **kwargs):
    print("Then here")
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        print("FUCK")
        print(instance)
        return instance
    else:
        print("YEW")
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def add_test_data_to_database():
    
    print("ENTERS HERE")
    
    # Jason Smith 
    # Client
    # password = "test"
    
    get_or_create(db.session, Clients, email = 'Jasonsmith@hotmail.com', accountType = 'client',
                    firstName = 'Jason', lastName = 'Smith', ndisNumber = '3453453', 
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    guardianFirstName = 'Janeene', asGuardian = True, ndisPlan = 'plan managed', 
                    planManager = 'plan partners', invoiceEmail = 'planpartners@fake.com')

    get_or_create(db.session, Clients, email = 'greg@yew.com', accountType = 'client', asGuardian = True, 
                    firstName = 'Greg', lastName = 'Tuwaidan', ndisNumber = '3453453', 
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344',
                    guardianFirstName = 'Lina', ndisPlan = 'plan managed', 
                    planManager = 'plan partners', invoiceEmail = 'planpartners@fake.com')

    get_or_create(db.session, SupportWorkers, email = 'jonowschan@gmail.com', accountType = 'support worker',
                    firstName = 'Jono', lastName = 'Chan',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344')
                    
    get_or_create(db.session, SupportWorkers, email = 'james@yew.com', accountType = 'support worker',
                    firstName = 'James', lastName = 'Franklin',
                    password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344')
                    



    get_or_create(db.session, Clients, email = 'Jessmunroe@hotmail.com', accountType = 'client',
                    firstName = 'Jess', lastName = 'Munroe')

    get_or_create(db.session, Clients, email = 'Jeffre@hotmail.com')
    
    # Rolf Harris
    # Support Worker
    # password = "test"

    get_or_create(db.session, SupportWorkers, email = 'RolfHarris@example.com', accountType = 'support worker',
                  firstName = 'Rolf', lastName = 'Harris', age = 3, gender = 'male', contactNo = '04444spammm',
                  password_hash = 'pbkdf2:sha256:260000$0WLpNaXEJFoCBkqY$171259332c77a3de2a96942f29ace3d69cc9826cf1fb37815eab13cb30d08344')
    get_or_create(db.session, SupportWorkers, email = 'DavidBeckam@example.com', firstName = 'David',
                    lastName = 'Beckam', age = 33, gender = 'male', contactNo = '04444spammm')
    get_or_create(db.session, SupportWorkers, email = 'Nathan@example.com')


    #u = SupportWorkers(email='David@example.com')
    #db.session.add(u)
    #z = SupportWorkers(email='Rob@example.com')
    #db.session.add(z)

    #db.session.commit()
    
    #print('Great Success')


