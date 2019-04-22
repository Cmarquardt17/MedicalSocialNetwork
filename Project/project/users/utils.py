import os
import secrets
from PIL import Image
from flask import url_for, current_app, flash, render_template, redirect, request, Blueprint
from flask_login import current_user
from flask_mail import Message
from project import mail
from functools import wraps
from itsdangerous import URLSafeTimedSerializer

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    #change email
    msg = Message('Password Reset Request',
                    sender='noreply.mednet@gmail.com',
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then ignore this email.
'''
    mail.send(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='noreply.mednet@gmail.com'
    )
    mail.send(msg)

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('We have still not verified your account, please try again later', 'warning')
            return redirect(url_for('users.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

def confirm_token(token, expiration=10000):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
