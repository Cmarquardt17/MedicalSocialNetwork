# project/test.py

import unittest
import os,sys,inspect
from project import run

app = create_app()


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        # Disable sending emails during unit testing

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

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


if __name__ == "__main__":
    unittest.main()
