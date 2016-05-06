import unittest
from flask.ext.testing import TestCase
from app import app, db

class MyTest(TestCase):
    def create_app(self):
        app.config.from_pyfile('testconfig.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove();
        db.drop_all()

    def test_passed_test(self):
        self.assertEqual(2, 2)

    def test_passed_test2(self):
        self.assertEqual(2, 2)

    def test_failed_test(self):
        self.assertEqual(2, 4)

    def test_failed_test2(self):
        self.assertEqual(2, 4)

test_cases = [MyTest]

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite