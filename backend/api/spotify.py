'''
References
------
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
'''

from typing import Optional, Union
from .base import PlatformApi, Playlist, PlaylistInfo
import requests


class SpotifyApi(PlatformApi):
    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(platform='SPOTIFY')
        self.client_id = client_id
        self.client_secret = client_secret

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        # requests.get('', headers={
        #     'Authorization': 
        # })
        pass

    def playlist_info(self, playlist_id: str) -> Union[str, None]:
        # ...
        return super().playlist_info(playlist_id)
