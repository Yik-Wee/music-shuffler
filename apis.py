'''
Exports for music platform specific API interfaces

`platform_apis`: `Dict[str, PlatformApi]`
- A dictionary mapping the music platform's name (in lowercase) to it's API instance

`ALL_PLATFORMS`: `List[str]`
- The list of all supported music platforms, obtained from `platform_apis.keys()`
'''
from typing import Dict
from backend.api import YouTubeApi, SpotifyApi, SoundCloudApi, PlatformApi
import keys

platform_apis: Dict[str, PlatformApi] = {
    'YOUTUBE': YouTubeApi(
        api_key=keys.YOUTUBE_API_KEY
    ),
    'SPOTIFY': SpotifyApi(
        client_id=keys.SPOTIFY_CLIENT_ID,
        client_secret=keys.SPOTIFY_CLIENT_SECRET
    ),
    'SOUNDCLOUD': SoundCloudApi()
}

# ALL_PLATFORMS = list(map(platform_apis.keys(), lambda x: x.lower()))
ALL_PLATFORMS = ('youtube', 'spotify', 'soundcloud')
'''The list of all supported music platforms, obtained from `platform_apis.keys()`'''
