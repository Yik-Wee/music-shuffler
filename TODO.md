# TODO
## Backend
- Ability to make custom playlists (tracks from diff platforms)
  - User accounts? Secure login system?
    - `Password = HASH(PlaintextPassword, Salt) CONCAT Salt` with e.g. scrypt
    - `User(Username, Password)`
  - User saved playlists
    - `UserPlaylists(Username, PlaylistID, Platform)`
  - User cached queue
    - `Queue(Username, QueueID, Length)`
    - `QueueTracks(QueueID, TrackID, Platform)`

## Frontend
- [ ] Fix cache queue
- Deal with unavailable youtube videos e.g. countdown, skip in 5s or something

## Maybe
- Use 206 partial response with flask API routes, using `yield` and `generator(), ...`
  - Reference: https://flask.palletsprojects.com/en/2.2.x/patterns/streaming/
- API cache so when user reloads page, `api_endpoint()` will wait for the previous API call to complete and use that result instead of making another API call
- If playlist/mix `length > 5000`, make a request to `/api/random_track?platform=...&id=...` instead of storing the entire playlist which would take up too much memory
- If playlist/mix `length > 5000`, randomise the `position` pointer to get the next random track instead of shuffling then rerendering the queue
- `youtube.py`: `YouTubeApi` use If-None-Match header
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag
