from common import *

def class_data_in_path(input_path):
    """Finds *.json files in input directory

    :param str_path: - path string.
    :return: - a dict of type {parse_class_name: full_path_to_file_with_data}.
    """
    d = {}
    for filename in files_in_path(input_path):
        if filename.endswith('.json'):
            d[filename[:-5]] = path.join(input_path, filename)
    return d

def load_all_json_entries_at_once(file_path):
    """Return a list of entries (dicts) containing class data

    :param filepath:  - full path to json with class data
    :return: - list of dictionaries with instance data
    """
    contents = json_contents(file_path)
    if isinstance(contents, dict) and (len(list(contents)) == 1) and ('results' in contents):
        return contents['results']
    else:
        logging.warning("Valid JSON but invalid schema.")
        return []

