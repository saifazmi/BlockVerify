from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Custom validators
    def validate_username(self, username):
        """Raise a VlidationError if the username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Raise a VlidationError if the email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddFileForm(FlaskForm):
    file = FileField('Select a file', validators=[DataRequired()])
    submit = SubmitField('Process File')


class VerifyFileForm(FlaskForm):
    file = FileField('Select a file', validators=[DataRequired()])
    submit = SubmitField('Verify File')
