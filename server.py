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
from apis import platform_apis, ALL_PLATFORMS
from debug_utils import print_blue, print_green, print_red

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

@app.route('/api/playlist_info/<platform>', methods=['GET'])
def api_playlist_info(platform: str):
    '''Returns the info of the playlist without the tracks & length as a JSON response'''
    if platform not in ALL_PLATFORMS:
        return {'error': f'Unsupported Platform {platform}'}, 404

    playlist_id = request.args.get('id')

    if playlist_id is None:
        return {'error': 'No playlist ID provided'}, 404

    platform = platform.upper()
    api = platform_apis[platform]

    # resolve playlist_id to standardised playlist id (specifically for soundcloud)
    playlist_id = api.resolve_playlist_id(playlist_id)

    # check cache
    res = colls['Playlist'].find({
        'Platform': platform,
        'PlaylistID': playlist_id,
    })

    # found in cache
    if res.ok and len(res.value) == 1:
        playlist_info = res.value[0]
        print_blue(f'Found Playlist {playlist_info["Title"]} with PlaylistID {playlist_id} in cache')

        return {
            'platform': platform,
            'playlist_id': playlist_id,
            'title': playlist_info['Title'],
            'owner': playlist_info['Owner'],
            'description': playlist_info['Description'],
            'thumbnail': playlist_info['Thumbnail'],
            'etag': playlist_info['Etag'],
        }, 200

    # not found in cache, fetch from API and replace cache
    playlist_info = api.playlist_info(playlist_id)
    if playlist_info is None:
        return {'error': f'Playlist with Playlist ID {playlist_id} not found'}, 404

    colls['Playlist'].delete({
        'Platform': platform,
        'PlaylistID': playlist_id,
    })

    colls['Playlist'].insert({
        'PlaylistID': playlist_info['playlist_id'],
        'Title': playlist_info['title'],
        'Owner': playlist_info['owner'],
        'Description': playlist_info['description'],
        'Thumbnail': playlist_info['thumbnail'],
        'Length': playlist_info['length'],
        'Etag': playlist_info['etag'],
        'Platform': platform,
    })

    print_blue(f'Inserted {playlist_id} into Playlist cache')

    return playlist_info, 200


