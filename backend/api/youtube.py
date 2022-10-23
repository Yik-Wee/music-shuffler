'''
References
------
https://developers.google.com/youtube/v3/getting-started#etags
https://stackoverflow.com/questions/36557579/how-do-i-use-etags-for-youtube-v3-data-api
https://stackoverflow.com/a/65281317
https://developers.google.com/youtube/v3/docs/playlists/list
'''

from typing import Union
from .base import PlatformApi, Playlist


class YouTubeApi(PlatformApi):
    def __init__(self, api_key: str) -> None:
        super().__init__(base_url='https://www.youtube.com')
        self.api_key = api_key

    def playlist(self, playlist_id: str) -> Union[Playlist, None]:
        pass

    def etag(self, playlist_id: str) -> Union[str, None]:
        return super().etag(playlist_id)
