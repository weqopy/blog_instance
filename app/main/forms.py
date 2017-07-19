from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    """docstring for NameForm"""
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
