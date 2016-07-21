from models import User,db
from app import bcrypt

ps=bcrypt.generate_password_hash('admin')
user=User(email='admin@gmail.com',password_hash=ps, name='Admin',admin = True)
db.session.add(user)
db.session.commit()
