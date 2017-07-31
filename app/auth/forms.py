from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Regexp, Length, Email
from ..models import User


class RegistForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    username = StringField("What's your name?", validators=[DataRequired(), Length(5, 12), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(6, 16),
                    EqualTo('confirm_pw', message='Passwords must match.')]
    )
    confirm_pw = PasswordField('Confirm password',
                               validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class Change_Password_Form(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField(
        "Password.",
        validators=[DataRequired(),
                    EqualTo('confirm_pw', message='Passwords must match.')]
    )
    confirm_pw = PasswordField('Confirm password.',
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailRequestForm(FlaskForm):
    new_email = StringField('New Email', validators=[
                            DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Change Email')
