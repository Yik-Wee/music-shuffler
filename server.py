# pylint: disable=missing-module-docstring
from typing import Dict
from flask import Flask, request, send_from_directory
from backend import (
    create_database,
    Collection,
    PlaylistCollection,
    TrackCollection,
    PlaylistTracksCollection
)

app = Flask(__name__)

colls: Dict[str, Collection] = {
    'Playlist': PlaylistCollection(),
    'PlaylistTracks': PlaylistTracksCollection(),
    'Track': TrackCollection(),
}


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>', methods=['GET'])
def index(path: str):
    '''Serves all files from frontend/public to /'''
    return send_from_directory('frontend/public', path)


# API routes
@app.route('/api/playlist/youtube', methods=['GET'])
def api():
    '''API endpoint for fetching YouTube playlist data'''
    playlist_id = request.args.get('id')
    # request YouTube API endpoint for playlist etag
    ...
    # compare with cache etag
    ...
    # different etag means playlist contents have changed
    # request for new playlist contents
    ...
    # same etag means playlist contents are unchanged
    # get playlist contents from cache
    ...
    # return playlist contents as JSON
    ...


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
