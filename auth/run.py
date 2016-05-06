from flask_failsafe import failsafe
import unittest
from io import StringIO
import re

FAILED_TEST_INFO_REGEX_FORMAT_STR = "FAIL: {0}"

class Test(object):
    def __init__(self, failed, file, suite, name):
        self.failed = failed
        self.file = file
        self.suite = suite
        self.name = name
        self.details = []

    def setDetails(self, details):
        self.details = details

class TestsSummary(object):
    def __init__(self):
        self.summary = None
        self.passed_tests = []
        self.failed_tests = []

    def hasSummary(self):
        return self.summary != None

    def setSummary(self, summary):
        self.summary = summary

    def addFailedTest(self, file, suite, name):
        self.failed_tests.append(Test(True, file, suite, name))

    def addPassedTest(self, file, suite, name):
        self.passed_tests.append(Test(False, file, suite, name))

    def setDetils(self, name, details):
        for failed_test in self.failed_tests:
            if failed_test.name == name:
                failed_test.setDetails(details)

    def __str__(self):
        out = ""
        if (self.summary == None):
            out += "No Summary"
        else:
            out += self.summary
        out += "\n"

        for failed_test in self.failed_tests:
            out += "{0}.{1}.{2} failed...\nDetails:\n".format(
                    failed_test.file,
                    failed_test.suite,
                    failed_test.name
                )
            for line in failed_test.details:
                out += line
                out += "\n"

        return out

def run_tests():
    output = StringIO()
    suite = unittest.TestLoader().discover('/code/tests/', pattern='*.py', top_level_dir='/code/')
    unittest.TextTestRunner(verbosity=2, stream=output).run(suite)
    return output.getvalue()

def parse_test_results(test_results):
    found_equals_line = False
    print("------------ TEST RESULTS -------------")
    print(test_results)
    print("------------ END RESULTS  -------------")

    test_summary_regex = r'Ran\s+(\d+)\s+test(s?)\s+in\s+(\d+\.\d+)(\w+)'
    failed_tests_regex = r'((\w+)\s+\((\w+)\.(\w+)\)).*(FAIL)'
    passed_tests_regex = r'(\w+)\s+\((\w+)\.(\w+)\).*(ok)'
    separator_regex = r'([=-])\1{40,}'

    results = {
        "summary": None,
        "failed_tests": [],
        "passed_tests": []
    }
    testsSummary = TestsSummary()
    lines = test_results.split('\n')
    for line in lines:
        if testsSummary.hasSummary() == False:
            match = re.search(test_summary_regex, line)
            if match != None:
                testsSummary.setSummary(match.group(0))
                continue
        match = re.search(failed_tests_regex, line)
        if match != None:
            file = match.group(2)
            suite = match.group(3)
            name = match.group(1)
            testsSummary.addFailedTest(file, suite, name)
            continue
        match = re.search(passed_tests_regex, line)
        if match != None:
            file = match.group(2)
            suite = match.group(3)
            name = match.group(1)
            testsSummary.addPassedTest(file, suite, name)
            continue

    for test in testsSummary.failed_tests:
        failed_test_regex = FAILED_TEST_INFO_REGEX_FORMAT_STR.format(re.escape(test.name))
        for i in range(len(lines)):
            match = re.search(failed_test_regex, lines[i])
            if match != None:
                details = []
                i += 2
                match = re.search(separator_regex, lines[i])
                while match == None:
                    details.append(lines[i])
                    i += 1
                    match = re.search(separator_regex, lines[i])
                print(details)
                test.setDetails(details)

    print(str(testsSummary))

@failsafe
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time
    from app import app
    return app

if __name__ == "__main__":
    parse_test_results(run_tests())
    create_app().run(host="0.0.0.0", port=8081, debug=True)
