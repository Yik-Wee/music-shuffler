from typing import List, Optional, TypedDict, Union


class Track(TypedDict):
    '''
    ```
    {
        'track_id': str,
        'platform': str,
        'title': str,
        'owner': str,
        'thumbnail': str,
        'duration_seconds': int,
    }
    ```
    '''
    track_id: str
    platform: str
    title: str
    owner: str
    thumbnail: str
    duration_seconds: Union[int, None]


def into_track(
    track_id: str,
    platform: str,
    title: str,
    owner: str,
    thumbnail: str,
    duration_seconds: Optional[int] = None
) -> Track:
    return {
        'track_id': track_id,
        'platform': platform,
        'title': title,
        'owner': owner,
        'thumbnail': thumbnail,
        'duration_seconds': duration_seconds,
    }


class PlaylistInfo(TypedDict):
    '''
    ```
    {
        'platform': str,
        'playlist_id': str,
        'title': str,
        'owner': str,
        'description': str,
        'thumbnail': str,
        'etag': str,
        'length': int,
    }
    ```
    '''
    platform: str
    playlist_id: str
    title: str
    owner: str
    description: str
    thumbnail: str
    etag: str
    length: int


def into_playlist_info(
    platform: str,
    playlist_id: str,
    title: str,
    owner: str,
    description: str,
    thumbnail: str,
    etag: str,
    length: int
) -> PlaylistInfo:
    return {
        'platform': platform,
        'playlist_id': playlist_id,
        'title': title,
        'owner': owner,
        'description': description,
        'thumbnail': thumbnail,
        'etag': etag,
        'length': length,
    }


class Playlist(PlaylistInfo):
    '''
    ```
    {
        'platform': str,
        'playlist_id': str,
        'title': str,
        'owner': str,
        'description': str,
        'thumbnail': str,
        'length': str,
        'etag': str,
        'tracks': List[Track],
    }
    ```
    '''
    tracks: List[Track]


def into_playlist(playlist_info: PlaylistInfo, tracks: List[Track]) -> Playlist:
    return {
        **playlist_info,
        'tracks': tracks,
    }


class PlatformApi:
    '''
    # PlatformApi
    ### The base class for each supported platform's API (e.g. YouTube API)

    Attributes
    ------
    `platform`
    - The music platform in uppercase. supported platforms are:
        - `"YOUTUBE", "PLAYLIST", "SPOTIFY"`

    Methods
    ------
    `playlist(self, playlist_id)`
    - Gets the playlist with the specified `playlist_id`
    - Returns the `Playlist` dict if playlist is found, `None` if not found

    `playlist_info(self, playlist_id)`
    Returns the `Playlist` info without the `tracks` or `length`
    '''

    def __init__(self, platform: str) -> None:
        self.platform = platform

    def playlist(
        self,
        playlist_id: str,
        playlist_info: Optional[PlaylistInfo] = None
    ) -> Union[Playlist, None]:
        raise NotImplementedError()

    def playlist_info(self, playlist_id: str) -> Union[PlaylistInfo, None]:
        '''
        Returns
        ------
        The `PlaylistInfo` which doesn't include fields `tracks` or `length`
        '''
        raise NotImplementedError()
