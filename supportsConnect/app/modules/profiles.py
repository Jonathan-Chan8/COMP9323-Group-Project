
# The following are functions related to user profiles

from .database import *


#----------------------------------------------------------------------------#
# Check if the user email exists in the database

def user_already_exists(email):
	conn, cur = connect_to_database() 
	query = """SELECT EXISTS(SELECT 1 FROM Users 
				WHERE email = '{0}');""".format(email)
	
	result = execute_read_query(query, conn, cur)
	return result
#----------------------------------------------------------------------------#
# Check if the user account details to the database

def add_user_to_database(email,first_name, last_name):

	conn, cur = connect_to_database() 
	query = """INSERT INTO Users(email, givenName, familyName) 
				VALUES ('{0}', '{1}', '{2}');""".format(email, first_name, last_name)
	
	result = execute_update_query(query, conn, cur)
	return result
#----------------------------------------------------------------------------#



