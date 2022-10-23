# https://stackoverflow.com/questions/30964214/how-to-get-each-track-of-a-playlist-with-the-soundcloud-api

from typing import Union
from .base import PlatformApi, Playlist


class SoundCloudApi(PlatformApi):
    def __init__(self) -> None:
        super().__init__(base_url='api.soundcloud.something i forgot')

    def playlist(self, playlist_id: str) -> Union[Playlist, None]:
        pass

    def etag(self, playlist_id: str) -> Union[str, None]:
        pass
