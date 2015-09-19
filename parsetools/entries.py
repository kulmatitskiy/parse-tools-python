from schema import Column, make_insert_tuple, make_col_name_tuple
from jsondump import *

def columns_from_list_of_entries(entries):
    if len(entries) == 0:
        return []

    first = entries[0]
    columns = []
    for k, v in first.iteritems():
        columns.append(Column.create(k, v))
    return columns


def make_insert_query(tablename, columns, entries):
    tuples = map(lambda entry: make_insert_tuple(entry, columns), entries)
    return "INSERT INTO %s\n    %s\nVALUES\n    %s" % (tablename, make_col_name_tuple(columns), ",\n    ".join(tuples))

def insert_statement_for_all_from_dir(input_path):
    stmt = ""
    for class_name, file_path in class_data_in_path(input_path).iteritems():
        entries = load_all_json_entries_at_once(file_path)
        columns = columns_from_list_of_entries(entries)
        stmt = stmt + make_insert_query(class_name, columns, entries) + "\n"
    return stmt


