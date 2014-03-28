from flask.ext.wtf import Form
from wtforms import HiddenField,TextField,TextAreaField
from wtforms.validators import Required

class LigaForm(Form):
    nome = TextField('nome', validators = [Required()])
    desc = TextAreaField('desc')
    publico = TextField('publico')
    