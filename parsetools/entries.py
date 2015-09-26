from schema import Column, IdColumn, make_insert_tuple, make_col_name_tuple
from jsondump import *
import pandas as pd
import time
import logging

def columns_from_list_of_entries(entries):
    if len(entries) == 0:
        return []

    first = entries[0]
    columns = []
    for k, v in first.iteritems():
        columns.append(Column.create(k, v))
    return columns

def make_create_table_query(table_name, columns, drop_if_exists=True):
    stmt = ""
    if drop_if_exists:
        stmt += "DROP TABLE IF EXISTS %s CASCADE;\n" % table_name
        stmt += "CREATE TABLE %s\n(\n" % table_name
    else:
        stmt += "CREATE TABLE IF NOT EXISTS %s\n(\n" % table_name

    stmt += ',\n'.join(["  %s %s" % (c.db_name, c.db_type) for c in columns]) + "\n);\n"
    return stmt


def make_insert_query(table_name, columns, entries):
    tuples = [make_insert_tuple(entry, columns) for entry in entries]
    return "INSERT INTO %s\n  %s\nVALUES\n  %s;\n" % (table_name, make_col_name_tuple(columns), ",\n  ".join(tuples))


def make_data_frame(entries):
    columns = columns_from_list_of_entries(entries)
    out = dict()
    for entry in entries:
        id = None
        new_entry = dict()
        for column in columns:
            if isinstance(column, IdColumn):
                id = entry[column.parse_name]
            else:
                new_entry[column.db_name] = column.plain_val(entry[column.parse_name])
        if id:
            out[id] = new_entry
        else:
            logging.warning("Found an entry with missing objectId; skipping.")

    return pd.DataFrame.from_dict(out, orient='index')


def snapshot_dump_from_dir(input_path):
    schema_name = "Snapshot_%s" % time.strftime("%Y_%m_%d")
    stmt = "CREATE SCHEMA IF NOT EXISTS %s;\n" % schema_name

    for class_name, file_path in class_data_in_path(input_path).iteritems():
        entries = load_all_json_entries_at_once(file_path)
        columns = columns_from_list_of_entries(entries)

        table_name = "%s.%s" %(schema_name, class_name)

        stmt += make_create_table_query(table_name, columns)
        stmt += make_insert_query(table_name, columns, entries) + "\n"

    return stmt


