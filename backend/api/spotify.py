'''
References
------
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
'''

from typing import Optional, Union
from .base import PlatformApi, Playlist, PlaylistInfo, try_json
import requests
import base64
from datetime import datetime, timedelta
import time


def validate_id(spotify_id: str) -> bool:
    # is base 62 without whitespace (is alphanumeric)
    return spotify_id.isalnum()


class SpotifyCredentialManager:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._token = ''
        self._token_expiry = datetime.min

    def get_token(self) -> str:
        # use cached token if hasnt expired yet
        if self._token_expiry > datetime.now():
            print(f'[SpotifyApi] use cached token {self._token}')
            return self._token

        auth_bytes = f'{self._client_id}:{self._client_secret}'.encode('ascii')
        auth_b64_bytes = base64.b64encode(auth_bytes)
        auth_b64 = auth_b64_bytes.decode('ascii')

        res = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': 'Basic ' + auth_b64
            },
            data={
                'grant_type': 'client_credentials'
            },
            timeout=5,
        )

        debug_origin = '[SpotifyCredentialManager.get_token()]'
        if not res.ok:
            print(f'{debug_origin} Spotify API responsded with error {res.status_code}: {res.text}')
            return ''

        result = try_json(res)
        if result is None:
            print(f'{debug_origin} Response was not json: {res.text}')
            return ''

        access_token = result['access_token']
        expires_in = result['expires_in']
        # token_type = result['token_type']

        print(f'[SpotifyApi] fetched token: {access_token}. Expires in {expires_in}s')
        self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
        self._token = access_token
        return self._token


class SpotifyApi(PlatformApi):
    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(platform='SPOTIFY')
        self.credentials = SpotifyCredentialManager(client_id, client_secret)
        # self.client_id = client_id
        # self.client_secret = client_secret
        self.cached_token = None
        self.expires = None

    def _fetch_endpoint(self, endpoint: str) -> requests.Response:
        debug_origin = '[SpotifyApi._fetch_playlist_info_endpoint()]'
        token = self.credentials.get_token()
        if not token:
            print(f'{debug_origin} Something went wrong fetching access token')
            return None

        # url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        res = requests.get(endpoint, headers=headers, timeout=30)
        return res

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlists-tracks
        playlist_id = playlist_id.strip()
        if not validate_id(playlist_id):
            return None
        ...
        return ...

    def playlist_info(self, playlist_id: str) -> Union[str, None]:
        # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
        playlist_id = playlist_id.strip()
        if not validate_id(playlist_id):
            return None

        debug_origin = '[SpotifyApi.playlist_info()]'
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        res = self._fetch_endpoint(url)

        if res.status_code == 400:
            # invalid ID/bad request
            return None

        if res.status_code == 401:
            # expired token. generate new token
            res = self._fetch_endpoint(url)

        if res.status_code == 403:
            # Bad OAuth request. This shouldn't happen
            print(f'{debug_origin} Bad OAuth request (wrong consumer key, bad nonce, expired timestamp...)')
            return None

        if res.status_code == 429:
            # Too many requests
            retry_in_seconds = 15
            print(f'{debug_origin} Rate limit exceeded (too many requests). Retrying in {retry_in_seconds}s...')
            time.sleep(retry_in_seconds)
            res = self._fetch_endpoint(url)
            if not res.ok:
                print(f'{debug_origin} (after retry) API responded with status {res.status_code}: {res.text}')
                return None

        if res.status_code == 404:
            # playlist not found. Try album
            print(f'{debug_origin} /playlist/{playlist_id} not found. Trying with album endpoint')
            return self.album_info(playlist_id)

        if not res.ok:
            print(f'{debug_origin} API responded with status {res.status_code}: {res.text}')

        result = try_json(res)
        if not result or not isinstance(result, dict):
            print(f'{debug_origin} Response body contained invalid or unexpected JSON: {result}')
            return None

        description = result.get('description', '')
        playlist_id = result.get('id')
        # thumbnail urls are temporary
        thumbnail_obj = result.get('images', [''])[0]
        thumbnail = thumbnail_obj.get('url') if isinstance(thumbnail_obj, dict) else ''
        name = result.get('name')
        owner_obj = result.get('owner', {})
        owner = owner_obj.get('display_name', '')
        length = result.get('tracks', {}).get('total', -1)
        snapshot_id = result.get('snapshot_id')

        return PlaylistInfo(
            platform=self.platform,
            playlist_id=playlist_id,
            title=name,
            owner=owner,
            description=description,
            thumbnail=thumbnail,
            etag=snapshot_id,
            length=length,
        )

    def album(self, album_id: str) -> Playlist:
        album_id = album_id.strip()
        if not validate_id(album_id):
            return None
        ...
        pass

    def album_info(self, album_id: str) -> PlaylistInfo:
        '''
        Used as a fallback for `playlist_info`. If album is not found, this will not check
        if the `album_id` is really a `playlist_id`.
        '''
        album_id = album_id.strip()
        if not validate_id(album_id):
            return None

        debug_origin = '[SpotifyApi.album_info()]'
        url = f'https://api.spotify.com/v1/albums/{album_id}'
        res = self._fetch_endpoint(url)

        if res.status_code == 400:
            # invalid ID/bad request
            return None

        if res.status_code == 401:
            # expired token. generate new token
            res = self._fetch_endpoint(url)

        if res.status_code == 403:
            # Bad OAuth request. This shouldn't happen
            print(f'{debug_origin} Bad OAuth request (wrong consumer key, bad nonce, expired timestamp...)')
            return None

        if res.status_code == 429:
            # Too many requests
            print(f'{debug_origin} Rate limit exceeded (too many requests). Retrying in 10s...')
            time.sleep(10)
            res = self._fetch_endpoint(url)
            if not res.ok:
                print(f'{debug_origin} (after retry) API responded with status {res.status_code}: {res.text}')
                return None

        if res.status_code == 404:
            # playlist not found. Try album
            print(f'{debug_origin} /album/{album_id} not found')
            return None

        if not res.ok:
            print(f'{debug_origin} API responded with status {res.status_code}: {res.text}')

        result = try_json(res)
        if not result or not isinstance(result, dict):
            print(f'{debug_origin} Response body contained invalid or unexpected JSON: {result}')
            return None

        total_tracks = result.get('total_tracks', -1)
        album_id = result.get('id')
        # thumbnail image urls are temporary
        thumbnail_obj = result.get('images', [''])[0]
        thumbnail = thumbnail_obj.get('url') if isinstance(thumbnail_obj, dict) else ''
        name = result.get('name', '')
        artists = result.get('artists', [])
        owners = filter(lambda name: name is not None, map(lambda x: x.get('name'), artists))
        owners_string = ', '.join(owners)

        return PlaylistInfo(
            platform=self.platform,
            playlist_id=album_id,
            title=name,
            owner=owners_string,
            description='',
            thumbnail=thumbnail,
            # No etag provided for albums. Albums must be updated through distributors
            # https://community.spotify.com/t5/Ongoing-Issues/Change-Album-Cover-Art/idi-p/1421730
            etag=None,
            length=total_tracks,
        )
