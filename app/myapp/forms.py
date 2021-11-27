from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


from myapp.models import User


class SignupForm(FlaskForm):
    email = StringField('EMAIL', validators = [DataRequired(), Email(message = 'invalid email')])
    username = StringField('USERNAME', validators = [DataRequired()])
    password = PasswordField('PASSWORD', validators = [DataRequired(), EqualTo('password2', message = 'Passwords must match')])
    password2 = PasswordField("CONFIRM PASSWORD", validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

class LoginForm(FlaskForm):
    username = StringField('USERNAME', validators=[DataRequired()])
    password = PasswordField('PASSWORD')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class FlashCardForm(FlaskForm):
    front = TextAreaField('Front', validators=[DataRequired()])
    back = TextAreaField('Back', validators=[DataRequired()])
    add = SubmitField('Add')

class NextButton(FlaskForm):
    nextCard = SubmitField('Next')


class UploadMarkdownForm(FlaskForm):
    file = FileField('Select markdown file:', validators=[FileRequired(), FileAllowed(['md'])])
    upload = SubmitField('Upload')


class SearchForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    button = SubmitField('Search')
    
class renderMarkdown(FlaskForm):
    pagedown = PageDownField('Enter markdown text')
    submit = SubmitField('Download as pdf')

