import os

class Config:
    SECRET_KEY = '1234'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'noreply.mednet@gmail.com'
    MAIL_PASSWORD = 'Password1@'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
