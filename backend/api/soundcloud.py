# https://stackoverflow.com/questions/30964214/how-to-get-each-track-of-a-playlist-with-the-soundcloud-api

from typing import List, Optional, Union
import re
import time
import json
import concurrent.futures
from datetime import datetime, timedelta
import requests
from .base import (
    PlatformApi,
    Playlist,
    PlaylistInfo,
    Track,
)


class SoundCloudV2TrackData:
    '''
    Utility class to extract track data from a soundcloud api-v2 response or
    a hydration track object
    '''
    def __init__(self, track_response: dict) -> None:
        self.track_id = str(track_response.get('id'))
        self.title = track_response.get('title')
        self.thumbnail = track_response.get('artwork_url')
        owner_data = track_response.get('user')
        if owner_data is not None:
            self.owner = owner_data.get('username', '')
        else:
            self.owner = ''
        duration_ms = track_response.get('duration')
        if duration_ms is not None and isinstance(duration_ms, int):
            self.duration_secs = duration_ms // 1000
        else:
            self.duration_secs = None

    def has_required_track_info(self):
        '''
        Returns
        ------
        `true` if the track data has the `track_id`, `title` and `owner` data, `false` otherwise
        '''
        return None not in (self.track_id, self.title, self.owner)

    def into_track(self) -> Track:
        '''
        Convert the extracted track data into `Track` dict
        '''
        return Track(
            track_id=self.track_id,
            platform='SOUNDCLOUD',
            title=self.title,
            owner=self.owner,
            thumbnail=self.thumbnail,
            duration_seconds=self.duration_secs,
        )


def fetch_tracks_parallel(
    track_ids: List[str],
    client_id: str,
    group_size: int = 50,
    threads: int = 8,
    session: Optional[requests.Session] = None,
    retry_sleep_secs: int = 2,
    max_retries: int = 5,
) -> List[Track]:
    '''
    Params
    ------
    `track_ids`
    - Track ids of all the tracks to fetch

    `client_id`
    - The client id obtained for the API call

    `group_size`
    - The size of each group of track ids. Each group will be fetched on separate threads
      (default `50`)

    `threads`
    - The number of threads to use (default `8`)

    `session`
    - The optional `Session` object to be used for GET requests.
      See https://requests.readthedocs.io/en/latest/user/advanced/

    `retry_sleep_secs`
    - The number of seconds to wait before retrying a failed request

    `max_retries`
    - The maximum number of retries of the failed request
    '''
    # split track ids into groups
    groups = []
    idx = 0
    while idx < len(track_ids):
        group = track_ids[idx:idx+group_size]
        groups.append(group)
        idx += group_size

    all_tracks = []

    # fetch each group of tracks on diff threads
    # https://medium.com/geekculture/python-how-to-send-100k-requests-quickly-b4ef9495620d
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = (
            executor.submit(
                fetch_tracks,
                group,
                client_id,
                session,
                retry_sleep_secs,
                max_retries
            ) for group in groups
        )
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                # concat the results in order of track position
                tracks = future.result()
                all_tracks.extend(tracks)
            except concurrent.futures.CancelledError as err:
                print(f'Future was cancelled: {err}')
            except concurrent.futures.TimeoutError as err:
                print(f'Future was timed out: {err}')
            except Exception as err:  # pylint: disable=broad-except
                print(f'An error occurred fetching tracks: {err}')

    return all_tracks


