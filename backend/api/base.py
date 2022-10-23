from typing import List, TypedDict, Union


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
    duration_seconds: int


class Playlist(TypedDict):
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
    platform: str
    playlist_id: str
    title: str
    owner: str
    description: str
    thumbnail: str
    length: int
    etag: str
    tracks: List[Track]


class PlatformApi:
    '''
    # PlatformApi
    ### The base class for each supported platform's API (e.g. YouTube API)

    Attributes
    ------
    `base_url`
    - The base url for the API endpoint

    Methods
    ------
    `playlist(self, playlist_id)`
    - Gets the playlist with the specified `playlist_id` from the API endpoint from `base_url
    - Returns the `Playlist` dict if playlist is found, `None` if not found

    `etag(self, playlist_id)`
    - Returns the etag of the playlist with the specified `playlist_id`, `None` if not found
    '''

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def playlist(self, playlist_id: str) -> Union[Playlist, None]:
        raise NotImplementedError()

    def etag(self, playlist_id: str) -> Union[str, None]:
        raise NotImplementedError()
