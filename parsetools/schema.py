import logging
import numbers
from time import strptime
from datetime import datetime

def on_wrong_type(col_name, col_type):
    logging.warning("Attempt to get an INSERT-tuple for a %s column (%s) and non-%s value. Will use NULL instead."
                    % (col_type, col_name, col_type))
    return 'NULL'


class Column(object):
    db_name = ""
    parse_name = ""

    def __init__(self, name):
        self.db_name = name if name != 'objectId' else 'object_id'
        self.parse_name = name

    @classmethod
    def check(cls, key, val):
        return True

    @staticmethod
    def insert_str_for_val(val):
        return "NULL"

    @staticmethod
    def plain_val(val):
        return None

    @classmethod
    def create(cls, name, example):
        for col_type in [StampColumn, BooleanColumn, NumericColumn, DateColumn,
                        GeoPointColumn, PointerColumn, IdColumn, TextColumn]:
            if col_type.check(name, example):
                return col_type(name)


class TextColumn(Column):
    db_type = 'text'

    @classmethod
    def check(cls, key, val):
        return True

    @staticmethod
    def plain_val(val):
        return str(val)

    @staticmethod
    def insert_str_for_val(val):
        return '\'%s\'' % str(val)


class IdColumn(TextColumn):
    @classmethod
    def check(cls, key, val):
        return key == 'objectId'


class BooleanColumn(Column):
    db_type = 'boolean'

    @classmethod
    def check(cls, key, val):
        return isinstance(val, bool)

    @staticmethod
    def plain_val(val):
        return val

    def insert_str_for_val(self, val):
        if BooleanColumn.check(None, val):
            return 'TRUE' if val else 'FALSE'
        return on_wrong_type(self.parse_name, 'Boolean')


class NumericColumn(Column):
    db_type = 'numeric'

    @classmethod
    def check(cls, key, val):
        return isinstance(val, numbers.Number)

    @staticmethod
    def plain_val(val):
        return float(val)

    def insert_str_for_val(self, val):
        if NumericColumn.check(None, val):
            return str(val)
        return on_wrong_type(self.parse_name, 'Numeric')


class DateColumn(Column):
    db_type = 'timestamp without time zone'

    @classmethod
    def check(cls, key, val):
        return isinstance(val, dict) and val.get('__type') == 'Date'

    @staticmethod
    def extract_date_string(iso):
        return str(iso).replace('T', ' ')[:-5]

    @staticmethod
    def plain_val(val):
        if not DateColumn.check(None, val):
            return None
        iso = val.get('iso')
        if isinstance(iso, (str, unicode)):
            try:
                struct_t = strptime(DateColumn.extract_date_string(iso), '%Y-%m-%d %H:%M:%S')
                return datetime(*struct_t[:6])
            except ValueError as e:
                logging.warning(e.message)
                return None
        return None

    def insert_str_for_val(self, val):
        if not DateColumn.check(None, val):
            return on_wrong_type('Date')
        iso = val.get('iso')
        if isinstance(iso, (str, unicode)):
            return "\'%s\'" % DateColumn.extract_date_string(iso)
        return on_wrong_type(self.parse_name, 'Date')


class StampColumn(Column):
    def __init__(self, name):
        self.parse_name = name
        self.db_name = "created_at" if name == 'createdAt' else 'updated_at'

    @classmethod
    def check(cls, key, val):
        return key == 'updatedAt' or key == 'createdAt'

    @staticmethod
    def plain_val(val):
        try:
            struct_t = strptime(DateColumn.extract_date_string(val), '%Y-%m-%d %H:%M:%S')
            return datetime(*struct_t[:6])
        except ValueError as e:
            logging.warning(e.message)
            return None

    @staticmethod
    def insert_str_for_val(val):
        return "\'%s\'" % val.replace('T', ' ')[:-5]


class GeoPointColumn(Column):
    db_type = 'text'

    @classmethod
    def check(cls, key, val):
        return isinstance(val, dict) and val.get('__type') == 'GeoPoint'

    @staticmethod
    def plain_val(val):
        if GeoPointColumn.check(None, val):
            return str(val.get('longitude')) + ', ' + str(val.get('latitude'))
        return None

    def insert_str_for_val(self, val):
        if GeoPointColumn.check(None, val):
            return str(val.get('longitude')) + ', ' + str(val.get('latitude'))
        return on_wrong_type(self.parse_name, 'GeoPoint')


class PointerColumn(Column):
    db_type = 'text'

    def __init__(self, name):
        self.parse_name = name
        self.db_name = name + "_id"

    @classmethod
    def check(cls, key, val):
        return isinstance(val, dict) and val.get('__type') == 'Pointer'

    @staticmethod
    def plain_val(val):
        if not PointerColumn.check(None, val):
            return None
        objid = val.get('objectId')
        if isinstance(objid, (str, unicode)):
            return str(objid)
        return None

    def insert_str_for_val(self, val):
        if not PointerColumn.check(None, val):
            return on_wrong_type('Pointer')
        objid = val.get('objectId')
        if isinstance(objid, (str, unicode)):
            return "\'%s\'" % str(objid)
        return on_wrong_type(self.parse_name, 'Pointer')


def make_col_name_tuple(columns):
    return "(" + ", ".join(map(lambda col: col.db_name, columns)) + ")"


def make_insert_tuple(obj, columns):
    inserts = []
    for col in columns:
        if col.parse_name not in obj:
            inserts.append("NULL")
        else:
            inserts.append(col.insert_str_for_val(obj[col.parse_name]))

    return "(" + ", ".join(inserts) + ")"



