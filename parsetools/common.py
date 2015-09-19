import logging
import os
from os import path
import json

def files_in_path(str_path):
    try:
        return [f for f in os.listdir(str_path) if path.isfile(path.join(str_path, f))]
    except OSError as e:
        logging.error(e.strerror)
        return []

def json_contents(file_path):
    try:
        f = open(file_path)
    except IOError as e:
        logging.warning(e.strerror)
        return None

    try:
        return json.load(f)
    except ValueError as e:
        logging.warning("Could not decode JSON. " + e.strerror)
        return None
    finally:
        f.close()
