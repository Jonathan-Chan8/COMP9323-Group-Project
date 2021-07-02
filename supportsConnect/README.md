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


# RUN THE WEBSITE #

1. Assuming you have set up the virtual environment

	$ python3 network.py


## DEACTIVATE VIRTUAL ENV ##

	$ deactivate supportsConnect_env
