'''
References
------
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
'''

from typing import List, Optional, Union
from .base import PlatformApi, Playlist, PlaylistInfo, Track, try_json
import requests
import base64
from datetime import datetime, timedelta
import time
from enum import Enum


def validate_id(spotify_id: str) -> bool:
    # is base 62 without whitespace (is alphanumeric)
    return spotify_id.isalnum()


def _extract_thumbnail(images: List[dict]) -> str:
    if len(images) == 0:
        return ''

    image_obj = images[0]
    if not isinstance(image_obj, dict):
        return ''

    image = image_obj.get('url', '')
    return image


class ResponseStatus(Enum):
    OK = 0
    NOT_FOUND = 1
    UNRECOVERABLE = 2


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

        debug_info = '[SpotifyCredentialManager.get_token()]'
        if not res.ok:
            print(f'{debug_info} Spotify API responsded with error {res.status_code}: {res.text}')
            return ''

        result = try_json(res)
        if result is None:
            print(f'{debug_info} Response was not json: {res.text}')
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

    def __fetch_endpoint(self, endpoint: str) -> requests.Response:
        debug_info = '[SpotifyApi._fetch_playlist_info_endpoint()]'
        token = self.credentials.get_token()
        if not token:
            print(f'{debug_info} Something went wrong fetching access token')
            return None

        # url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        res = requests.get(endpoint, headers=headers, timeout=30)
        return res

    def __extract_tracks_from(self, items: List[dict], is_album: bool = False, album_cover_url: str = '') -> List[Track]:
        tracks = []

        for item in items:
            if is_album:
                track_data = item
                thumbnail = album_cover_url
            else:
                track_data = item.get('track', {})
                # track thumbnail is its album art
                album = track_data.get('album', {})
                images = album.get('images', [])
                thumbnail = _extract_thumbnail(images)

            track_id = track_data.get('id')
            duration_secs = track_data.get('duration_ms', -1000) // 1000
            artists = track_data.get('artists', [])
            owner_names = ', '.join(map(lambda x: x.get('name', ''), artists))
            name = track_data.get('name', '')

            tracks.append(
                Track(
                    track_id=track_id,
                    platform=self.platform,
                    title=name,
                    owner=owner_names,
                    thumbnail=thumbnail,
                    duration_seconds=duration_secs,
                )
            )

        return tracks

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlists-tracks
        playlist_id = playlist_id.strip()
        if not validate_id(playlist_id):
            return None

        debug_info = '[SpotifyApi.playlist()]'

        limit = 50

        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}'
        res = self.__fetch_endpoint(url)
        status = self.__handle_status_codes(res)
        if status == ResponseStatus.UNRECOVERABLE:
            return None

        if status == ResponseStatus.NOT_FOUND:
            # try album
            return self.album(playlist_id, playlist_info)

        result = try_json(res)
        if not result or not isinstance(result, dict):
            print(f'{debug_info} Response body contained invalid or unexpected JSON: {result}')
            return None

        items = result.get('items')
        tracks = self.__extract_tracks_from(items)

        encountered_unexpected_error = False
        url = result.get('next')

        while url and not encountered_unexpected_error:
            res = self.__fetch_endpoint(url)
            status = self.__handle_status_codes(res)
            if status != ResponseStatus.OK:
                encountered_unexpected_error = True

            result = try_json(res)
            if not result or not isinstance(result, dict):
                print(f'{debug_info} Response body contained invalid or unexpected JSON: {result}')
                encountered_unexpected_error = True

            items = result.get('items')
            tracks.extend(self.__extract_tracks_from(items))
            url = result.get('next')

        if not playlist_info:
            playlist_info = self.playlist_info(playlist_id)

        return Playlist(**playlist_info, tracks=tracks)

    def __handle_status_codes(self, res: requests.Response, __max_retries=3, __retries=0) -> int:
        if __retries >= __max_retries:
            return ResponseStatus.UNRECOVERABLE

        url = res.url
        print(f'Handling response from {url}: {res}')

        if res.status_code == 401:
            # expired token. generate new token
            print('Bad or expired token. Retrying with a new token')
            res = self.__fetch_endpoint(url)

        if res.status_code == 400:
            # invalid ID/bad request
            error_obj = try_json(res)

            if error_obj is None or not isinstance(error_obj, dict) or error_obj.get('error') is None:
                print('Bad request')
            else:
                error_msg = error_obj.get('error').get('message', '(no details provided by API response)')
                print(f'Bad request: {error_msg}')
            return ResponseStatus.UNRECOVERABLE

        if res.status_code == 403:
            # Bad OAuth request. This shouldn't happen
            print('Bad OAuth request (wrong consumer key, bad nonce, expired timestamp...)')
            return ResponseStatus.UNRECOVERABLE

        if res.status_code == 429:
            # Too many requests
            retry_after = res.headers.get('Retry-After', 15)
            print(f'Rate limit exceeded (too many requests). Retrying in {retry_after}s...')
            time.sleep(retry_after)
            res = self.__fetch_endpoint(url)
            # recursively handle the response up to the specified number of __max_retries
            return self.__handle_status_codes(res, __max_retries, __retries+1)

        if res.status_code == 404:
            # not found
            print('Not found')
            return ResponseStatus.NOT_FOUND

        # https://developer.spotify.com/documentation/web-api/#response-status-codes
        if res.status_code == 500:
            # internal server error
            print('Spotify API encountered an internal server error')
            return ResponseStatus.UNRECOVERABLE

        if res.status_code == 502:
            print('Spotify API encounrered a Bad Gateway')
            return ResponseStatus.UNRECOVERABLE

        if res.status_code == 503:
            print('Spotify API temporarily unavailable')
            return ResponseStatus.UNRECOVERABLE

        if not res.ok:
            print(f'Spotify API (endpoint {url}) responded with status {res.status_code}: {res.text}')
            return ResponseStatus.UNRECOVERABLE

        return ResponseStatus.OK

    def playlist_info(self, playlist_id: str) -> Union[str, None]:
        # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
        playlist_id = playlist_id.strip()
        if not validate_id(playlist_id):
            return None

        debug_info = '[SpotifyApi.playlist_info()]'
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        res = self.__fetch_endpoint(url)

        status = self.__handle_status_codes(res)
        if status == ResponseStatus.UNRECOVERABLE:
            return None

        if status == ResponseStatus.NOT_FOUND:
            # playlist not found. Try album
            print(f'{debug_info} /playlist/{playlist_id} not found. Trying with album endpoint')
            return self.album_info(playlist_id)

        result = try_json(res)
        if not result or not isinstance(result, dict):
            print(f'{debug_info} Response body contained invalid or unexpected JSON: {result}')
            return None

        description = result.get('description', '')
        playlist_id = result.get('id')
        # thumbnail urls are temporary
        images = result.get('images', [])
        thumbnail = _extract_thumbnail(images)
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

    def album(self, album_id: str, album_info: Optional[PlaylistInfo] = None) -> Playlist:
        album_id = album_id.strip()
        if not validate_id(album_id):
            return None

        if not album_info:
            album_info = self.album_info(album_id)

        thumbnail = album_info['thumbnail']

        debug_info = '[SpotifyApi.playlist()]'
        limit = 50

        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?limit={limit}'
        res = self.__fetch_endpoint(url)
        status = self.__handle_status_codes(res)
        if status != ResponseStatus.OK:
            return None

        result = try_json(res)
        if not result or not isinstance(result, dict):
            print(f'{debug_info} Response body contained invalid or unexpected JSON: {result}')
            return None

        items = result.get('items')
        tracks = self.__extract_tracks_from(items, is_album=True, album_cover_url=thumbnail)

        encountered_unexpected_error = False
        url = result.get('next')

        while url and not encountered_unexpected_error:
            res = self.__fetch_endpoint(url)
            status = self.__handle_status_codes(res)
            if status != ResponseStatus.OK:
                encountered_unexpected_error = True

            result = try_json(res)
            if not result or not isinstance(result, dict):
                print(f'{debug_info} Response body contained invalid or unexpected JSON: {result}')
                encountered_unexpected_error = True

            items = result.get('items')
            tracks.extend(self.__extract_tracks_from(items, is_album=True, album_cover_url=thumbnail))
            url = result.get('next')

        return Playlist(**album_info, tracks=tracks)

    def album_info(self, album_id: str) -> PlaylistInfo:
        '''
        Used as a fallback for `playlist_info`. If album is not found, this will not check
        if the `album_id` is really a `playlist_id`.
        '''
        album_id = album_id.strip()
        if not validate_id(album_id):
            return None

        debug_info = '[SpotifyApi.album_info()]'
        url = f'https://api.spotify.com/v1/albums/{album_id}'
        res = self.__fetch_endpoint(url)

        status = self.__handle_status_codes(res)
        if status == ResponseStatus.UNRECOVERABLE:
            return None

        if status == ResponseStatus.NOT_FOUND:
            print(f'{debug_info} /album/{album_id} not found')
            return None

        result = try_json(res)
        if not result or not isinstance(result, dict):
            print(f'{debug_info} Response body contained invalid or unexpected JSON: {result}')
            return None

        total_tracks = result.get('total_tracks', -1)
        album_id = result.get('id')
        # thumbnail image urls are temporary
        images = result.get('images', [])
        thumbnail = _extract_thumbnail(images)
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
