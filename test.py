import os
from os import path
import parsetools

dir = path.dirname(path.abspath(__file__))
os.chdir(dir)
current_path = os.getcwd()
print("Changed working directory to: %s\n" % current_path)

print parsetools.snapshot_dump_from_dir(current_path + "/test_data")