#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Function to connect to supportsconnect_database

from psycopg2 import connect, Error

def connect_to_database():

	print ('Connecting to database')
	try:
	    # declare a new PostgreSQL connection object
	    conn = connect(
	        dbname = "supportsconnect_database",
	        user = "postgres",
	        host = "localhost",
	        password = "password",
	        port = '6666'
	        #connect_timeout = connection_time 	# attempt to connect for 'x' seconds then raise exception

	    )
	    print("Connection success")
	    cur = conn.cursor()
	    
	except (Exception, Error) as err:
	    print ("Failed to connect to the database \npsycopg2 connect error:", err)
	    conn = None
	    cur = None

	return conn, cur

#----------------------------------------------------------------------------#

# CRUD (CREATE, READ, UPDATE, DELETE) Operations

def execute_update_query(query, conn, cur):

	result = False
	if cur != None:
		try:
			cur.execute(query)
			print("SUCCESSFULLY ADDED")

		except (Exception, Error) as error:
			print("\nexecute_sql() error:", error)
			conn.rollback()
	else:
		result = False

	conn.commit()
	cur.close()
	conn.close()

	return result

def execute_read_query(query, conn, cur):

	if cur != None:
		try:
			cur.execute(query)
			result = cur.fetchone()[0]
		except (Exception, Error) as error:
			print("\nexecute_sql() error:", error)
			conn.rollback()
	else:
		result = False
	cur.close()
	conn.close()

	return result


