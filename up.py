#! /c/Users/cj/AppData/Local/Programs/Python/Python35/Python3
import os
import re
import shutil
import time

from subprocess import call, check_call

from testparser import parse_test_results


def remove_stupid_cache_files():
    for dirname, dirnames, filenames in os.walk('.'):
        for subdirname in dirnames:
            if re.search("__pycache__", subdirname):
                dir_to_remove = os.path.join(dirname, subdirname)
                print("removing '{}'".format(dir_to_remove))
                shutil.rmtree(dir_to_remove)

        for filename in filenames:
            if re.search("(\.p((o)|(yc))$)", filename):
                file_to_remove = os.path.join(dirname, subdirname, filename)
                if (os.path.isfile(file_to_remove)):
                    print("removing '{}'".format(file_to_remove))
                    os.remove(file_to_remove)

remove_stupid_cache_files()

results_dir = './test_results/'

if not os.path.exists(results_dir):
    os.makedirs(results_dir)

auth_results_file = "auth_test_results.txt"
auth_results_full_path = os.path.join(results_dir, auth_results_file)
print(auth_results_full_path)

if (os.path.isfile(auth_results_full_path)):
    os.remove(auth_results_full_path)

# build the composition
check_call(["docker-compose", "build"])

check_call(
    [
        "docker-compose",
        "run",
        "-d",
        "--rm",
        "auth",
        "python",
        "test.py",
        auth_results_file
    ])

while (not os.path.isfile(auth_results_full_path)):
    time.sleep(0.1)

time.sleep(2)

with open(auth_results_full_path, 'r') as f:
    test_results = parse_test_results(f.read())
    f.close()

print(str(test_results))

failed_tests = [test for test in test_results.tests if test.failed]

if len(failed_tests) > 0:
    print("TESTS FAILED! Postponing startup...")
else:
    call(["docker-compose", "up"])
