from typing import Union
from .base import PlatformApi, Playlist

class SpotifyApi(PlatformApi):
    def __init__(self) -> None:
        super().__init__(base_url='oiwefobwofeboerf')

    def playlist(self, playlist_id: str) -> Union[Playlist, None]:
        pass

    def etag(self, playlist_id: str) -> Union[str, None]:
        return super().etag(playlist_id)
