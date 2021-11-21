from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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

class FlashCardForm(FlaskForm):
    front = TextAreaField('Front', validators = [DataRequired()])
    back = TextAreaField('Back', validators = [DataRequired()])
    add = SubmitField('Add')

class NextButton(FlaskForm):
    nextCard = SubmitField('Next')