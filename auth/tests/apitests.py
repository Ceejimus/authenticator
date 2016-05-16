import os

from app import app, db

import app.api as api

import app.domain as domain

from flask import json

from flask.ext.testing import TestCase


class ApiTests(TestCase):

    def create_app(self):
        app.config.from_pyfile('testconfig.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_can_create_user(self):
        user_data = {
            'email': 'test@test.com',
            'password': 'mytestpass'
        }
        with self.app.test_client() as client:
            result = client.post(
                '/user/create',
                data=json.dumps(user_data),
                headers={'content-type': 'application/json'})
            self.assert200(result)
            data = json.loads(result.data)
            self.assertEqual(user_data['email'], data['email'])
            self.assertEqual(False, data['authenticated'])

        user_from_db = api.get_user_data_from_email(user_data['email'])
        self.assertEqual(user_from_db["email"], user_data['email'])
        self.assertEqual(user_from_db["authenticated"], False)

    def test_can_get_user(self):
        user_data = {
            'email': 'test@test.com',
            'password': 'mytestpass'
        }

        new_user = api.create_user_from_user_data(user_data, os.urandom(256))

        db.session.add(new_user)
        db.session.commit()

        with self.app.test_client() as client:
            result = client.get('/user?email=' + user_data['email'])
            self.assert200(result)
            data = json.loads(result.data)
            self.assertEqual(user_data['email'], data['email'])
            self.assertEqual(False, data['authenticated'])

    def test_can_authenticate_user(self):
        user_data = {
            'email': 'test@test.com',
            'password': 'password'
        }

        salt = os.urandom(50)
        pass_hash = api.hash_password(
            api.string_to_bytes(user_data['password']), salt)
        new_user = domain.User(user_data['email'], pass_hash, salt)
        db.session.add(new_user)
        db.session.commit()

        with self.app.test_client() as client:
            # right password gives true
            result = client.post(
                '/user/authenticate',
                data=json.dumps(user_data),
                headers={'content-type': 'application/json'})
            self.assert200(result)
            data = json.loads(result.data)
            self.assertTrue(data["authenticated"])

            # wrong password gives false
            user_data["password"] = "wrongpassword"
            result = client.post(
                '/user/authenticate',
                data=json.dumps(user_data),
                headers={'content-type': 'application/json'})
            self.assert200(result)
            data = json.loads(result.data)
            self.assertFalse(data["authenticated"])