def fetch_tracks(
    track_ids: List[str],
    client_id: str,
    session: Optional[requests.Session] = None,
    retry_sleep_secs: int = 2,
    max_retries: int = 5,
) -> List[Track]:
    '''
    Warning
    ------
    If the number of track_ids is too large, an empty list `[]` will be returned as
    a 400 Bad Request response will be obtained. It is best to fetch a small number
    of `track_ids` (e.g. <50)

    Params
    ------
    `track_ids`
    - Track ids of all the tracks to fetch

    `client_id`
    - The client id obtained for the API call

    `session`
    - The optional `Session` object to be used for GET requests.
      See https://requests.readthedocs.io/en/latest/user/advanced/

    `retry_sleep_secs`
    - The number of seconds to wait before retrying a failed request

    `max_retries`
    - The maximum number of retries of the failed request
    '''
    if session is None:
        get = requests.get
    else:
        get = session.get

    ids = ','.join(track_ids)
    endpoint = f'https://api-v2.soundcloud.com/tracks?ids={ids}&client_id={client_id}'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.1',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'en-GB,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'api-v2.soundcloud.com',
        'Origin': 'https://soundcloud.com',
        'Referer': 'https://soundcloud.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        # including User-Agent prevents the need to retry due to 403 forbidden error
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    }
    res = get(endpoint, timeout=30, headers=headers)

    if not res.ok:
        # Error 403 forbidden occurs when too many requests are sent per unit time
        # (perhaps DoS protection). Retry after 5s. Max 3 retries
        retries = 0
        success = False

        while retries < max_retries and not success:
            print(f'retrying (sleeping {retry_sleep_secs}s)')
            time.sleep(retry_sleep_secs)
            print(f'retrying (number {retries+1})\n\t{endpoint}')

            res = get(endpoint, timeout=30, headers=headers)
            if not res.ok:
                retries += 1
            else:
                success = True

        if not success:
            print(f'Error {endpoint}', res.status_code, res.text, res.json())
            return []

    result = None
    try:
        result = res.json()
    except requests.JSONDecodeError as err:
        print(err)
        return []

    if not isinstance(result, list):
        return []

    tracks = []
    for track_info in result:
        track_res = SoundCloudV2TrackData(track_info)
        track = track_res.into_track()
        tracks.append(track)
    return tracks


