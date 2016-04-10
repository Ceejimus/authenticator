from flask_failsafe import failsafe
import unittest
from io import StringIO
import re

def run_tests():
    output = StringIO()
    suite = unittest.TestLoader().discover('/code/tests/', pattern='*.py', top_level_dir='/code/')
    unittest.TextTestRunner(verbosity=2, stream=output).run(suite)
    return output.getvalue()

def parse_test_results(test_results):
    print("------------ TEST RESULTS -------------")
    print(test_results)
    print("------------ END RESULTS  -------------")
    print("------------ REGEX RESULTS -------------")
    # find and print test summary
    test_summary_regex = r'Ran\s+(\d+)\s+test(s?)\s+in\s+(\d+\.\d+)(\w+)'
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
    passed_tests_regex = r'(\w+)\s+\((\w+)\.(\w+)\)\s+\.\.\.\s+(ok)'
    passed_tests = re.finditer(passed_tests_regex, test_results)

    # find and print passed tests summary
    failed_tests_regex = r'(\w+)\s+\((\w+)\.(\w+)\)\s+\.\.\.\s+(FAIL)'
    failed_tests = re.finditer(failed_tests_regex, test_results)
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
