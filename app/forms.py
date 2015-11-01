from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, TextField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])


class ContactForm(Form):
    name = StringField("Name")
    email = StringField("Email",  [Email("Please enter your email address.")])
    message = TextAreaField("Message",  [DataRequired("Please enter a message.")])
