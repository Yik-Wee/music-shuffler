from typing import Optional, Union
from .base import PlatformApi, Playlist, PlaylistInfo

class SpotifyApi(PlatformApi):
    def __init__(self) -> None:
        super().__init__(platform='SPOTIFY')

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        pass

    def playlist_info(self, playlist_id: str) -> Union[str, None]:
        return super().playlist_info(playlist_id)
