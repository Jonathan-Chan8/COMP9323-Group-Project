from .database import *

##-------------------------------------------------------------------------------------------------##
# 										Profile Queries 											#

# Check if the user email exists in the database

def user_already_exists(email):

	query = """SELECT EXISTS(SELECT 1 FROM Users 
				WHERE email = '{0}');""".format(email)
	
	result = execute_read_query(query)
	return result

# Add user account details to the database

def add_user_to_database(first_name, last_name, email, password, account_type):

	query = """INSERT INTO Users(firstname, lastname, email, password, accounttype) 
				VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');""".format(first_name, 
														last_name, email, password, account_type)
	
	result = execute_update_query(query)
	return result


##-------------------------------------------------------------------------------------------------##
# 										Schedule Queries 											#




##-------------------------------------------------------------------------------------------------##
# 										Report Queries 												#