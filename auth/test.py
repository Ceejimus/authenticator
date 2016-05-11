import unittest
from io import StringIO
import os

print(__name__)

def run_tests():
    output = StringIO()
    # for dirname, dirnames, filenames in os.walk('/code/'):
    # 	print("black")
    #     # print path to all filenames.
    #     for filename in filenames:
    #         blah = os.path.join(dirname, subdirname, filename)
    #         with f as open(blah, 'r'):
    #             print(filename)

    suite = unittest.TestLoader().discover('/code/tests/', pattern='*.py', top_level_dir='/code/')
    unittest.TextTestRunner(verbosity=2, stream=output).run(suite)
    return output.getvalue()

if __name__ == "__main__":
	print("Running tests...")
	test_results = run_tests()
	with open('/test_results/auth_test_results.txt', mode='w+') as file:
		file.write(test_results)