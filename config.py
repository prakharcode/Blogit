import os
class Configuration(object):    #instructs flask to run in debug
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__)) #getting current directory location
    DEBUG = False
    SECRET_KEY = 'flask is fun!'
    DATABASE_URL='postgres://rzxstcytozlazj:phsZ1z__CsU8-x8gjkeA_a1g7t@ec2-54-243-48-178.compute-1.amazonaws.com:5432/dfg7fns2de7j0v'
    SQLALCHEMY_DATABASE_URI = os.environ[DATABASE_URL]   #using the database in current directory
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    STATIC_DIR = os.path.join(APPLICATION_DIR,'static')
    IMAGES_DIR  = os.path.join(STATIC_DIR,'images')
