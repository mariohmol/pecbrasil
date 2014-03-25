from wtforms import TextField, TextAreaField, HiddenField
from wtforms.validators import Required, Length
from flask_wtf import Form


class SearchForm(Form):
    search = TextField('search', validators = [Required()])

class AskForm(Form):
    question = TextField('question', validators = [Required()])
    body = TextAreaField('body', validators = [])
    app = TextField('app', validators = [])
    email = TextField('email', validators = [])
    tags = TextField('tags', validators = [])
    def validate(self):
        return True

class ReplyForm(Form):
    reply = TextAreaField('reply', validators = [Required()])
    parent = HiddenField('parent')
