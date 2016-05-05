from flask_failsafe import failsafe
import unittest
from io import StringIO
import re

FAILED_TEST_INFO_REGEX_FORMAT_STR = "FAIL: {0}$.*\-+"

def run_tests():
    output = StringIO()
    suite = unittest.TestLoader().discover('/code/tests/', pattern='*.py', top_level_dir='/code/')
    unittest.TextTestRunner(verbosity=2, stream=output).run(suite)
    return output.getvalue()

def parse_test_results(test_results):
    print("------------ TEST RESULTS -------------")

    test_summary_regex = r'Ran\s+(\d+)\s+test(s?)\s+in\s+(\d+\.\d+)(\w+)'
    results = {}
    for line in test_results.split('\n'):
        if ('summary' not in results):
            match = re.search(test_summary_regex, line)
            if match != None:
                results['summary'] = match.group(0)
        print(line)
    print('Results Summary: %s' % results['summary'])

    print("------------ END RESULTS  -------------")

    print("------------ REGEX RESULTS -------------")

    # find and print test summary
    test_summary = re.search(test_summary_regex, test_results)
    num_tests = int(test_summary.group(1))
    time_taken = float(test_summary.group(3))
    time_unit = test_summary.group(4)
    print(" ----- %d test%s ran in %s(%s)" % (
            num_tests, 
            test_summary.group(2), #test or tests
            time_taken,
            time_unit
        )
    )
    # find and print failed tests summary
    failed_tests_regex = r'((\w+)\s+\((\w+)\.(\w+)\)).*(FAIL)'
    failed_tests = re.finditer(failed_tests_regex, test_results)
    print(" \n---- Failures -----\n")
    for failed_test in failed_tests:
        failed_test_regex = FAILED_TEST_INFO_REGEX_FORMAT_STR.format(re.escape(failed_test.group(1)))
        test_info = re.search(failed_test_regex, test_results, re.DOTALL)
        print(failed_test_regex)
        print(test_results)
        print(test_info)
        module = failed_test.group(3)
        fixture = failed_test.group(4)
        test = failed_test.group(2)
        print(" ----- Module: \"%s\" -- Fixture: \"%s\" -- Test: \"%s\"" % (
                module,
                fixture,
                test
            )
        )

    # for test in failed_tests:
    #     print(test)
    # print(sum(1 for _ in failed_tests))
    # if failed_tests == None or len(failed_tests) == 0:
    #     print("no failed tests")
    # else:
    #     for failed_test in failed_tests:
    #         print(failed_test)

    # find and print passed tests summary
    passed_tests_regex = r'(\w+)\s+\((\w+)\.(\w+)\).*(ok)'
    passed_tests = re.finditer(passed_tests_regex, test_results)
    # if passed_tests == None or len(passed_tests) == 0:
    #     print("no passed tests")
    print("------------ END RESULTS  -------------")

@failsafe
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time
    from app import app
    return app

if __name__ == "__main__":
    parse_test_results(run_tests())
    create_app().run(host="0.0.0.0", port=8081, debug=True)
