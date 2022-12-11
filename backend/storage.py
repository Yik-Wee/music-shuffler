import os as __os
import sqlite3
from typing import Any, List, Optional, Union, Callable
from .storage_result import Ok, Err, Result


BACKEND_FOLDER = __os.path.dirname(__os.path.realpath(__file__))
DB_PATH = __os.path.join(BACKEND_FOLDER, 'music_cache.db')
SCHEMA_PATH = __os.path.join(BACKEND_FOLDER, 'schema.sql')


class Column:
    '''
    Attributes
    ------
    `column_name`
      - The name of the table's column
    `default`
      - The default value for the column if not specified
    `is_required`
      - Whether the column requires a value
    '''

    def __init__(self, column_name: str, default=None, is_required: bool = True):
        self.column_name = column_name
        self.default = default
        self.is_required = is_required

    def __repr__(self) -> str:
        return f'Column({self.column_name}, default={self.default}, is_required={self.is_required})'

    def __str__(self) -> str:
        return self.column_name


class Collection:
    '''
    Attributes
    ------
    `columns`
      - Class attribute. Specifies the table's `Column`s
    `db_path`
      - The path to database. `DB_PATH` by default.
    '''
    columns: List[Column] = []

    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path

    @classmethod
    def validate(cls, record: dict) -> Result:
        '''
        Params
        ------
        `record`
          - the record to validate, containing keys corresponding to the columns of the Playlist
            table. Adds default values to columns if not provided

        Return
        ------
        `bool` 
          - `True` if record is valid, `False` otherwise
        '''

        valid_column_count = 0

        for column in cls.columns:
            # populate the record with the missing columns
            if column.column_name not in record:
                # required columns cannot be empty so they cannot be
                # populated with the default (empty) value
                if not column.is_required:
                    record[column.column_name] = column.default
                    valid_column_count += 1
                else:
                    return Err(f'Invalid record. key `{column}` is required')
            else:
                valid_column_count += 1

        if valid_column_count < len(record):
            return Err('Invalid record. Too many columns')
        return Ok(True)

    def try_execute(
        self,
        sql: str,
        values: Union[list, dict],
        commit: bool = True,
        cursor_callback: Optional[Callable[[sqlite3.Cursor], Any]] = None
    ) -> Result:
        '''
        Params
        ------
        `sql`
          - The SQL code to execute
        `values`
          - The parameterised values as a `list` or `dict`
        `commit`
          - Default `True`. Whether to commit the transaction
        `cursor_callback`
          - The callback funcion to decide what to be returned from the cursor
        '''
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('PRAGMA foreign_keys = ON;')
                cur.execute(sql, values)
                if commit:
                    conn.commit()

                if cursor_callback is not None:
                    results = cursor_callback(cur)
                    return Ok(results)
        except sqlite3.Error as err:
            return Err(err)
        return Ok()

    def try_executemany(
        self,
        sql: str,
        seq_of_values: List[Union[list, dict]],
        commit: bool = True,
        cursor_callback: Optional[Callable[[sqlite3.Cursor], Any]] = None,
    ) -> Result:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute('PRAGMA foreign_keys = ON;')
                cur.executemany(sql, seq_of_values)
                if commit:
                    conn.commit()

                if cursor_callback is not None:
                    results = cursor_callback(cur)
                    return Ok(results)
        except sqlite3.Error as err:
            return Err(err)
        return Ok()

    def insert(self, record: dict) -> Result:
        '''
        Params
        ------
        `record`
          - the record to insert, containing keys corresponding to the columns of the table

        Return
        ------
        `Result`
          - `Ok(None)` if successfully inserted record, `Err(error)` otherwise
        '''
        raise NotImplementedError()

    def delete(self, record: Union[dict, str]) -> Result:
        raise NotImplementedError()

    def find(self, record: Union[dict, str]) -> Result:
        raise NotImplementedError()


