# https://developers.google.com/drive/api/v3/reference/files/list

from typing import List, Optional, Union
import requests
from .base import (
    PlatformApi,
    Playlist,
    PlaylistInfo,
    Track,
)

class SoundCloudApi(PlatformApi):
    def __init__(self) -> None:
        # https://www.googleapis.com/drive/v3
        super().__init__(platform='GOOGLE_DRIVE')

    def resolve_playlist_id(self, playlist_id: str) -> str:
        '''
        Resolves the playlist_id (playlist request path) into the canonical
        (standardised) request path

        Params
        ------
        `playlist_id`
        - ...
        '''
        pass

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
        - ...
        `playlist_info`
        - ...
        ...
        '''
        pass

    def playlist_info(self, playlist_id: str) -> Union[str, None]:
        pass
