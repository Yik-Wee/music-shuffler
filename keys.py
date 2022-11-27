import os
import dotenv


class MissingApiKeyException(Exception):
    def __init__(self, key_name: str) -> None:
        super().__init__(
            f'Missing {key_name} in .env file. Please provide one in .env in the format:',
            f'\n{key_name}=<Your {key_name}>'
        )


dotenv.load_dotenv('.env', verbose=True)
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


if YOUTUBE_API_KEY is None:
    raise MissingApiKeyException('YOUTUBE_API_KEY')

if SPOTIFY_CLIENT_ID is None:
    raise MissingApiKeyException('SPOTIFY_CLIENT_ID')

if SPOTIFY_CLIENT_SECRET is None:
    raise MissingApiKeyException('SPOTIFY_CLIENT_SECRET')
