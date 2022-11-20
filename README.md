# TODO
- [ ] Fix `SearchBar`
- [ ] Finish `SpotifyApi` and test it
- [ ] Finish `SoundCloudApi` and test it
- [ ] Add `/library` route: caching **playlist IDs** and mixes (`playlistID[]`) in `localStorage` -> `fetch` title, owner & length from API endpoint
- [ ] Add playlist mixes to frontend (shuffle tracks from multiple playlists)
- [ ] Add specific tracks from different playlists to queue
- [ ] Add `NavBar`
- [ ] Search function to find a track in the playlist/queue
- [ ] Ability to empty the queue
- [ ] Add lazy loading to track-renderer containers to speed up re-rendering of shuffled queue
  - https://css-tricks.com/lazy-loading-images-in-svelte/
- [ ] Add styling to frontend
- [ ] Add settings
- [ ] Decide whether to render thumbnails client side & store thumbnails server side. If so, change.
- [ ] Deal with deleted videos server side
- [ ] **(1?)** Use 206 partial response with flask API routes, using `yield` and `generator(), ...`
  - Reference: https://flask.palletsprojects.com/en/2.2.x/patterns/streaming/
- [ ] **(2?)** API cache so when user reloads page, `api_endpoint()` will wait for the previous API call to complete and use that result instead of making another API call
- [ ] **(3?)** If playlist/mix `length > 5000`, make a request to `/api/random_track?platform=...&id=...` instead of storing the entire playlist which would take up too much memory
- [ ] **(4?)** If playlist/mix `length > 5000`, randomise the `position` pointer to get the next random track instead of shuffling then rerendering the queue

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
