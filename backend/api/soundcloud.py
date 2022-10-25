# https://stackoverflow.com/questions/30964214/how-to-get-each-track-of-a-playlist-with-the-soundcloud-api

from typing import Optional, Union
from .base import PlatformApi, Playlist, PlaylistInfo


class SoundCloudApi(PlatformApi):
    def __init__(self) -> None:
        super().__init__(platform='SOUNDCLOUD')

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        pass

    def playlist_info(self, playlist_id: str) -> Union[str, None]:
        pass
