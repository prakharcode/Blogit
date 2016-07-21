import os
class Configuration(object):    #instructs flask to run in debug
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__)) #getting current directory location
    DEBUG = False
    SECRET_KEY = 'flask is fun!'
    SQLALCHEMY_DATABASE_URI = os.environ[DATABASE_URL]   #using the database in current directory
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    STATIC_DIR = os.path.join(APPLICATION_DIR,'static')
    IMAGES_DIR  = os.path.join(STATIC_DIR,'images')
