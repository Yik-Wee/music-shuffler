'''
The flask server for the music shuffler web app
'''
from flask import Flask, request, send_from_directory
from werkzeug.exceptions import NotFound
from backend import (
    create_database,
    colls
)
from backend.api import Playlist, Track
from platforms import platform_apis, ALL_PLATFORMS

BUILD_DIR = './frontend/build'
app = Flask(__name__)


def print_red(msg: str, **kwargs):
    '''Prints the `msg` in bold red for debugging'''
    print(f'\x1b[1;31m{msg}\x1b[0m', **kwargs)


def print_green(msg: str, **kwargs):
    '''Prints the `msg` in bold green for debugging'''
    print(f'\x1b[1;32m{msg}\x1b[0m', **kwargs)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>', methods=['GET'])
def index(path: str):
    '''Serves all files from frontend/public to /'''
    try:
        print(f'path = {path}')
        return send_from_directory(BUILD_DIR, path)
    except NotFound as _err:
        if not path.endswith('/'):
            path += '/'
        return send_from_directory(BUILD_DIR, path + 'index.html')


# API routes
@app.route('/api/playlist/<platform>', methods=['GET'])
def api_endpoint(platform: str):
    '''API endpoint for fetching playlist data'''
    if platform not in ALL_PLATFORMS:
        return {'error': f'Unsupported Platform {platform}'}, 404

    playlist_id = request.args.get('id')
    platform = platform.upper()
    api = platform_apis[platform]

    # request YouTube API endpoint for playlist etag
    etag = api.etag(playlist_id)

    # compare with cache etag
    if etag is not None:
        playlist_coll = colls['Playlist']
        record = {
            'PlaylistID': playlist_id,
            'Platform': platform
        }
        result = playlist_coll.find(record)
        if not result.ok:
            return {'error': f'Error fetching cached playlist\'s etag. {result.err()}'}, 500

        if len(result.value) == 0:
            cached_etag = None
        else:
            cached_record = result.value[0]
            cached_etag = cached_record['Etag']

        # same etag means playlist contents are unchanged
        # get playlist contents from cache
        if etag == cached_etag:
            playlist_tracks_coll = colls['PlaylistTracks']
            result = playlist_tracks_coll.find(record)
            if not result.ok:
                return {'error': f'Error fetching cached playlist. {result.err()}'}

            records = result.value
            if len(records) == 0:
                return {
                    'platform': platform,
                    'playlist_id': playlist_id,
                    'tracks': [],
                }

            playlist: Playlist = {
                'platform': platform,
                'playlist_id': playlist_id,
                'title': records[0]['PlaylistTitle'],
                'owner': records[0]['PlaylistOwner'],
                'description': records[0]['PlaylistDescription'],
                'thumbnail': records[0]['PlaylistThumbnail'],
                'length': records[0]['Length'],
                'etag': etag,
                'tracks': [],
            }

            for record in records:
                # PlaylistId, TrackID, Platform, Position
                track: Track = {
                    'track_id': record['TrackID'],
                    'platform': record['TrackPlatform'],
                    'title': record['TrackTitle'],
                    'owner': record['TrackOwner'],
                    'thumbnail': record['TrackThumbnail'],
                    'duration_seconds': record['DurationSeconds'],
                }
                playlist['tracks'].append(track)
            return playlist

    # etag is None or different etag means playlist contents have changed
    # request for new playlist contents
    playlist = api.playlist(playlist_id)
    if playlist is None:
        return {'error': f'Playlist with Playlist ID {playlist_id} not found'}

    # cache the new playlist
    playlist_coll = colls['Playlist']
    track_coll = colls['Track']
    playlist_tracks_coll = colls['PlaylistTracks']

    # delete the old cache
    res = playlist_tracks_coll.delete({
        'PlaylistID': playlist_id,
        'Platform': platform,
    })
    if not res.ok:
        print_red(
            f'Error deleting from PlaylistTracks (PlaylistID = {playlist_id}, Platform = {platform}): {res}'
        )
    else:
        print_green(f'Successfully deleted from PlaylistTracks (PlaylistID = {playlist_id}, Platform = {platform})')

    res = playlist_coll.delete({
        'PlaylistID': playlist_id,
        'Platform': platform,
    })
    if not res.ok:
        print_red(
            f'Error deleting from Playlist (PlaylistID = {playlist_id}, Platform = {platform}): {res}'
        )
    else:
        print_green(f'Successfully deleted from Playlist (PlaylistID = {playlist_id}, Platform = {platform})')

    # insert the new cache
    res = playlist_coll.insert({
        'PlaylistID': playlist_id,
        'Title': playlist['title'],
        'Owner': playlist['owner'],
        'Description': playlist['description'],
        'Thumbnail': playlist['thumbnail'],
        'Length': playlist['length'],
        'Etag': etag,
        'Platform': platform,
    })
    if not res.ok:
        print_red(f'Error inserting into Playlist (PlaylistID = {playlist_id}): {res}')
    else:
        print_green(f'Successfully inserted into Playlist (PlaylistID = {playlist_id})')

    for i, track in enumerate(playlist['tracks']):
        res = track_coll.insert({
            'TrackID': track['track_id'],
            'Platform': platform,
            'Title': track['title'],
            'Owner': track['owner'],
            'Thumbnail': track['thumbnail'],
            'DurationSeconds': track['duration_seconds']
        })
        if not res.ok:
            print_red(f'Error inserting into Track (TrackID = {track["track_id"]}): {res}')
        else:
            print_green(f'Successfully inserted into Track (TrackID = {track["track_id"]})')

        res = playlist_tracks_coll.insert({
            'PlaylistID': playlist_id,
            'TrackID': track['track_id'],
            'Platform': track['platform'],
            'Position': i,
        })
        if not res.ok:
            print_red(
                f'Error inserting into PlaylistTracks (PlaylistID = {playlist_id}, TrackID = {track["track_id"]}): ' \
                f'{res}'
            )
        else:
            print_green(
                'Successfully inserted into PlaylistTracks' \
                f'(PlaylistID = {playlist_id}, TrackID = {track["track_id"]})'
            )

    # return playlist contents as JSON
    return playlist


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
