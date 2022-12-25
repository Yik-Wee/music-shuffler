# Running locally
### Provide the following information inside `.env`
- `YOUTUBE_API_KEY`
  - Ensure `127.0.0.1` or `localhost` is whitelisted. Read https://developers.google.com/youtube/v3/getting-started on how to obtain the key or set restrictions.
  - A `MissingYouTubeApiException` is raised if this field is missing
- `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`
  - Obtain from https://developer.spotify.com/dashboard/

# Functionality
### Search for a YouTube, Spotify or SoundCloud playlist by its Playlist ID
### Only public/unlisted YouTube playlists can be accessed
### Only public Spotify playlists can be accessed
### Only public SoundCloud playlists can be accessed

# Dependencies
### Found in [requirements.txt](requirements.txt)
### Run
```sh
pip install -r requirements.txt
```
### To install the following requirements
- flask
- python-dotenv
- requests
# Dev Dependencies
### Only for code formatting and linting
- pylint
- autopep8
