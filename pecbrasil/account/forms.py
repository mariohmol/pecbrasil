from wtforms import  TextField, TextAreaField, BooleanField, HiddenField,PasswordField #QuerySelectField
from flask.ext.wtf import Form
from wtforms.validators import Required,Length,url
from flask.ext.wtf.html5 import URLField
#flask.ext.wtf import
from pecbrasil.ask.models import Status
#from twisted.python.formmethod import Password

class LoginForm(Form):
    provider = HiddenField('provider', validators = [Required()])
    password = PasswordField('password')
    email = TextField('email')
    remember_me = BooleanField('remember_me', default = False)

class UserEditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    bio = TextAreaField('bio', validators = [Length(min=0, max=256)])
    website = URLField(validators=[url()])

class UserCreateForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    password = PasswordField('password')
    fullname = TextField('fullname')
    email = TextField('email', validators = [Required()])
  #  bio = TextAreaField('bio', validators = [Length(min=0, max=256)])
  #  website = URLField(validators=[url()])