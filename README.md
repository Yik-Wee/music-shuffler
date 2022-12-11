# TODO
## Backend
- [ ] `YouTubeApi`: use `item['contentDetails']['itemCount']` to get `Length` field.
  - Afterwards, the `length == -1` check can be removed
  - https://developers.google.com/youtube/v3/docs/playlists#contentDetails.itemCount
- [ ] Finish `SpotifyApi` and test it
  - https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
- [ ] Finish `SoundCloudApi` and test it
  - SoundCloud API no longer supports registering an app (since like 2019 or something -_-)
  - Request regular frontend routes and parse the response for playlist data
  - ID stored must be the request path `url` / `permalink_url` ~~OR the id e.g. 118270473 and request sent to the widget endpoint.~~
  - use `last_modified` as the etag
  - https://github.com/skdhg/soundcloud-scraper
- [ ] Deal with deleted videos server side

## Frontend
- [ ] Add lazy loading to track-renderer containers to speed up re-rendering of shuffled queue
  - https://css-tricks.com/lazy-loading-images-in-svelte/
- [ ] Search function to find a track in the playlist/queue
- [ ] Add styling to frontend
- [ ] **?** Deal with unavailable youtube videos e.g. countdown, skip in 5s or something
- [ ] **?** Add settings

# TODO Maybe
- [ ] Use 206 partial response with flask API routes, using `yield` and `generator(), ...`
  - Reference: https://flask.palletsprojects.com/en/2.2.x/patterns/streaming/
- [ ] API cache so when user reloads page, `api_endpoint()` will wait for the previous API call to complete and use that result instead of making another API call
- [ ] If playlist/mix `length > 5000`, make a request to `/api/random_track?platform=...&id=...` instead of storing the entire playlist which would take up too much memory
- [ ] If playlist/mix `length > 5000`, randomise the `position` pointer to get the next random track instead of shuffling then rerendering the queue
- [ ] `youtube.py`: `YouTubeApi` use If-None-Match header
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag

# Navigation redo
- `/mix?id=...`
  - fetch playlists from mix
- `/search?platform=...&id=...`
  - fetch playlist info, display on `PlaylistCard`
  - onclick, goto `/[platform]?id=...`
- `/playlist/[platform]?id=...`
  - Fetch playlist, display tracks, shuffle, etc.
  - If track clicked and playlist not current queue yet, set playlist tracks to current queue
- `/queue`
  - Display tracks in current queue, shuffle, etc.
- `/library`
  - See all saved playlists & mixes
- `/settings`

# Running
### To run locally, please provide the following information inside `.env`
- `YOUTUBE_API_KEY`
  - Your YouTube API Key. Ensure `127.0.0.1` or `localhost` is whitelisted. Read https://developers.google.com/youtube/v3/getting-started on how to obtain the key or set restrictions.
  - A `MissingYouTubeApiException` is raised if this field is missing
- ...

# Functionality
### Search for a YouTube, Spotify or SoundCloud playlist by its Playlist ID
### Only public/unlisted YouTube playlists can be accessed
### Only public Spotify playlists can be accessed
### Only public/unlisted SoundCloud playlists can be accessed

# Dependencies
### Dependencies can be found in [requirements.txt](requirements.txt)
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
