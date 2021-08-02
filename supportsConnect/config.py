import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost:6666/supportsconnect_database'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ## POSTGRES ##

    # Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"



    ## SQLITE ##

    #    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    #    SQLALCHEMY_TRACK_MODIFICATIONS = False