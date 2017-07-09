from flask_wtf import FlaskForm  # Form 已弃用
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class NameForm(FlaskForm):
    """docstring for NameForm"""
    name = StringField("What's your name?", validators=[DataRequired()])
    password = PasswordField('Set your password.',
                             validators=[DataRequired(),
                                         EqualTo('confirm_password',
                                                 message='Passwords must match.')])
    confirm_password = PasswordField(
        'Confirm the password', validators=[DataRequired()])
    submit = SubmitField('Submit')
