from flask.ext.wtf import Form
from wtforms import HiddenField,TextField,TextAreaField, validators
from wtforms.validators import Required

class AvaliarForm(Form):
    desc = TextAreaField('desc',  [validators.Length(min=0, max=25)])
    voto = TextField('voto', validators = [Required()])
    necessidade = TextField('necessidade')
    
    

    