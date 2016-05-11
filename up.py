#! /c/Users/cj/AppData/Local/Programs/Python/Python35/python
import unittest
from io import StringIO
from subprocess import call, check_output
import re
import os
import shutil

FAILED_TEST_INFO_REGEX_FORMAT_STR = "(FAIL|ERROR): {0}"

class Test(object):
    def __init__(self, failed, file, suite, name):
        self.failed = failed
        self.file = file
        self.suite = suite
        self.name = name
        self.details = []

    def setDetails(self, details):
        self.details = details

class TestRun(object):
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

    def allTestsPassed(self):
        return len(self.failed_tests) == 0

    def __str__(self):
        out = "="*80
        out += "\n"
        out += "="*80
        out += "\n"
        if (self.summary == None):
            out += "No Summary\n"
        else:
            out += self.summary
            out += "\n"

        out += "\n"

        failed_test_count = len(self.failed_tests)
        passed_test_count = len(self.passed_tests)
        test_count = failed_test_count + passed_test_count

        if failed_test_count > 0:
            out += "{0}/{1} tests failed ...\n\n".format(failed_test_count, test_count)
        for failed_test in self.failed_tests:
            out += "{0}.{1}.{2} failed...\nDetails:\n".format(
                    failed_test.file,
                    failed_test.suite,
                    failed_test.name
                )
            for line in failed_test.details:
                out += line
                out += "\n"

        if passed_test_count > 0:
            out += "{0}/{1} tests passed ...\n\n".format(passed_test_count, test_count)
        for passed_test in self.passed_tests:
            out += "[PASSED] {0}.{1}.{2}...\n".format(
                    passed_test.file,
                    passed_test.suite,
                    passed_test.name
                )
            out += "\n"

        out += "="*80
        out += "\n"
        out += "="*80
        out += "\n"

        return out

def parse_test_results(test_results):
    test_summary_regex = r'Ran\s+(\d+)\s+test(s?)\s+in\s+(\d+\.\d+)(\w+)'
    failed_tests_regex = r'((\w+)\s+\((\w+)\.(\w+)\)).*(FAIL|ERROR)'
    passed_tests_regex = r'((\w+)\s+\((\w+)\.(\w+)\)).*(ok)'
    separator_regex = r'([=-])\1{40,}'

    testRun = TestRun()
    lines = test_results.split('\n')
    for line in lines:
        if testRun.hasSummary() == False:
            match = re.search(test_summary_regex, line)
            if match != None:
                testRun.setSummary(match.group(0))
                continue
        match = re.search(failed_tests_regex, line)
        if match != None:
            file = match.group(3)
            suite = match.group(4)
            name = match.group(2)
            testRun.addFailedTest(file, suite, name)
            continue
        match = re.search(passed_tests_regex, line)
        if match != None:
            file = match.group(3)
            suite = match.group(4)
            name = match.group(2)
            testRun.addPassedTest(file, suite, name)
            continue

    for test in testRun.failed_tests:
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
                test.setDetails(details)

    return(testRun)

test_output_dir = './test_results/'

dirs_deleted = []
for dirname, dirnames, filenames in os.walk('.'):
    for subdirname in dirnames:
        if re.search("__pycache__", subdirname):
            print("removing '{}'".format(os.path.join(dirname, subdirname)))
            shutil.rmtree(os.path.join(dirname, subdirname))

    for filename in filenames:
        if re.search("(\.p((o)|(yc))$)", filename):
            print("removing '{}'".format(os.path.join(dirname, subdirname, filename)))
            os.remove(os.path.join(dirname, subdirname, file))


# build the composition
call(["docker-compose", "build"])

# for some reason I have to call tests twice for it to pick up changes
# not a big deal ... for now
call(["docker-compose", "run", "-d", "--rm", "auth", "python", "test.py"])
# call(["docker-compose", "run", "-d", "--rm", "auth", "python", "test.py"])

# open test results -- parse -- print results
with open('./test_results/auth_test_results.txt', 'r') as f:
    print(str(parse_test_results(f.read())))
