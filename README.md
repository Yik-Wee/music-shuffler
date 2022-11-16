# TODO
- [ ] Finish `SpotifyApi` and test it
- [ ] Finish `SoundCloudApi` and test it
- [ ] Add youtube player api functionality to frontend
- [ ] Add spotify player api functionality to frontend
- [ ] Add soundcloud player api functionality to frontend
- [ ] Add sveltekit stores `src/stores.ts`
- [ ] Add playlists to frontend (`fetch` from API -> display -> shuffle)
- [ ] Add caching **playlist IDs** and mixes (`playlistID[]`) in `localStorage` -> `fetch` title, owner & length from API endpoint
- [ ] Add playlist mixes to frontend (shuffle tracks from multiple playlists)
- [ ] Add specific tracks from different playlists to queue
- [ ] Ability to empty the queue
- [ ] Add styling to frontend
- [ ] Add settings
- [ ] **(1?)** Use 206 partial response with flask API routes, using `yield` and `generator(), ...`
  - Reference: https://flask.palletsprojects.com/en/2.2.x/patterns/streaming/
- [ ] **(2?)** API cache so when user reloads page, `api_endpoint()` will wait for the previous API call to complete and use that result instead of making another API call
- [ ] **(3?)** If playlist/mix `length > 5000`, make a request to `/api/random_track?platform=...&id=...` instead of storing the entire playlist which would take up too much memory
- [ ] **(4?)** If playlist/mix `length > 5000`, randomise the `position` pointer to get the next random track which takes O(1) time instead of shuffling then rerendering the queue taking O(n) time

# Navigation
## Non-navbar Routes
### `/[platform]?id=...`
  - fetches playlist info (NOT tracks)
  - When the playlist card / play button is clicked, store `id` GET param in `store`, redirect to `/queue?id=...`
  <!-- - **(1?)** Cancel button to cancel fetching of contents & display partial contents -->
## Navbar routes
### Home
- Display recently played playlist(s)
- Initialise player with most recently played song at position it was stopped at
### Library
#### Playlists
- This section displays saved playlists
- Select multiple playlists (/ specific tracks ?) to create a new mix
<!-- - When a playlist card is clicked, route to `/[platform]?id=<playlistID>` -->
- When a playlist card is clicked, route to `/queue?id=...`
#### Mixes
- This section displays the created mixes
### Queue
- Get playlist ID / Mix ID from the url GET params `?id`
  - Playlist: `?id=<playlist_id>`
  - Mix: `?id=<MIX ID>` e.g. `?id=MIX23`
- Fetch tracks, display & shuffle
### Search
- Search bar at the top. Disappears on scroll down, reappears on scroll up
- When searched, route to `/[platform]?id=<playlistID>`

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
