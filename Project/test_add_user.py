# project/test.py

import unittest
import os,sys,inspect
from project import create_app, db
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db, bcrypt
from project.models import User, Post
from project.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from project.users.utils import (save_picture, send_reset_email,
                                generate_confirmation_token, confirm_token,
                                send_email, check_confirmed)

app = create_app()
app.app_context().push()

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.assertEqual(app.debug, True)
        # Disable sending emails during unit testing

    # executed after each test
    def tearDown(self):
        pass

    def test_register_user(self):
        db.drop_all()
        db.create_all()
        user = User(username = 'Testt',
                    email='test@ttest.com',
                    password = bcrypt.generate_password_hash("test").decode('utf-8'),
                    firstName='test',
                    middleName='test',
                    lastName='test',
                    address='test',
                    phone='0000000000',
                    doctor='test',
                    drLicenseNum='test',
                    dateOfBirth='test',
                    gender='test',
                    ssn='000000000',
                    race='test',
                    emergencyName='test',
                    emergencyRelation='test',
                    emergencyAddress='test',
                    emergencyPhone='test',
                    majorSurgery='test',
                    smoking='test',
                    confirmed=False)
        db.session.add(user)
        db.session.commit()
        result = User.query.first()
        self.assertEqual(user, result)



if __name__ == "__main__":
    unittest.main()
