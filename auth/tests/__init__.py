import unittest
from app import app, db
import app.domain as domain
import app.api as api

from flask.ext.testing import TestCase

class UserTests(TestCase):
    def create_app(self):
        app.config.from_pyfile('testconfig.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove();
        db.drop_all()

    def test_can_get_user_from_email(self):
        newUser = domain.User("test@test.com", "passhash", "salt")
        db.session.add(newUser)
        db.session.commit()
        user_data = api.get_user_from_email("test@test.com")
        self.assertEqual(user_data["email"], "test@test.com")
        self.assertEqual(user_data["authenticated"], False)

    def test_passed_test2(self):
        self.assertEqual(2, 5)

    def test_failed_test(self):
        self.assertEqual(2, 8)

    def test_failed_test2(self):
        self.assertEqual(2, 4)

test_cases = [UserTests]

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite