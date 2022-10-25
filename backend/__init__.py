import sqlite3
from typing import TypedDict
from .storage import *


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


def clear_database(db_path: str = DB_PATH):
    '''Clears the entire database file'''
    with open(db_path, 'wb') as _:
        pass


class CollectionDict(TypedDict):
    Playlist: PlaylistCollection
    PlaylistTracks: PlaylistTracksCollection
    Track: TrackCollection


colls: CollectionDict = {
    'Playlist': PlaylistCollection(),
    'PlaylistTracks': PlaylistTracksCollection(),
    'Track': TrackCollection(),
}
