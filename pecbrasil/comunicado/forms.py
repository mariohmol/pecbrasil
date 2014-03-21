from wtforms import  TextField, TextAreaField, BooleanField, HiddenField,PasswordField #QuerySelectField
from flask.ext.wtf import Form
from wtforms.validators import Required,Length,url
from flask.ext.wtf.html5 import URLField
#flask.ext.wtf import
from pecbrasil.ask.models import Status
#from twisted.python.formmethod import Password

class ConvidarForm(Form):
    obs = TextAreaField('bio', validators = [Length(min=0, max=256)])
    email = TextField('email', validators = [Required()])