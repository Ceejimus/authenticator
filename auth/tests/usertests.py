import os
import random

from app import app, db

import app.api as api

import app.domain as domain

from flask.ext.testing import TestCase


class UserTests(TestCase):

    def create_app(self):
        app.config.from_pyfile('testconfig.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Make sure you can save and retreive a user from the database #

    def test_can_get_user_data_from_email(self):
        password = "password"
        salt = os.urandom(50)
        pass_hash = api.hash_password(api.string_to_bytes(password), salt)
        new_user = domain.User("test@test.com", pass_hash, salt)
        db.session.add(new_user)
        db.session.commit()
        user_data = api.get_user_data_from_email("test@test.com")
        self.assertEqual(user_data["email"], "test@test.com")
        self.assertEqual(user_data["password"], pass_hash)
        self.assertEqual(user_data["salt"], salt)
        self.assertEqual(user_data["authenticated"], False)

    def test_can_authenticate_user_against_supplied_password(self):
        password = api.string_to_bytes('password')
        salt = os.urandom(256)
        user_data = {
            'password': api.hash_password(password, salt),
            'salt': salt
        }

        right = api.authenticate_user_password(user_data, password)
        self.assertTrue(right)

        wrong = api.authenticate_user_password(
            user_data,
            api.string_to_bytes("wrong password"))
        self.assertFalse(wrong)

    # make sure the hash works consistently
    def test_hash_generally_works(self):
        lower_chars = "abcdefghijklmnopqrstuvwxyz"
        upper_chars = "ABCDEFGHIJKLMNOPQRSTUWXYZ"
        digits = "0123456789"
        things = "!@#$%^&*()_-+=~`;:\'\"\\.>,</?"
        chars = lower_chars + upper_chars + digits + things

        for i in range(5):
            password = ''.join(random.choice(chars) for _ in range(128))
            password = api.string_to_bytes(password)
            salt = os.urandom(128)
            hash_result1 = api.hash_password(password, salt)
            hash_result2 = api.hash_password(password, salt)
            hash_result3 = api.hash_password(password, salt)

            self.assertEqual(hash_result1, hash_result2)
            self.assertEqual(hash_result1, hash_result3)
            self.assertEqual(hash_result2, hash_result3)

    # make sure user objects are created correctly
    def test_can_create_user_from_user_data(self):
        email = "test@test.com"
        password = "password"
        user_data = {
            'email': email,
            'password': password
        }
        salt = os.urandom(256)
        hashed_password = api.hash_password(
            api.string_to_bytes(password), salt)
        user = api.create_user_from_user_data(user_data, salt)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, hashed_password)
        self.assertEqual(user.salt, salt)
        self.assertEqual(user.authenticated, False)
