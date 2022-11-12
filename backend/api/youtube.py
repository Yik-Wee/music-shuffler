'''
References
------
https://developers.google.com/youtube/v3/getting-started#etags
https://stackoverflow.com/questions/36557579/how-do-i-use-etags-for-youtube-v3-data-api
https://stackoverflow.com/a/65281317
https://developers.google.com/youtube/v3/docs/playlists/list
'''

from typing import List, Optional, Union
import requests
from .base import PlatformApi, Playlist, PlaylistInfo, Track


def choose_thumbnail(all_thumbnails: dict, priority: Optional[List[str]] = None) -> str:
    if priority is None:
        priority = ['standard', 'default']

    # try each key in order of its priority
    for key in priority:
        thumbnail = all_thumbnails.get(key)
        if thumbnail is not None:
            thumbnail_url = thumbnail['url']
            return thumbnail_url

    return ''


class YouTubeApi(PlatformApi):
    def __init__(self, api_key: str) -> None:
        '''
        Params
        ------
        `api_key`
        - The YouTube API key to send requests to the YouTube API.
          Read https://developers.google.com/youtube/v3/getting-started if you do not have one.
        '''
        super().__init__(platform='YOUTUBE')
        self.api_key = api_key

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        # https://developers.google.com/youtube/v3/docs/playlistItems/list#usage
        playlist_id = playlist_id.strip()

        url = 'https://www.googleapis.com/youtube/v3/playlistItems'\
            f'?part=snippet&maxResults=50&playlistId={playlist_id}&key={self.api_key}'

        s = requests.Session()

        response = s.get(url, timeout=30)
        if not response.ok:
            print(f'Error fetching playlist items for playlist {playlist_id}: {response.reason}')
            return None

        result = None
        try:
            result = response.json()
        except requests.JSONDecodeError as err:
            print(err)
            return None

        next_page_token = result.get('nextPageToken')
        length = result['pageInfo']['totalResults']
        tracks: List[Track] = []

        items = result['items']
        for item in items:
            all_thumbnails = item['snippet']['thumbnails']
            thumbnail = choose_thumbnail(all_thumbnails)

            track = {
                'track_id': item['id'],
                'platform': self.platform,
                'title': item['snippet']['title'],
                'owner': item['snippet']['channelTitle'],
                'thumbnail': thumbnail,
                # getting duration of video requires another API call which would increase
                # quota usage by n number of videos
                'duration_seconds': None,
            }
            tracks.append(track)

        while next_page_token:
            response = s.get(f'{url}&pageToken={next_page_token}', timeout=30)
            if not response.ok:
                print(
                    f'Error fetching playlist items for playlist {playlist_id}: {response.reason}')
                return None

            result = None
            try:
                result = response.json()
            except requests.JSONDecodeError as err:
                print(err)
                return None

            items = result['items']
            for item in items:
                all_thumbnails = item['snippet']['thumbnails']
                thumbnail = choose_thumbnail(all_thumbnails)

                track = {
                    'track_id': item['id'],
                    'platform': self.platform,
                    'title': item['snippet']['title'],
                    'owner': item['snippet']['channelTitle'],
                    'thumbnail': thumbnail,
                    # getting duration of video requires another API call which would increase
                    # quota usage by n number of videos
                    'duration_seconds': None,
                }
                tracks.append(track)

            next_page_token = result.get('nextPageToken')

        if playlist_info is None:
            playlist_info = self.playlist_info(playlist_id)

        playlist_ = {
            **playlist_info,
            'length': length,
            'tracks': tracks,
        }
        
        return playlist_

    def playlist_info(self, playlist_id: str) -> Union[PlaylistInfo, None]:
        '''
        Strips the `playlist_id` of leading/trailing whitespace before requesting the playlist info

        Returns
        ------
        - `None` if not found or error, `PlaylistInfo` if successful
        '''
        playlist_id = playlist_id.strip()
        url = 'https://www.googleapis.com/youtube/v3/playlists'\
            f'?part=snippet&id={playlist_id}&key={self.api_key}'
        response = requests.get(url, timeout=30)  # timeout 30 seconds
        if not response.ok:
            print(f'Error fetching etag for playlist {playlist_id}: {response.reason}')
            return None

        result = None
        try:
            result = response.json()
        except requests.JSONDecodeError as err:
            print(err)
            return None

        # https://developers.google.com/youtube/v3/docs/playlists#resource
        items = result['items']
        # playlist_id not found so no resource items in response
        if len(items) == 0:
            return None

        playlist_resource = items[0]
        etag = playlist_resource['etag']
        playlist_id = playlist_resource['id']

        snippet = playlist_resource['snippet']
        title = snippet['title']
        description = snippet['description']
        owner = snippet['channelTitle']

        all_thumbnails = snippet['thumbnails']
        thumbnail = choose_thumbnail(all_thumbnails)

        info = {
            'platform': self.platform,
            'playlist_id': playlist_id,
            'title': title,
            'owner': owner,
            'description': description,
            'thumbnail': thumbnail,
            'etag': etag,
        }
        return info
