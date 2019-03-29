# project/test.py

import unittest
import sys

from project import create_app

app = create_app()
TEST_DB: str = "test.db"


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

    '''def test_correct_login(self):
        with self.app:
            response = self.app.post(
                '/login',
                data=dict(user='admin', password='admin'),
                follow_redirects=True
            )
            #self.assertIn(b'You were logged in', response.data)
            self.assertTrue(user == 'admin')
            self.assertTrue(user.is_active())'''


if __name__ == "__main__":
    unittest.main()
