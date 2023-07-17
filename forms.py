from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FloatField
from wtforms.validators import DataRequired, URL

##WTForm

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField('Sign Up!')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class TrackForm(FlaskForm):
    url = StringField("URL",validators=[DataRequired(), URL()])
    budget = FloatField("Budget",validators=[DataRequired()])
    submit = SubmitField("Track Price")


class Subscribeform(FlaskForm):
    submit = SubmitField("Subscribe")
