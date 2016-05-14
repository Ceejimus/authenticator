import re

FAILED_TEST_INFO_REGEX_FORMAT_STR = "(FAIL|ERROR): {0}\s+"


class Test(object):

    def __init__(self, failed, file, suite, name):
        self.failed = failed
        self.file = file
        self.suite = suite
        self.name = name
        self.details = []

    def set_details(self, details):
        self.details = details


class TestRun(object):

    def __init__(self):
        self.summary = None
        self.passed_tests = []
        self.failed_tests = []

    def has_summary(self):
        return self.summary is not None

    def set_summary(self, summary):
        self.summary = summary

    def add_failed_test(self, file, suite, name):
        self.failed_tests.append(Test(True, file, suite, name))

    def add_passed_test(self, file, suite, name):
        self.passed_tests.append(Test(False, file, suite, name))

    def set_details(self, name, details):
        for failed_test in self.failed_tests:
            if failed_test.name == name:
                failed_test.set_details(details)

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

        failed_test_count = len(self.failed_tests)
        passed_test_count = len(self.passed_tests)
        test_count = failed_test_count + passed_test_count

        if failed_test_count > 0:
            out += "{0}/{1} tests failed ...\n\n".format(
                failed_test_count, test_count)
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
            out += "{0}/{1} tests passed ...\n\n".format(
                passed_test_count, test_count)
        for passed_test in self.passed_tests:
            out += "[PASSED] {0}.{1}.{2}\n".format(
                passed_test.file,
                passed_test.suite,
                passed_test.name
            )
            out += "\n"

        out += "=" * 80
        out += "\n"
        out += "=" * 80
        out += "\n"

        return out


def parse_test_results(test_results):
    test_summary_regex = r'Ran\s+(\d+)\s+test(s?)\s+in\s+(\d+\.\d+)(\w+)'
    failed_tests_regex = r'((\w+)\s+\((\w+)\.(\w+)\)).*(FAIL|ERROR)'
    passed_tests_regex = r'((\w+)\s+\((\w+)\.(\w+)\)).*(ok)'
    separator_regex = r'([=-])\1{40,}'

    test_run = TestRun()
    lines = test_results.split('\n')
    i = 0
    for line in lines:
        i += 1
        # print("line: {} -- {}".format(i, line))
        if not test_run.has_summary():
            match = re.search(test_summary_regex, line)
            if match is not None:
                # print("summary found")
                test_run.set_summary(match.group(0))
                continue
        match = re.search(failed_tests_regex, line)
        if match is not None:
            file = match.group(3)
            suite = match.group(4)
            name = match.group(2)
            # print("failed {}.{}.{}".format(file, suite, name))
            test_run.add_failed_test(file, suite, name)
            continue
        match = re.search(passed_tests_regex, line)
        if match is not None:
            file = match.group(3)
            suite = match.group(4)
            name = match.group(2)
            # print("passed {}.{}.{}".format(file, suite, name))
            test_run.add_passed_test(file, suite, name)
            continue

    for test in test_run.failed_tests:
        i = 0
        while (i < len(lines)):
            failed_test_regex = FAILED_TEST_INFO_REGEX_FORMAT_STR.format(
                re.escape(test.name))
            # print("line: {} -- {}".format(i, lines[i]))
            match = re.search(failed_test_regex, lines[i])
            if match is not None:
                # print("Match Found! [REGEX] {}".format(failed_test_regex))
                details = []
                i += 2
                match = re.search(separator_regex, lines[i])
                while match is None:
                    details.append(lines[i])
                    i += 1
                    match = re.search(separator_regex, lines[i])
                test.set_details(details)
                print("details for {}.{}.{}:\n{}".format(
                    test.file, test.suite, test.name, details))
            i += 1

    return(test_run)
