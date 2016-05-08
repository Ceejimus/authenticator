import unittest
from io import StringIO

def run_tests():
    output = StringIO()
    suite = unittest.TestLoader().discover('/code/tests/', pattern='*.py', top_level_dir='/code/')
    unittest.TextTestRunner(verbosity=2, stream=output).run(suite)
    return output.getvalue()

if __name__ == "__main__":
	file = open('/test_results/auth_test_results.txt', mode='w+')
	file.write(run_tests())
	file.close()