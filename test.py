import os
import sys
import logging
from os import path
import parsetools
from psycopg2 import connect, DatabaseError

# --- Enter Database settings here ---
db_settings = {
    'database': 'test',
    'user': 'postgres'
}


def what_to_do(db_con, db_cur):
    # --- Insert your method calls here ---
    snapshot_dir = "/test_data"
    statements = parsetools.snapshot_dump_from_dir(current_path + snapshot_dir)
    print(statements)
    db_cur.execute(statements)
    db_con.commit()

#

if __name__ == "__main__":
    dir = path.dirname(path.abspath(__file__))
    os.chdir(dir)
    current_path = os.getcwd()
    print("Changed working directory to: %s\n" % current_path)

    con = None
    try:
        con = connect(database=db_settings['database'], user=db_settings['user'])
        what_to_do(con, con.cursor())
    except DatabaseError as e:
        if con:
            con.rollback()
        logging.error(e.message)
        sys.exit(1)
    finally:
        if con:
            con.close()