class PlaylistCollection(Collection):
    '''
    Interface for the Playlist table
    '''

    columns = [
        Column('PlaylistID'),
        Column('Title'),
        Column('Owner'),
        Column('Description', default='', is_required=False),
        Column('Thumbnail', default='', is_required=False),
        Column('Length'),
        Column('Etag', is_required=False),
        Column('Platform'),
    ]

    def insert(self, record: dict) -> Result:
        '''
        Params
        ------
        `record`
        - The record to insert. Must have exactly the `columns`:
            - PlaylistID, Title, Owner, Description, Thumbnail, Length, Etag, Platform

        Returns
        ------
        - `Err(validation_err_msg)` if record is invalid
        - `Err(sqlite3.Error)` if record insertion fails
        - `Ok(None)` if insertion is successful
        '''
        # validate record
        validation_result = self.validate(record)
        if not validation_result.ok:
            return validation_result

        result = self.try_execute('''
            INSERT INTO Playlist (PlaylistID, Title, Owner, Description, Thumbnail, Length, Etag, Platform)
            VALUES (:PlaylistID, :Title, :Owner, :Description, :Thumbnail, :Length, :Etag, :Platform)
        ''', record)
        return result

    def delete(self, record: Union[dict, str]) -> Result:
        '''
        Params
        ------
        `record`
          - filters the columns to delete, containing keys corresponding to the columns of the
            Playlist table. Only allow deletion of rows by PlaylistID and Platform columns.
            If record = '*', deletes everything from Playlist table
        '''

        if record == '*':
            result = self.try_execute('DELETE FROM Playlist;', ())
            return result

        playlist_id = record.get('PlaylistID')
        platform = record.get('Platform')
        if playlist_id is None or platform is None:
            return Err('Invalid filter (record). Both PlaylistID and Platform columns are required')

        # record contains both PlaylistID, Platform but also other invalid columns
        if len(record) > 2:
            return Err('Invalid filter (record). Too many invalid keys')

        result = self.try_execute('''
            DELETE FROM Playlist
            WHERE PlaylistID = ? AND Platform = ?;
        ''', (playlist_id, platform))
        return result

    def find(self, record: Union[dict, str]):
        '''
        Params
        ------
        `record`
          - The filter to match by. Only columns PlaylistID and Platform will be used as the filter and
            must be provided. Setting record = '*' fetches all data from the cache
        '''

        if record == '*':
            result = self.try_execute(
                'SELECT * FROM Playlist', (), cursor_callback=lambda cur: cur.fetchall())
            return result

        playlist_id = record.get('PlaylistID')
        platform = record.get('Platform')
        if playlist_id is None or platform is None:
            return Err('Invalid filter (record). Both PlaylistID and Platform columns are required')

        # record contains both PlaylistID, Platform but also other invalid columns
        if len(record) > 2:
            return Err('Invalid filter (record). Too many keys')

        result = self.try_execute('''
            SELECT * FROM Playlist
            WHERE PlaylistID = ? AND Platform = ?;
        ''', (playlist_id, platform), commit=False, cursor_callback=lambda cur: cur.fetchall())
        return result


