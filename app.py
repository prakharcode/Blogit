from flask import Flask, g
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager




app = Flask(__name__)
app.config.from_object(Configuration) #use value from Configuration Object
db = SQLAlchemy(app)
migrte = Migrate(app,db)

manager= Manager(app)
manager.add_command('db',MigrateCommand)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.before_request
def _before_request():
    g.user = current_user
