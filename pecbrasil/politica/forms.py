from flask.ext.wtf import Form
from wtforms import HiddenField,TextField,TextAreaField
from wtforms.validators import Required

class PoliticoForm(Form):
    output_format = HiddenField('output_format', id="output_format")
    data = HiddenField('data', id="data")
    title = HiddenField('title', id="title")
    nome = TextField('nome')

class TimeForm(Form):
    nome = TextField('nome', validators = [Required()])
    desc = TextAreaField('desc')
    color = TextField('color')
    