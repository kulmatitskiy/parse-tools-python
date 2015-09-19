import os
from os import path
import parsetools

dir = path.dirname(path.abspath(__file__))
os.chdir(dir)
current_path = os.getcwd()
print("Changed working directory to: %s\n" % current_path)

print parsetools.insert_statement_for_all_from_dir(current_path + "/test_data")