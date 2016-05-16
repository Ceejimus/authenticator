import unittest

from tests.usertests import UserTests
from tests.apitests import ApiTests


test_cases = [UserTests, ApiTests]


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        print(tests)
        suite.addTests(tests)
    return suite
