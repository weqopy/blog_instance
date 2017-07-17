from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class RegistForm(FlaskForm):
    """docstring for RegistForm"""
    username = StringField("What's your name?", validators=[DataRequired()])
    password = PasswordField(
        "Password.",
        validators=[DataRequired(),
                    EqualTo('confirm_pw', message='Passwords must match.')]
    )
    confirm_pw = PasswordField('Confirm password.',
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    """docstring for LoginForm"""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')
