import re

FAILED_TEST_INFO_REGEX_FORMAT_STR = "(FAIL|ERROR): {0}\s+"
TEST_SUMMARY_REGEX = r'Ran\s+(\d+)\s+test(s?)\s+in\s+(\d+\.\d+)(\w+)'
FAILED_TESTS_REGEX = r'((\w+)\s+\((.*)\).*(FAIL|ERROR))'
PASSED_TESTS_REGEX = r'((\w+)\s+\((.*)\).*ok)'
SEPARATOR_REGEX = r'([=-])\1{40,}'


class Test(object):

    def __init__(self, failed, location, name):
        self.failed = failed
        self.location = location
        self.name = name
        self.details = []

    def set_details(self, details):
        self.details = details


class TestRun(object):

    def __init__(self):
        self.summary = None
        self.tests = []

    def has_summary(self):
        return self.summary is not None

    def set_summary(self, summary):
        self.summary = summary

    def add_test(self, test):
        self.tests.append(test)

    def set_details(self, name, details):
        for test in self.tests:
            if test.name == name:
                test.set_details(details)

    def all_tests_passed(self):
        return len(self.failed_tests) == 0

    def __str__(self):
        out = "=" * 80
        out += "\n"
        out += "=" * 80
        out += "\n"
        if self.summary is None:
            out += "No Summary\n"
        else:
            out += self.summary
            out += "\n"

        out += "\n"

        failed_tests = [test for test in self.tests if test.failed]
        passed_tests = [test for test in self.tests if not test.failed]

        failed_test_count = len(failed_tests)
        passed_test_count = len(passed_tests)
        test_count = failed_test_count + passed_test_count

        if failed_test_count > 0:
            out += "{0}/{1} tests failed ...\n\n".format(
                failed_test_count, test_count)
        for failed_test in failed_tests:
            out += "[FAILED] {0}.{1}\nDetails:\n".format(
                failed_test.location,
                failed_test.name
            )
            for line in failed_test.details:
                out += line
                out += "\n"

        if passed_test_count > 0:
            out += "{0}/{1} tests passed ...\n\n".format(
                passed_test_count, test_count)
        for passed_test in passed_tests:
            out += "[PASSED] {0}.{1}\n".format(
                passed_test.location,
                passed_test.name
            )
            out += "\n"

        out += "=" * 80
        out += "\n"
        out += "=" * 80
        out += "\n"

        return out


def parse_test_results(test_results):
    test_run = TestRun()
    lines = test_results.split('\n')
    i = 0
    for line in lines:
        i += 1
        if not test_run.has_summary():
            match = re.search(TEST_SUMMARY_REGEX, line)
            if match is not None:
                test_run.set_summary(match.group(0))
                continue
        match = re.search(FAILED_TESTS_REGEX, line)
        if match is not None:
            location = match.group(3)
            name = match.group(2)
            failed_test = Test(True, location, name)
            test_run.add_test(failed_test)
            continue
        match = re.search(PASSED_TESTS_REGEX, line)
        if match is not None:
            location = match.group(3)
            name = match.group(2)
            passed_test = Test(False, location, name)
            test_run.add_test(passed_test)
            continue

    failed_tests = (test for test in test_run.tests if test.failed)

    for test in failed_tests:
        i = 0
        while (i < len(lines)):
            failed_test_regex = FAILED_TEST_INFO_REGEX_FORMAT_STR.format(
                re.escape(test.name))
            match = re.search(failed_test_regex, lines[i])
            if match is not None:
                details = []
                i += 2
                match = re.search(SEPARATOR_REGEX, lines[i])
                while match is None:
                    details.append(lines[i])
                    i += 1
                    match = re.search(SEPARATOR_REGEX, lines[i])
                test.set_details(details)
            i += 1

    return(test_run)