class SoundCloudApi(PlatformApi):
    def __init__(self) -> None:
        super().__init__(platform='SOUNDCLOUD')
        self._client_id_expiry: datetime = datetime.min
        self._client_id: str = ''
        self._client_id = self.get_client_id()

    def get_client_id(self) -> str:
        # check cached client_id
        if self._client_id_expiry > datetime.now():
            print(f'use cached client_id: {self._client_id}')
            return self._client_id

        scripts_re = r'<script crossorigin src=\"(.+)\"><\/script>'
        res = requests.get('https://soundcloud.com', timeout=2)
        if not res.ok:
            return ''

        html = res.text
        script_urls = re.findall(scripts_re, html)
        if len(script_urls) == 0:
            return ''

        # https://github.com/zackradisic/soundcloud-api/blob/master/clientid.go
        # script exposing the client_id is the last script
        script_url = script_urls[-1]
        res = requests.get(script_url, timeout=2)
        if not res.ok:
            return ''

        # parse the js text for the client_id
        js_text = res.text
        js_re = r',client_id:"([^"]+)"'
        groups = re.findall(js_re, js_text)
        if len(groups) == 0:
            return ''

        client_id = groups[0]
        # set client_id expiry in case client id expires and no longer works
        # arbitrary - expires after 30 min
        self._client_id_expiry = datetime.now() + timedelta(minutes=30)
        return client_id

    def __parse_hydration(self, html: str) -> Union[dict, None]:
        html_re = r'__sc_hydration\s*=\s*(.*)\s*;'
        groups = re.findall(html_re, html)
        if len(groups) == 0:
            return None

        sc_hydration = json.loads(groups[0])
        idx_playlist = -1

        for i, obj in enumerate(sc_hydration):
            hydratable = obj.get('hydratable')
            if hydratable == 'playlist':
                idx_playlist = i
                break

        # was not a playlist/album url
        if idx_playlist == -1:
            return None

        playlist_data = sc_hydration[idx_playlist].get('data')
        return playlist_data

    def resolve_playlist_id(self, playlist_id: str) -> str:
        '''
        Resolves the playlist_id (playlist request path) into the canonical
        (standardised) request path

        Params
        ------
        `playlist_id`
        - The canonical_url (request path) of the soundcloud playlist
        '''
        info = self.playlist_info(playlist_id)
        # playlist not found - resolve to original playlist_id
        if info is None:
            return playlist_id

        return info['playlist_id']

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        '''
        https://stackoverflow.com/questions/20870270/how-to-get-soundcloud-embed-code-by-soundcloud-com-url/27461646#27461646

        Params
        -----
        `playlist_id`
        - The canonical_url (request path) of the soundcloud playlist
          e.g. `/uyn_yn/sets/uyuni-jellyfish`
        `playlist_info`
        - The `PlaylistInfo` to be appended to the returned `Playlist`. Setting to `None` will call
          `self.playlist_info()` and append the result to the returned `Playlist`.
        ...
        '''
        # prepare url endpoint
        if not playlist_id.startswith('/'):
            url = f'https://soundcloud.com/{playlist_id}'
        else:
            url = f'https://soundcloud.com{playlist_id}'

        s = requests.Session()
        response = s.get(url, timeout=5)
        # playlist private or not found
        if not response.ok:
            return None

        # parse the HTML for window.__sc_hydration
        playlist_data = self.__parse_hydration(response.content.decode('utf-8'))

        # validate playlist data parsed
        if playlist_data is None or not isinstance(playlist_data, dict):
            print(
                '[SoundCloudApi] no field / unusable field `data` in hydration object: ',
                json.dumps(playlist_data, indent=2)
            )
            return None

        # get track list from playlist data
        track_data_list = playlist_data.get('tracks')
        if track_data_list is None or not isinstance(track_data_list, list):
            print('[SoundCloudApi] No track data for this playlist could be parsed')
            return None

        # extract playlist info from parsed playlist data
        if not playlist_info:
            # standardised url is used as the playlist ID
            playlist_id = playlist_data.get('url')
            title = playlist_data.get('title')
            thumbnail = playlist_data.get('artwork_url')
            last_modified = playlist_data.get('last_modified')
            playlist_length = playlist_data.get('track_count', len(track_data_list))
            description = playlist_data.get('description')
            owner_data = playlist_data.get('user')
            if owner_data is not None:
                owner = owner_data.get('username', '')
            else:
                owner = ''

            playlist_info = PlaylistInfo(
                platform=self.platform,
                playlist_id=playlist_id,
                title=title,
                owner=owner,
                description=description,
                thumbnail=thumbnail,
                etag=last_modified,
                length=playlist_length,
            )

        all_tracks: List[Track] = []
        remaining_track_ids = []

        # extract prerendered track data
        for track_data in track_data_list:
            extracted_track_data = SoundCloudV2TrackData(track_data)
            if extracted_track_data.has_required_track_info():
                track = extracted_track_data.into_track()
                all_tracks.append(track)
            else:
                remaining_track_ids.append(extracted_track_data.track_id)

        # fetch remaining (non-prerendered) tracks in parallel
        if len(remaining_track_ids) > 0:
            tracks = fetch_tracks_parallel(
                remaining_track_ids, client_id=self.get_client_id(), session=s)
            all_tracks.extend(tracks)

        playlist = Playlist(**playlist_info, tracks=all_tracks)
        return playlist

    def playlist_info(self, playlist_id: str) -> Union[str, None]:
        # prepare url endpoint
        if not playlist_id.startswith('/'):
            url = f'https://soundcloud.com/{playlist_id}'
        else:
            url = f'https://soundcloud.com{playlist_id}'

        response = requests.get(url, timeout=5)

        # playlist private or not found
        if not response.ok:
            return None

        # parse the HTML for window.__sc_hydration
        playlist_data = self.__parse_hydration(response.text)

        # validate playlist data parsed
        if playlist_data is None or not isinstance(playlist_data, dict):
            print(
                '[SoundCloudApi] no field / unusable field `data` in hydration object: ',
                json.dumps(playlist_data, indent=2)
            )
            return None

        # get track list from playlist data
        track_data_list = playlist_data.get('tracks')
        if track_data_list is None or not isinstance(track_data_list, list):
            print('[SoundCloudApi] No track data for this playlist could be parsed')
            return None

        # extract playlist info from parsed playlist data
        # standardised url is used as the playlist ID
        playlist_id = playlist_data.get('url')
        title = playlist_data.get('title')
        thumbnail = playlist_data.get('artwork_url')
        last_modified = playlist_data.get('last_modified')
        playlist_length = playlist_data.get('track_count', len(track_data_list))
        description = playlist_data.get('description')
        owner_data = playlist_data.get('user')
        if owner_data is not None:
            owner = owner_data.get('username', '')
        else:
            owner = ''

        playlist_info = PlaylistInfo(
            platform=self.platform,
            playlist_id=playlist_id,
            title=title,
            owner=owner,
            description=description,
            thumbnail=thumbnail,
            etag=last_modified,
            length=playlist_length,
        )
        return playlist_info
