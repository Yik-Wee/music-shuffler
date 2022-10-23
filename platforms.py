'''
Exports for music platform specific API interfaces

`platform_apis`: `Dict[str, PlatformApi]`
- A dictionary mapping the music platform's name (in lowercase) to it's API instance

`ALL_PLATFORMS`: `List[str]`
- The list of all supported music platforms, obtained from `platform_apis.keys()`
'''
from typing import Dict
import os
import dotenv
from backend.api import YouTubeApi, SpotifyApi, SoundCloudApi, PlatformApi

dotenv.load_dotenv('.env')
_YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

platform_apis: Dict[str, PlatformApi] = {
    'YOUTUBE': YouTubeApi(api_key=_YOUTUBE_API_KEY),
    'SPOTIFY': SpotifyApi(),
    'SOUNDCLOUD': SoundCloudApi()
}

# ALL_PLATFORMS = list(map(platform_apis.keys(), lambda x: x.lower()))
ALL_PLATFORMS = ('youtube', 'spotify', 'soundcloud')
'''The list of all supported music platforms, obtained from `platform_apis.keys()`'''
