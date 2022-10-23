# import os as __os
import sqlite3
from .storage import *


# BACKEND_FOLDER = __os.path.dirname(__os.path.realpath(__file__))
# DB_PATH = __os.path.join(BACKEND_FOLDER, 'music_cache.db')
# SCHEMA_PATH = __os.path.join(BACKEND_FOLDER, 'schema.sql')


class __DbInitialiser:
    is_created = False

    @classmethod
    def create_database(cls, db_path: str = DB_PATH):
        if cls.is_created:
            return

        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f, sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.executescript(f.read())
            conn.commit()
            cls.is_created = True


def create_database(db_path: str = DB_PATH):
    '''Creates the database `db_path` with tables from `schema.sql` if they don't already exist'''
    __DbInitialiser.create_database(db_path)
