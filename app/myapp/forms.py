from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo
from wtforms import ValidationError
from myapp.models import User


class SignupForm(FlaskForm):
    email = StringField('EMAIL', validators = [DataRequired(), Email(message = 'invalid email')])
    username = StringField('USERNAME', validators = [DataRequired()])
    password = PasswordField('PASSWORD', validators = [DataRequired(), EqualTo('password2', message = 'Passwords must match')])
    password2 = PasswordField("CONFIRM PASSWORD", validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use')

class LoginForm(FlaskForm):
    username = StringField('USERNAME', validators = [DataRequired()])
    password = PasswordField('PASSWORD')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    
class NoteForm(FlaskForm):
    '''WTForm for upload markdown file to notes page and later converting to pdf

    Attributes:
        name: note name
        note: note file
        submit: Submit field to add card
    '''
    name = StringField('name', validators={DataRequired()})
    note = FileField('file', validators={DataRequired()})
    submit = SubmitField('submit')
