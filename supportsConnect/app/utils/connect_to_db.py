#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Function to connect to supportsconnect_database

from psycopg2 import connect, Error

def connect_to_supportsconnect_database():

	print ('Connecting to supportsconnect_database')
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