# https://stackoverflow.com/questions/30964214/how-to-get-each-track-of-a-playlist-with-the-soundcloud-api

from typing import List, Optional, Union
import re
import time
import json
import requests
from datetime import datetime, timedelta
from .base import (
    PlatformApi,
    Playlist,
    PlaylistInfo,
    Track,
    into_track,
    into_playlist,
    into_playlist_info
)


class SoundCloudV2TrackResponse:
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
        return None not in (self.track_id, self.title, self.thumbnail, self.owner)

    def into_track(self) -> Track:
        return into_track(
            self.track_id,
            'SOUNDCLOUD',
            self.title,
            self.owner,
            self.thumbnail,
            self.duration_secs
        )


def fetch_tracks(
    track_ids: List[str],
    client_id: str,
    session: Optional[requests.Session] = None,
    retry_sleep_secs: int = 2,
    max_retries: int = 5,
) -> List[Track]:
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
    # res = requests.get(endpoint, timeout=30, headers=headers)
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
        track_res = SoundCloudV2TrackResponse(track_info)
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

        print('fetch client_id')
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

            playlist_info = into_playlist_info(
                self.platform,
                playlist_id,
                title,
                owner,
                description,
                thumbnail,
                last_modified,
                playlist_length,
            )

        all_tracks: List[Track] = []
        remaining_track_ids = []

        for track_data in track_data_list:
            extracted_track_data = SoundCloudV2TrackResponse(track_data)
            if extracted_track_data.has_required_track_info():
                track = extracted_track_data.into_track()
                all_tracks.append(track)
            else:
                remaining_track_ids.append(extracted_track_data.track_id)

        # TODO Use multithreading
        print(f'Prerendered {len(all_tracks)} tracks')
        print(f'Fetching {len(remaining_track_ids)} tracks')
        if len(remaining_track_ids) > 0:
            idx = 0
            tracks_per_req = 50
            while idx < len(remaining_track_ids):
                track_ids = remaining_track_ids[idx:idx+tracks_per_req]
                print(f'fetch track_ids idx {idx} to {idx+tracks_per_req}')
                all_tracks.extend(
                    fetch_tracks(track_ids, self.get_client_id(), s)
                )
                idx += tracks_per_req

        playlist = into_playlist(playlist_info, all_tracks)
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

        playlist_info = into_playlist_info(
            self.platform,
            playlist_id,
            title,
            owner,
            description,
            thumbnail,
            last_modified,
            playlist_length,
        )
        return playlist_info
