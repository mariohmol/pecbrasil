from wtforms import Form, PasswordField

class AccessForm(Form):
    pw = PasswordField('pw')
