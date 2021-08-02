from app import app, db
from app.models import *




def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def add_test_data_to_database():
	
	get_or_create(db.session, Clients, email = 'Jasonsmith@hotmail.com', password = 'password', accountType = 'client',
					firstName = 'Jason', lastName = 'Smith')

	get_or_create(db.session, Clients, email = 'Jessmunroe@hotmail.com', password = 'password', accountType = 'client',
					firstName = 'Jess', lastName = 'Munroe')

	get_or_create(db.session, Clients, email = 'Jeffre@hotmail.com', password = 'encrypted')
	get_or_create(db.session, SupportWorkers, email = 'RolfHarris@example.com')
	get_or_create(db.session, SupportWorkers, email = 'Nathan@example.com')


	#u = SupportWorkers(email='David@example.com')
	#db.session.add(u)
	#z = SupportWorkers(email='Rob@example.com')
	#db.session.add(z)

	#db.session.commit()
	
	#print('Great Success')


