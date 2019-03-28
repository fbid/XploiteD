from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from sqlalchemy import func
from flask_login import current_user
from app.models.user import User

class RegistrationForm(FlaskForm):
    uname_v = [DataRequired(), Length(min=6,max=20)]
    username = StringField('Username', validators=uname_v)

    email_v = [DataRequired(), Email()]
    email = StringField('Email', validators=email_v)

    psw_v = [DataRequired()]
    password = PasswordField('Password', validators=psw_v)
    c_psw_v = [DataRequired(), EqualTo('password')]
    password_confirmation = PasswordField('Confirm Password', validators=c_psw_v)

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        '''Checks if another user with the same username already exists (case insensitive)'''
        user = User.query.filter(func.lower(User.username)==username.data.lower()).first()
        if user:
            raise ValidationError(f'Username {username.data} is already taken. Please use another one')

    def validate_email(self, email):
        '''Checks if another user with the same email address already exists'''
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError(f'Email {email.data} is already in use.')

class LoginForm(FlaskForm):
    email_v = [DataRequired(), Email()]
    email = StringField('Email', validators=email_v)

    psw_v = [DataRequired()]
    password = PasswordField('Password', validators=psw_v)

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateUserInfoForm(FlaskForm):
    uname_v = [DataRequired(), Length(min=6,max=20)]
    username = StringField('New Username', validators=uname_v)

    email_v = [Optional(), Email()]
    email = StringField('New Email', validators=email_v)

    pic_v = [FileAllowed(['jpg', 'png'])]
    picture = FileField('Picture', validators=pic_v)

    # Submit form
    submit = SubmitField('Update')

    def validate_username(self, username):
        if not username.data == current_user.username:
            '''Checks if another user with the same username already exists (case insensitive)'''
            user = User.query.filter(func.lower(User.username)==username.data.lower()).first()
            if user:
                raise ValidationError(f'Username {username.data} is already taken. Please use another one')

    def validate_email(self, email):
        if not email.data == current_user.email:
            '''Checks if another user with the same email address already exists'''
            user = User.query.filter_by(email=email.data.lower()).first()
            if user:
                raise ValidationError(f'Email {email.data} is already in use.')

class RequestPasswordResetForm(FlaskForm):
    email_v = [DataRequired(), Email()]
    email = StringField('Email', validators=email_v)

    submit = SubmitField('Send request')

class PasswordResetForm(FlaskForm):
    psw_v = [DataRequired()]
    password = PasswordField('Password', validators=psw_v)
    c_psw_v = [DataRequired(), EqualTo('password')]
    password_confirmation = PasswordField('Confirm Password', validators=c_psw_v)

    submit = SubmitField('Reset password')
