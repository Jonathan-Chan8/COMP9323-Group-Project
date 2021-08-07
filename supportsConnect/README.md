# Instructions to get the website up and running (on localhost)#


## Create the Database ##

1. Download Docker (if there's an option to download docker-compose, say yes)
2. Navigate to the COMPP9323-Group-Project/Database directory
3. Execute the following command:
    
    $ docker-compose up --build 

    It will print a bunch of stuff out, but the last line should say "LOG:  database system is ready to accept connections". Also, leave off the --build tag the next times you run it.

4. You should be good to go. The postgres database is listening on port 6666 of your local machine. Just leave it running in that terminal
5. To stop Docker, do Ctrl+C and then do:
    
    $ docker-compose down

## Setup a Python Virtual Environment ##


1. Open up a new terminal and navigate to the COMP9323-Group-Project/supportsConnect directory
2. Create virtual environment called 'supportsConnect_env': 

    $ python3 -m venv supportsConnect_env

3. Activate the python virtual environment from this directory: 
    
    $ source supportsConnect_env/bin/activate      (deactivating it is just: $ deactivate supportsConnect_env)

4. Install dependencies for the virtual environment:
    
    $ pip install -r requirements.txt

    NOTE if you are on mac and it can't download psycopg2, do this
    ```
    pip install psycopg2-binary
    ```

5. Add git ignore, so the virtual environment dependencies aren't tracked by git:

    $ echo 'supportsConnect_env' > .gitignore


## Add the SQL_Alchemy ORM schema to our postgresql database ""

With the virtual environment now setup and whilst in the COMP9323-Group-Project/supportsConnect directory:

1. Create a directory called 'migrations' 

	$ flask db init      

2. Add the ORM schema in models.py to the migrations

	$ flask db migrate   

3. Commit the migrations to database

	$ flask db upgrade   


# RUN THE WEBSITE #

Assumes: Docker is running, the virtual environment has been created and the database schema has been added

1. From the same terminal that you ran $ flask db upgrade (i.e. in the COMP9323-Group-Project/supportsConnect directory and the virtual environment on)

. Run the website

    $ flask run

    You should then be able to view the website at localhost in your browser


## Add test data to the database ##

Whilst in the COMP9323-Group-Project/supportsConnect directory, run:

    $ python add_test_data.py
    
    If successful, it should say "- instance added" a bunch of times. 
    -- The user test data (login/password) details are in the add_test_data.py file - 

## Making changes to the database in models.py ##

Once the changes have been made, run:
    
    $ flask db migrate 
    $ flask db upgrade 

    The database should now be updated. 

However, if it threw errors in this process:
    
1. Tear down the docker container

    $ ctrl-C
    $ docker-compose down 

2. Then create it again

    $ docker-compose up

3. Then go delete the folder called 'migrations' in COMP9323-Group-Project/supportsConnect
4. Then add the SQL_Alchemy ORM schema to our database again

    $ flask db init
    $ flask db migrate 
    $ flask db upgrade





