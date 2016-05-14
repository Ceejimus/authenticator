import unittest
from app import app, db
import app.domain as domain
import app.api as api

from flask.ext.testing import TestCase

import os
import random

class UserTests(TestCase):
    def create_app(self):
        app.config.from_pyfile('testconfig.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove();
        db.drop_all()

    ### Make sure you can save and retreive a user from the database ###
    def test_can_get_user_from_email(self):
        password = "password"
        salt = os.urandom(50)
        pass_hash = api.hash_password(api.string_to_bytes(password), salt)
        newUser = domain.User("test@test.com", pass_hash, salt)
        db.session.add(newUser)
        db.session.commit()
        user_data = api.get_user_from_email("test@test.com")
        self.assertEqual(user_data["email"], "test@test.com")
        self.assertEqual(user_data["password"], pass_hash)
        self.assertEqual(user_data["salt"], salt)
        self.assertEqual(user_data["authenticated"], False)

    ### make sure the hash works consistently ###
    def test_hash_works_generally(self):
        lower_chars = "abcdefghijklmnopqrstuvwxyz"
        upper_chars = "ABCDEFGHIJKLMNOPQRSTUWXYZ"
        digits = "0123456789"
        things = "!@#$%^&*()_-+=~`;:\'\"\\.>,</?"

        for i in range(5):
            password = ''.join(random.choice(lower_chars + upper_chars + digits + things) for _ in range(128))
            password = api.string_to_bytes(password)
            salt = os.urandom(128)
            hash_result1 = api.hash_password(password, salt)
            hash_result2 = api.hash_password(password, salt)
            hash_result3 = api.hash_password(password, salt)

            self.assertEqual(hash_result1, hash_result2)
            self.assertEqual(hash_result1, hash_result3)
            self.assertEqual(hash_result2, hash_result3)

    ### make sure user objects are created correctly ###
    def test_can_create_user_from_user_data(self):
        email = "test@test.com"
        password = "password"
        user_data = {
            'email': email,
            'password': password
        }
        salt = os.urandom(256)
        hashed_password = api.hash_password(api.string_to_bytes(password), salt)
        user = api.create_user_from_user_data(user_data, salt)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, hashed_password)
        self.assertEqual(user.salt, salt)
        self.assertEqual(user.authenticated, False)

    def test_can_create_user_from_user_date_returns_none(self):
        user_data_no_email = {
            'password': "password"
        }

        user_data_no_password = {
            'email': "test@test.com",
        }

        user_data_no_nuthin = {}

        salt = os.urandom(10) # what the heck

        self.assertEqual(None, api.create_user_from_user_data(user_data_no_email, salt))
        self.assertEqual(None, api.create_user_from_user_data(user_data_no_password, salt))
        self.assertEqual(None, api.create_user_from_user_data(user_data_no_nuthin, salt))

        user_data_no_email = {
            'email': None,
            'password': "password"
        }

        user_data_no_password = {
            'email': "test@test.com",
            'password': None
        }

        user_data_no_nuthin = {
            'email': None,
            'password': None
        }

        self.assertEqual(None, api.create_user_from_user_data(user_data_no_email, salt))
        self.assertEqual(None, api.create_user_from_user_data(user_data_no_password, salt))
        self.assertEqual(None, api.create_user_from_user_data(user_data_no_nuthin, salt))

test_cases = [UserTests]

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        print(tests)
        suite.addTests(tests)
    return suite