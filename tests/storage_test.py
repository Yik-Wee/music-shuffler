import json
import os
from typing import Dict
from backend import create_database, PlaylistCollection, PlaylistTracksCollection, TrackCollection, Collection

TESTS_FOLDER = os.path.dirname(os.path.realpath(__file__))
TESTS_DB_PATH = os.path.join(TESTS_FOLDER, 'test.db')

create_database(db_path=TESTS_DB_PATH)

colls: Dict[str, Collection] = {
    'Playlist': PlaylistCollection(TESTS_DB_PATH),
    'PlaylistTracks': PlaylistTracksCollection(TESTS_DB_PATH),
    'Track': TrackCollection(TESTS_DB_PATH),
}


def delete_all():
    for coll_name, coll in colls.items():
        delete_result = coll.delete('*')
        print(f'Deleted Column `{coll_name}`')
        print(f'\t{repr(delete_result)}')


def test_insertion():
    def test_insert_playlist(playlist_id: str, title: str, owner: str, length: int, platform: str):
        print(f'INSERT {playlist_id}')
        insert_result = colls['Playlist'].insert({
            'PlaylistID': playlist_id,
            'Title': title,
            'Owner': owner,
            'Length': length,
            'Platform': platform,
        })
        print(repr(insert_result))
        print()


    def test_insert_track(track_id: str, platform: str, title: str, owner: str, duration_seconds: int):
        print(f'INSERT {track_id}')
        insert_result = colls['Track'].insert({
            'TrackID': track_id,
            'Platform': platform,
            'Title': title,
            'Owner': owner,
            'DurationSeconds': duration_seconds,
        })
        print(repr(insert_result))
        print()


    def test_insert_playlist_tracks(playlist_id: str, track_id: str, platform: str, position: int):
        print(f'INSERT {playlist_id}, {track_id}')
        insert_result = colls['PlaylistTracks'].insert({
            'PlaylistID': playlist_id,
            'TrackID': track_id,
            'Platform': platform,
            'Position': position,
        })
        print(repr(insert_result))
        print()

    test_insert_playlist('PLA1', 'Epic Playlist A1', 'Epic Owner A1', 10, 'YOUTUBE')
    test_insert_track('V00001', 'YOUTUBE', 'EPIC TRACK 1', 'EPIC CHANNEL 1', 320)
    test_insert_track('V00002', 'YOUTUBE', 'Chill Ambience', 'Lofi Girl', 3600)
    test_insert_track('V00003', 'YOUTUBE', 'Anime girl ASMR to fall asleep to', 'ASMR channel', 530)
    test_insert_playlist_tracks('PLA1', 'V00001', 'YOUTUBE', 0)
    test_insert_playlist_tracks('PLA1', 'V00002', 'YOUTUBE', 1)
    test_insert_playlist_tracks('PLA1', 'V00003', 'YOUTUBE', 2)


# delete_all()
test_insertion()
all_playlists = colls['Playlist'].find('*')
all_tracks = colls['Track'].find('*')
all_playlist_tracks = colls['PlaylistTracks'].find('*')


def pretty_print(*args):
    '''Pretty print the list of objects *args'''
    for obj in args:
        if not obj.ok:
            print(obj)
        elif obj.value is None:
            print(None)
        else:
            # records = map(obj.value, dict)
            records = []
            for record in obj.value:
                records.append(dict(record))
            print(json.dumps(records, indent=2))
        print()


pretty_print(all_playlists, all_tracks, all_playlist_tracks)
