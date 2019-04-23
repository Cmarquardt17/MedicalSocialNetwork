# project/test.py

import unittest
import os,sys,inspect
from project import create_app
#from project import Blueprint

app = create_app()
#errors = Blueprint('errors', __name__)

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        #self.assertEqual(app.debug, False)
        # Disable sending emails during unit testing

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_Handler(self):
        response = self.app.get('/something')
        response2 = self.app.get('/post/1/update')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response2.status_code, 302)

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertIn(b'Log In', response.data)

    def test_incorrect_login(self):
        response = self.app.post(
            '/login',
            data=dict(user="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Log In', response.data)

    def test_create_user(self):

        u = User(nickname = 'john', email = 'john@example.com', account_type = "tester")
        response = self.app.get('/logout')
        self.assertIn(b'/home', response.data)

if __name__ == "__main__":
    unittest.main()
