import logging
import numbers

def on_wrong_type(col_name, col_type):
    logging.warning("Attempt to get an INSERT-tuple for a %s column (%s) and non-%s value. Will use NULL instead."
                    % (col_type, col_name, col_type))
    return 'NULL'


class Column(object):
    name = ""

    def __init__(self, name):
        self.name = name

    @classmethod
    def check(cls, key, val):
        return True

    @staticmethod
    def insert_str_for_val(cls, val):
        return "NULL"

    @classmethod
    def create(cls, name, example):
        for col_type in [StampColumn, BooleanColumn, NumericColumn, DateColumn,
                        GeoPointColumn, PointerColumn, TextColumn]:
            if col_type.check(name, example):
                return col_type(name)


class TextColumn(Column):
    @classmethod
    def check(cls, key, val):
        return True

    @staticmethod
    def insert_str_for_val(val):
        return '\'%s\'' % str(val)


class BooleanColumn(Column):
    @classmethod
    def check(cls, key, val):
        return isinstance(val, bool)

    def insert_str_for_val(self, val):
        if BooleanColumn.check(None, val):
            return 'TRUE' if val else 'FALSE'
        return on_wrong_type(self.name, 'Boolean')


class NumericColumn(Column):
    @classmethod
    def check(cls, key, val):
        return isinstance(val, numbers.Number)

    def insert_str_for_val(self, val):
        if NumericColumn.check(None, val):
            return str(val)
        return on_wrong_type(self.name, 'Numeric')


class DateColumn(Column):
    @classmethod
    def check(cls, key, val):
        return isinstance(val, dict) and val.get('__type') == 'Date'

    def insert_str_for_val(self, val):
        if not DateColumn.check(None, val):
            return on_wrong_type('Date')
        iso = val.get('iso')
        if isinstance(iso, (str, unicode)):
            return "\'%s\'" % str(iso).replace('T', ' ')[:-5]
        return on_wrong_type(self.name, 'Date')


class StampColumn(Column):
    @classmethod
    def check(cls, key, val):
        return key == 'updatedAt' or key == 'createdAt'

    @staticmethod
    def insert_str_for_val(val):
        return "\'%s\'" % val.replace('T', ' ')[:-5]


class GeoPointColumn(Column):
    @classmethod
    def check(cls, key, val):
        return isinstance(val, dict) and val.get('__type') == 'GeoPoint'

    def insert_str_for_val(self, val):
        if GeoPointColumn.check(None, val):
            return str(val.get('longitude')) + ', ' + str(val.get('latitude'))
        return on_wrong_type(self.name, 'GeoPoint')


class PointerColumn(Column):
    @classmethod
    def check(cls, key, val):
        return isinstance(val, dict) and val.get('__type') == 'Pointer'

    def insert_str_for_val(self, val):
        if not PointerColumn.check(None, val):
            return on_wrong_type('Pointer')
        objid = val.get('objectId')
        if isinstance(objid, (str, unicode)):
            return "\'%s\'" % str(objid)
        return on_wrong_type(self.name, 'Pointer')


def make_col_name_tuple(columns):
    return "(" + ", ".join(map(lambda col: col.name, columns)) + ")"


def make_insert_tuple(obj, columns):
    inserts = []
    for col in columns:
        if col.name not in obj:
            inserts.append("NULL")
        else:
            inserts.append(col.insert_str_for_val(obj[col.name]))

    return "(" + ", ".join(inserts) + ")"



