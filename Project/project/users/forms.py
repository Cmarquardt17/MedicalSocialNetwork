from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from project.models import User

#This method is the layout for the registration page that the potential new user will have to fill out
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
    doctor = StringField('Are You a Clinician? ("yes"/"no")',
                            validators=[DataRequired(), Length(min=2, max=10)])
    drLicenseNum = StringField('Doctor License Number ("N/A" if you are not a Doctor")',
                            validators=[DataRequired(), Length(min=2, max=10)])
    dateOfBirth = StringField('Date of Birth',
                            validators=[DataRequired(), Length(min=2, max=20)])
    gender = StringField('Gender',
                            validators=[DataRequired(), Length(min=2, max=20)])
    ssn = StringField('Social Security Number',
                            validators=[DataRequired(), Length(min=9, max=9)])
    race = StringField('Race',
                            validators=[DataRequired(), Length(min=2, max=20)])
    emergencyName = StringField('Emergency Contact Name',
                            validators=[DataRequired(), Length(min=2, max=120)])
    emergencyRelation = StringField('Emergency Contact Relation',
                            validators=[DataRequired(), Length(min=2, max=120)])
    emergencyAddress = StringField('Emergency Contact Address',
                            validators=[DataRequired(), Length(min=2, max=120)])
    emergencyPhone = StringField('Emergency Contact Phone',
                            validators=[DataRequired(), Length(min=2, max=120)])
    majorSurgery = StringField('Major Surgeries(Seperate with commas)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    smoking = StringField('Smoking (Yes/No)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password (Must be more than 2 characters)', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #To make sure that the username is valid with all of the qualifications
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please try again.')

    #A double enter/check that the email they first entered in is correct
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please try again.')

#The login layout for a user to login to
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#The layout for the user to update their information if they are on the account page 
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
    doctor = StringField('Are You a Clinician?("yes"/"no")',
                            validators=[DataRequired(), Length(min=2, max=10)])
    drLicenseNum = StringField('Doctor License Number ("N/A" if you are not a Doctor")',
                            validators=[DataRequired(), Length(min=2, max=10)])
    dateOfBirth = StringField('Date of Birth',
                            validators=[DataRequired(), Length(min=2, max=20)])
    gender = StringField('Gender',
                            validators=[DataRequired(), Length(min=2, max=20)])
    ssn = StringField('Social Security Number',
                            validators=[DataRequired(), Length(min=9, max=9)])
    race = StringField('Race',
                            validators=[DataRequired(), Length(min=2, max=20)])
    emergencyName = StringField('Emergency Contact Name)',
                            validators=[DataRequired(), Length(min=2, max=120)])
    emergencyRelation = StringField('Emergency Contact Relation)',
                            validators=[DataRequired(), Length(min=2, max=120)])
    emergencyAddress = StringField('Emergency Contact Address)',
                            validators=[DataRequired(), Length(min=2, max=120)])
    emergencyPhone = StringField('Emergency Contact Phone)',
                            validators=[DataRequired(), Length(min=2, max=120)])
    majorSurgery = StringField('Major Surgeries(Seperate with commans)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    smoking = StringField('Smoking (Yes/No)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

    #A check to see if the user hasn't already been created by a previous user
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please try again.')

    #To make sure the email hasn't already been used by a previous user
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists. Please try again.')

#Form for the request to set a password, the one below is the actually changing of the password
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    #Must make sure the email goes with the password and if not will be asked to reigster with the website
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register.')

#Form for the resetting your password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
