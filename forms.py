from app import app, g
import wtforms
from wtforms import validators
from models import User
from wtforms import HiddenField



class LoginForm(wtforms.Form):
    email = wtforms.StringField('E-mail',validators = [validators.DataRequired()])
    password = wtforms.PasswordField('Password',validators = [validators.DataRequired()])
    remember_me = wtforms.BooleanField('Remember Me',default = True)

    def validate(self):
        if not super(LoginForm,self).validate():
            return False

        self.user = User.authenticate(self.email.data, self.password.data)

        if not self.user:
            self.email.errors.append('Invalid email or password')
            return False

        return True
class SignUpForm(wtforms.Form):
    name = wtforms.StringField('Name', validators = [validators.DataRequired()])
    email = wtforms.StringField('E-mail', validators = [validators.DataRequired()])
    password_hash = wtforms.PasswordField('Password', validators = [validators.DataRequired()])
    confirmpass = wtforms.PasswordField('Confirm Password', validators = [validators.DataRequired(),validators.EqualTo('password_hash','Not same as Password')])
    def save_entry(self):
        return User.create(email = self.email.data, password = self.password_hash.data,name = self.name.data)
