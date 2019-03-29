from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from project.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    firstName = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    middleName = StringField('Middle Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address',
                            validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone',
                            validators=[DataRequired(), Length(min=2, max=10)])
    dateOfBirth = StringField('Date of Birth',
                            validators=[DataRequired(), Length(min=2, max=20)])
    gender = StringField('Gender',
                            validators=[DataRequired(), Length(min=2, max=20)])
    ssn = StringField('Social Security Number',
                            validators=[DataRequired(), Length(min=9, max=9)])
    race = StringField('Race',
                            validators=[DataRequired(), Length(min=2, max=20)])
    emergency = StringField('Emergency Contact Info(Name, Relation, Phone, Address)',
                            validators=[DataRequired(), Length(min=2, max=120)])
    majorSurgery = StringField('Major Surgeries(Seperate with commans)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    smoking = StringField('Smoking (Yes/No)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please try again.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please try again.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    firstName = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    middleName = StringField('Middle Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address',
                            validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone',
                            validators=[DataRequired(), Length(min=2, max=10)])
    dateOfBirth = StringField('Date of Birth',
                            validators=[DataRequired(), Length(min=2, max=20)])
    gender = StringField('Gender',
                            validators=[DataRequired(), Length(min=2, max=20)])
    ssn = StringField('Social Security Number',
                            validators=[DataRequired(), Length(min=9, max=9)])
    race = StringField('Race',
                            validators=[DataRequired(), Length(min=2, max=20)])
    emergency = StringField('Emergency Contact Info(Name, Relation, Phone, Address)',
                            validators=[DataRequired(), Length(min=2, max=120)])
    majorSurgery = StringField('Major Surgeries(Seperate with commans)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    smoking = StringField('Smoking (Yes/No)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please try again.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please try again.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
