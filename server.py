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
    api = platform_apis[platform]

    # request YouTube API endpoint for playlist etag
    etag = api.etag(playlist_id)

    # compare with cache etag
    if etag is not None:
        playlist_coll = colls['Playlist']
        record = {
            'PlaylistId': playlist_id,
            'Platform': platform.upper()
        }
        result = playlist_coll.find(record)
        if not result.ok:
            return {'error': f'Error fetching cached playlist\'s etag. {result.err()}'}, 500

        cached_record = result.value()[0]
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
                'title': records[0]['Playlist.Title'],
                'owner': records[0]['Playlist.Owner'],
                'description': records[0]['Playlist.Description'],
                'thumbnail': records[0]['Playlist.Thumbnail'],
                'length': records[0]['Playlist.Length'],
                'etag': etag,
                'tracks': [],
            }

            for record in records:
                # PlaylistId, TrackID, Platform, Position
                track: Track = {
                    'track_id': record['Track.TrackID'],
                    'platform': record['Track.Platform'],
                    'title': record['Track.Title'],
                    'owner': record['Track.Owner'],
                    'thumbnail': record['Track.Thumbnail'],
                    'duration_seconds': record['Track.DurationSeconds'],
                }
                playlist['tracks'].append(track)
            return playlist

    # etag is None or different etag means playlist contents have changed
    # request for new playlist contents
    playlist = api.playlist(playlist_id)
    if playlist is None:
        return {'error': f'Playlist with Playlist ID {playlist_id} not found'}

    # return playlist contents as JSON
    return playlist


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
