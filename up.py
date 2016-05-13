#! /c/Users/cj/AppData/Local/Programs/Python/Python35/python
import unittest
from io import StringIO
from subprocess import check_call
import re
import os
import shutil
import time
import datetime

FAILED_TEST_INFO_REGEX_FORMAT_STR = "(FAIL|ERROR): {0}\s+"

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
            out += "[FAILED] {0}.{1}.{2}\nDetails:\n".format(
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
            out += "[PASSED] {0}.{1}.{2}\n".format(
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
    i = 0
    for line in lines:
        i += 1
        # print("line: {} -- {}".format(i, line))
        if testRun.hasSummary() == False:
            match = re.search(test_summary_regex, line)
            if match != None:
                # print("summary found")
                testRun.setSummary(match.group(0))
                continue
        match = re.search(failed_tests_regex, line)
        if match != None:
            file = match.group(3)
            suite = match.group(4)
            name = match.group(2)
            # print("failed {}.{}.{}".format(file, suite, name))
            testRun.addFailedTest(file, suite, name)
            continue
        match = re.search(passed_tests_regex, line)
        if match != None:
            file = match.group(3)
            suite = match.group(4)
            name = match.group(2)
            # print("passed {}.{}.{}".format(file, suite, name))
            testRun.addPassedTest(file, suite, name)
            continue

    for test in testRun.failed_tests:
        i = 0
        while (i < len(lines)):
            failed_test_regex = FAILED_TEST_INFO_REGEX_FORMAT_STR.format(re.escape(test.name))
            # print("line: {} -- {}".format(i, lines[i]))
            match = re.search(failed_test_regex, lines[i])
            if match != None:
                # print("Match Found! [REGEX] {}".format(failed_test_regex))
                details = []
                i += 2
                match = re.search(separator_regex, lines[i])
                while match == None:
                    details.append(lines[i])
                    i += 1
                    match = re.search(separator_regex, lines[i])
                test.setDetails(details)
                print("details for {}.{}.{}:\n{}".format(test.file, test.suite, test.name, details))
            i += 1

    return(testRun)

def remove_stupid_cache_files():
    for dirname, dirnames, filenames in os.walk('.'):
        for subdirname in dirnames:
            if re.search("__pycache__", subdirname):
                print("removing '{}'".format(os.path.join(dirname, subdirname)))
                shutil.rmtree(os.path.join(dirname, subdirname))

        for filename in filenames:
            if re.search("(\.p((o)|(yc))$)", filename):
                print("removing '{}'".format(os.path.join(dirname, subdirname, filename)))
                os.remove(os.path.join(dirname, subdirname, file))

remove_stupid_cache_files()

results_dir = './test_results/'
auth_results_file = "auth_test_results.txt"
auth_results_full_path = os.path.join(results_dir, auth_results_file)
print(auth_results_full_path)

# build the composition
check_call(["docker-compose", "build"])

check_call(["docker-compose", "run", "-d", "--rm", "auth", "python", "test.py", auth_results_file])

# for some god damn reason the file doesn't get finished writing by the time this is executed
# if it takes longer than a second to write the file then something is up
# time.sleep(1)
# open test results -- parse -- print results

while (not os.path.isfile(auth_results_full_path)):
    time.sleep(0.1)

time.sleep(0.5)

with open(auth_results_full_path, 'r') as f:
    print(str(parse_test_results(f.read())))

time.sleep(0.5)

os.remove(auth_results_full_path)