@app.route('/api/playlist/<platform>', methods=['GET'])
def api_full_playlist(platform: str):
    '''API endpoint for fetching playlist data'''
    if platform not in ALL_PLATFORMS:
        return {'error': f'Unsupported Platform {platform}'}, 404

    playlist_id = request.args.get('id')

    if playlist_id is None:
        return {'error': 'No playlist ID provided'}, 404

    platform = platform.upper()
    api = platform_apis[platform]
    playlist_id = api.resolve_playlist_id(playlist_id)

    # request API endpoint for playlist etag
    print_blue(
        f'({platform}) Fetching playlist_info(playlist_id={playlist_id})')
    playlist_info = api.playlist_info(playlist_id)

    # playlist does not exist
    if playlist_info is None:
        # delete the old cache e.g. if playlist became private/deleted
        res = colls['PlaylistTracks'].delete({
            'PlaylistID': playlist_id,
            'Platform': platform,
        })
        if not res.ok:
            print_red(
                'Error deleting from PlaylistTracks '
                f'(PlaylistID = {playlist_id}, Platform = {platform}): {res}')
        else:
            print_green(
                'Successfully deleted from PlaylistTracks '
                f'(PlaylistID = {playlist_id}, Platform = {platform})')

        res = colls['Playlist'].delete({
            'PlaylistID': playlist_id,
            'Platform': platform,
        })
        if not res.ok:
            print_red(
                'Error deleting from Playlist '
                f'(PlaylistID = {playlist_id}, Platform = {platform}): {res}')
        else:
            print_green(
                'Successfully deleted from Playlist '
                f'(PlaylistID = {playlist_id}, Platform = {platform})')

        return {'error': f'Playlist with Playlist ID {playlist_id} not found'}, 404

    etag = playlist_info.get('etag')

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
            cached_record = None
            cached_etag = None
            use_cache = False
        else:
            cached_record = result.value[0]
            cached_etag = cached_record['Etag']
            playlist_tracks_coll = colls['PlaylistTracks']
            result = playlist_tracks_coll.find(record)
            if not result.ok or len(result.value) == 0 and playlist_info['length'] != 0:
                use_cache = False
            else:
                # same etag means playlist contents are unchanged
                use_cache = etag == cached_etag

        # get playlist contents from cache
        if use_cache:
            print_blue(f'Matching etags: {etag}. Using cache')
            playlist_tracks_coll = colls['PlaylistTracks']
            result = playlist_tracks_coll.find(record)
            if not result.ok:
                return {'error': f'Error fetching cached playlist. {result.err()}'}

            records = result.value
            playlist: Playlist = {
                'platform': platform,
                'playlist_id': cached_record['PlaylistID'],
                'title': cached_record['Title'],
                'owner': cached_record['Owner'],
                'description': cached_record['Description'],
                'thumbnail': cached_record['Thumbnail'],
                'length': cached_record['Length'],
                'etag': etag,
                'tracks': [],
            }

            for record in records:
                # PlaylistID, TrackID, Platform, Position
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
    print_blue(f'({platform}) Fetching playlist(playlist_id={playlist_id})')
    playlist = api.playlist(playlist_id, playlist_info)
    if playlist is None:
        return {'error': f'Playlist with Playlist ID {playlist_id} not found'}, 404

    # cache the new playlist
    playlist_coll = colls['Playlist']
    track_coll = colls['Track']
    playlist_tracks_coll = colls['PlaylistTracks']

    # delete the old cache
    res = playlist_tracks_coll.delete({
        'PlaylistID': playlist['playlist_id'],
        'Platform': platform,
    })
    if not res.ok:
        print_red(
            'Error deleting from PlaylistTracks '
            f'(PlaylistID = {playlist_id}, Platform = {platform}): {res}')
    else:
        print_green(
            'Successfully deleted from PlaylistTracks '
            f'(PlaylistID = {playlist_id}, Platform = {platform})')

    res = playlist_coll.delete({
        'PlaylistID': playlist['playlist_id'],
        'Platform': platform,
    })
    if not res.ok:
        print_red(
            'Error deleting from Playlist '
            f'(PlaylistID = {playlist_id}, Platform = {platform}): {res}')
    else:
        print_green(
            'Successfully deleted from Playlist '
            f'(PlaylistID = {playlist_id}, Platform = {platform})')

    # insert the new cache
    res = playlist_coll.insert({
        'PlaylistID': playlist['playlist_id'],
        'Title': playlist['title'],
        'Owner': playlist['owner'],
        'Description': playlist['description'],
        'Thumbnail': playlist['thumbnail'],
        'Length': playlist['length'],
        'Etag': etag,
        'Platform': platform,
    })
    if not res.ok:
        print_red(
            'Error inserting into Playlist '
            f'(PlaylistID = {playlist_id}, Platform = {platform}): {res}')
    else:
        print_green(
            'Successfully inserted into Playlist '
            f'(PlaylistID = {playlist_id}, Platform = {platform})')

    tracks_to_insert = []
    playlist_tracks_to_insert = []
    for i, track in enumerate(playlist['tracks']):
        track_record = {
            'TrackID': track['track_id'],
            'Platform': platform,
            'Title': track['title'],
            'Owner': track['owner'],
            'Thumbnail': track['thumbnail'],
            'DurationSeconds': track['duration_seconds']
        }
        tracks_to_insert.append(track_record)

        playlist_track_record = {
            'PlaylistID': playlist['playlist_id'],
            'TrackID': track['track_id'],
            'Platform': track['platform'],
            'Position': i,
        }
        playlist_tracks_to_insert.append(playlist_track_record)

    res = track_coll.insertmany(tracks_to_insert)
    if not res.ok:
        print_red(f'Error inserting many into Track: {res}')
    else:
        print_green('Successfully inserted many into Track')

    playlist_tracks_coll.insertmany(playlist_tracks_to_insert)
    if not res.ok:
        print_red(
            f'Error inserting many into PlaylistTracks (PlaylistID = {playlist_id}): {res}')
    else:
        print_green(
            f'Successfully inserted many into PlaylistTracks (PlaylistID = {playlist_id})')

    # return playlist contents as JSON
    return playlist


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