class TrackCollection(Collection):
    '''
    Interface for the Track table.
    '''

    columns = [
        Column('TrackID'),
        Column('Platform'),
        Column('Title'),
        Column('Owner'),
        Column('Thumbnail', default='', is_required=False),
        Column('DurationSeconds', default=None, is_required=False),
    ]

    def insert(self, record: dict) -> Result:
        '''
        Params
        ------
        `record`
        - The record to insert. Performs INSERT OR IGNORE INTO Track ... insertion.
          must have the exact `columns`:
            - TrackID, Platform, Title, Owner, Thumbnail, DurationSeconds

        Returns
        ------
        - `Err(validation_err_msg)` if record is invalid
        - `Err(sqlite3.Error)` if record insertion fails
        - `Ok(None)` if insertion is successful
        '''
        # validate record
        validation_result = self.validate(record)
        if not validation_result.ok:
            return validation_result

        result = self.try_execute('''
            INSERT OR IGNORE INTO Track (TrackID, Platform, Title, Owner, Thumbnail, DurationSeconds)
            VALUES (:TrackID, :Platform, :Title, :Owner, :Thumbnail, :DurationSeconds)
        ''', record)
        return result

    def insertmany(self, list_of_records: List[dict]) -> Result:
        # validate records
        # for record in list_of_records:
        #     validation_result = self.validate(record)
        #     if not validation_result.ok:
        #         return validation_result

        result = self.try_executemany('''
            INSERT OR IGNORE INTO Track (TrackID, Platform, Title, Owner, Thumbnail, DurationSeconds)
            VALUES (:TrackID, :Platform, :Title, :Owner, :Thumbnail, :DurationSeconds)
        ''', list_of_records)
        return result

    def delete(self, record: Union[dict, str]) -> Result:
        '''
        Params
        ------
        `record`
          - filters the columns to delete, containing keys corresponding to the columns of the Track
            table. Only allow deletion of rows by TrackID and Platform columns.
            If record = '*', deletes everything from Playlist table
        '''

        if record == '*':
            result = self.try_execute('DELETE FROM Track;', ())
            return result

        track_id = record.get('TrackID')
        platform = record.get('Platform')
        if track_id is None or platform is None:
            return Err('Invalid filter (record). Both TrackID and Platform columns are required')

        # record contains both TrackID, Platform but also other invalid columns
        if len(record) > 2:
            return Err('Invalid filter (record). Too many keys')

        result = self.try_execute('''
            DELETE FROM Track
            WHERE TrackID = ? AND Platform = ?;
        ''', (track_id, platform))
        return result

    def find(self, record: Union[dict, str]):
        '''
        Params
        ------
        `record`
          - The filter to match by. Only columns TrackID and Platform will be used as the filter and
            must be provided. Setting record = '*' fetches all data from the cache
        '''

        if record == '*':
            result = self.try_execute(
                'SELECT * FROM Track;', (), commit=False, cursor_callback=lambda cur: cur.fetchall())
            return result

        track_id = record.get('TrackID')
        platform = record.get('Platform')
        if track_id is None or platform is None:
            return Err('Invalid filter (record). Both TrackID and Platform columns are required')

        # record contains both TrackID, Platform but also other invalid columns
        if len(record) > 2:
            return Err('Invalid filter (record). Too many keys')

        result = self.try_execute('''
            SELECT * FROM Track
            WHERE TrackID = ? AND Platform = ?;
        ''', (track_id, platform), commit=False, cursor_callback=lambda cur: cur.fetchall())
        return result


