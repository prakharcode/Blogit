import os
class Configuration(object):    #instructs flask to run in production mode
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__)) #getting current directory location
    DEBUG = False
    SECRET_KEY = 'flask is fun!'
    db= ""  #-------unique URL provided by heroku for database
    SQLALCHEMY_DATABASE_URI = db   #using the database in current directory
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    STATIC_DIR = os.path.join(APPLICATION_DIR,'static')
    IMAGES_DIR  = os.path.join(STATIC_DIR,'images')
