'''
References
------
https://developers.google.com/youtube/v3/getting-started#etags
https://stackoverflow.com/questions/36557579/how-do-i-use-etags-for-youtube-v3-data-api
https://stackoverflow.com/a/65281317
https://developers.google.com/youtube/v3/docs/playlists/list
'''

from typing import Union
import requests
from .base import PlatformApi, Playlist


class YouTubeApi(PlatformApi):
    def __init__(self, api_key: str) -> None:
        super().__init__(base_url='https://www.youtube.com')
        self.api_key = api_key

    def playlist(self, playlist_id: str) -> Union[Playlist, None]:
        platform = 'YOUTUBE'
        return {
            'platform': platform,
            'playlist_id': playlist_id,
            'title': 'youtube playlist title',
            'owner': 'playlist owner',
            'description': 'cool epic poggers description\nCOGGERS',
            'thumbnail': 'playlist thumbnail',
            'length': 'playlist length',
            'etag': 'ABCD',
            'tracks': [
                {
                    'track_id': 'v_oUn9lKN-o3=',
                    'platform': platform,
                    'title': 'COOL TITLE',
                    'owner': 'pp',
                    'thumbnail': 'ytimg.something/something',
                    'duration_seconds': 100,
                },
                {
                    'track_id': 'vnFio9283bFW_as-n',
                    'platform': platform,
                    'title': 'WENDY\'S *NEW* RICK \'N MORTY BURGER REVIEW',
                    'owner': 'review brah',
                    'thumbnail': 'ytimg something 2',
                    'duration_seconds': 611,
                },
            ],
        }

    def etag(self, playlist_id: str) -> Union[str, None]:
        return 'ABCD'