class PlaylistTracksCollection(Collection):
    '''
    Interface for PlaylistTracks table.
    '''

    columns = [
        Column('PlaylistID'),
        Column('TrackID'),
        Column('Platform'),
        Column('Position'),
    ]

    def insert(self, record: dict):
        '''
        Params
        ------
        `record`
        - The record to insert, containing the exact `columns`:
            - PlaylistID, TrackID, Platform, Position
        '''
        # validate record
        validation_result = self.validate(record)
        if not validation_result.ok:
            return validation_result

        result = self.try_execute('''
            INSERT INTO PlaylistTracks (PlaylistID, TrackID, Platform, Position)
            VALUES (:PlaylistID, :TrackID, :Platform, :Position)
        ''', record)
        return result

    def insertmany(self, list_of_records: List[dict]) -> Result:
        result = self.try_executemany('''
            INSERT INTO PlaylistTracks (PlaylistID, TrackID, Platform, Position)
            VALUES (:PlaylistID, :TrackID, :Platform, :Position)
        ''', list_of_records)

        if not result.ok:
            return result

        # update "Length" of Playlist table
        # PlaylistID and Platform should be consistent throughout all list_of_records
        # otherwise it would violate FK constraint & `Err()` result would have been returned
        playlist_id = list_of_records[0]['PlaylistID']
        platform = list_of_records[0]['Platform']

        result = self.try_execute('''
            UPDATE Playlist
            SET Length = (
                SELECT COUNT(*) AS Length
                FROM PlaylistTracks
                WHERE
                    PlaylistID = :PlaylistID AND
                    Platform = :Platform
            )
            WHERE PlaylistID = :PlaylistID AND Platform = :Platform;
        ''', {'PlaylistID': playlist_id, 'Platform': platform})
        return result

    def delete(self, record: Union[dict, str]) -> Result:
        '''
        Params
        ------
        `record`
          - filters the columns to delete, containing keys corresponding to the columns of the
            PlaylistTracks table. Only allow deletion of rows by PlaylistID and Platform columns.
            If record = '*', deletes everything from Playlist table
        '''

        if record == '*':
            result = self.try_execute('DELETE FROM PlaylistTracks;', ())
            return result

        playlist_id = record.get('PlaylistID')
        platform = record.get('Platform')
        if playlist_id is None or platform is None:
            return Err('Invalid filter (record). PlaylistID and Platform columns are required')

        # record contains both TrackID, Platform but also other invalid columns
        if len(record) > 2:
            return Err('Invalid filter (record). Too many keys')

        result = self.try_execute('''
            DELETE FROM PlaylistTracks
            WHERE PlaylistID = ? AND Platform = ?;
        ''', (playlist_id, platform))
        return result

    def find(self, record: Union[dict, str]):
        '''
        Params
        ------
        `record`
          - The filter to match by. Only column PlaylistID and Platform will be used as the filter
            and must be provided. Setting record = '*' fetches all data from the cache

        Returns
        ------
        - `Err(validation_err_msg)` if record is invalid
        - `Err(sqlite3.Error)` if record insertion fails
        - `Ok(records: List[sqlite3.Row])` if insertion is successful
            - each record contains the fields:
                - Position
                - PlaylistID, Platform, PlaylistTitle, PlaylistOwner, PlaylistDescription, PlaylistThumbnail, Length, Etag
                - TrackID, TrackPlatform, TrackTitle, TrackOwner, TrackThumbnail, DurationSeconds
        '''

        if record == '*':
            result = self.try_execute(
                'SELECT * FROM PlaylistTracks;', (), commit=False, cursor_callback=lambda cur: cur.fetchall())
            return result

        playlist_id = record.get('PlaylistID')
        platform = record.get('Platform')
        if playlist_id is None or platform is None:
            return Err('Invalid filter (record). Both PlaylistID and Platform columns are required')

        # record contains both PlaylistID, Platform but also other invalid columns
        if len(record) > 2:
            return Err('Invalid filter (record). Too many keys')

        result = self.try_execute('''
            SELECT
                PlaylistTracks.Position,

                Playlist.PlaylistID,                           Playlist.Platform AS "Platform",
                Playlist.Title AS "PlaylistTitle",             Playlist.Owner AS "PlaylistOwner",
                Playlist.Description AS "PlaylistDescription", Playlist.Thumbnail AS "PlaylistThumbnail",
                Playlist.Length,                               Playlist.Etag,

                Track.TrackID,                                 Track.Platform AS "TrackPlatform",
                Track.Title AS "TrackTitle",                   Track.Owner AS "TrackOwner",
                Track.Thumbnail AS "TrackThumbnail",           Track.DurationSeconds
            FROM PlaylistTracks
            INNER JOIN Playlist
            ON
                Playlist.PlaylistID = PlaylistTracks.PlaylistID
                AND Playlist.Platform = PlaylistTracks.Platform
            INNER JOIN Track
            ON
                Track.TrackID = PlaylistTracks.TrackID
                AND Track.Platform = PlaylistTracks.Platform
            WHERE Playlist.PlaylistID = ? AND Playlist.Platform = ?
            ORDER BY Position ASC;
        ''', (playlist_id, platform), commit=False, cursor_callback=lambda cur: cur.fetchall())
        return result
