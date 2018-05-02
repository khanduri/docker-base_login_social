from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class ProfileForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[Email("Please enter your email address.")])
    timezone = StringField("timezone")
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])


class ContactForm(Form):
    name = StringField("Name")
    email = StringField("Email", [Email("Please enter your email address.")])
    message = TextAreaField("Message", [DataRequired("Please enter a message.")])
