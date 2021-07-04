This directory is responsible for:
- Spinning up the Flask server on localhost
- Running html / css in the client's web browser

## SET UP VIRTUAL ENV ##

1. navigate to the COMP9323-Group-Project/supportsConnect directory
2. Create virtual environment called 'supportsConnect_env': 

	$ python3 -m venv supportsConnect_env

3. Activate the python virtual environment from this directory: 
	
	$ source supportsConnect_env/bin/activate 

4. Install dependencies for the virtual environment:
	
	$ pip install -r requirements.txt

	NOTE if you are on mac and it can't download psycopg2, do this
	```
	pip install psycopg2-binary
	```

5. Add git ignore, so the virtual environment dependencies aren't tracked by git:

	$ echo 'supportsConnect_env' > .gitignore

## Connect to the database ##

1. Download Docker (if there's an option to download docker-compose, say yes)
2. Navigate to the COMPP9323-Group-Project/Database directory
3. Execute the following command:
	
	$ docker-compose up --build 

	It will print a bunch of stuff out, but the last line should say "LOG:  database system is ready to accept connections". Also, leave off the --build tag the next times you run it.

4. You should be good to go. The postgres database is listening on port 6666 of your local machine.
5. To stop Docker, do Ctrl+C and then do:
	
	$ docker-compose down


# RUN THE WEBSITE #

1. Assuming you have set up the virtual environment and have docker working, do:

	$ python3 network.py

	You should then be able to view the website in your browser

## DEACTIVATE VIRTUAL ENV ##

	$ deactivate supportsConnect_env
