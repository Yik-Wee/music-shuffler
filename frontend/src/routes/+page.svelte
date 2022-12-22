<!-- <script lang="ts">
    // TESTING CODE
    import TrackList from "../components/TrackList.svelte";
    import { TrackQueue } from "../stores";

    TrackQueue.setQueue(
        [
            {
                track_id: 'F64yFFnZfkI',
                platform: 'youtube',
                title: 'ヨルシカ - 言って。(Music Video)',
                owner: 'ヨルシカ / n-buna Official',
                thumbnail: 'https://i.ytimg.com/vi/F64yFFnZfkI/sddefault.jpg',
            },
            {
                track_id: '2TLdQFjTPITmXmxZkRmi2k',
                platform: 'spotify',
                title: 'Interlude (Gymnopedie No. 1)',
                owner: 'Anamanaguchi',
                thumbnail: 'https://i.scdn.co/image/ab67616d0000b27313f450149d7ffbeadbf51a4b',
                duration_seconds: 69,
            },
            {
                track_id: '506962848',
                platform: 'soundcloud',
                title: '美波「ETERNAL BLUE」',
                owner: 'Eysus',
                thumbnail: 'https://i1.sndcdn.com/artworks-000412590138-7iqtgg-large.jpg',
                duration_seconds: 383,
            },
        ],
        'test',
        'mix'
    )
</script>

<TrackList tracklist={TrackQueue.tracklist()} /> -->

<h1>Music Shuffler</h1>
<pre>♪ ( ´˘`) -ᴗ-) ´˘`) -ᴗ-) ♫</pre>

<h2>🤔 How it works</h2>
<p>
    Shuffle YouTube, Spotify and SoundCloud playlists! Just enter the playlist URL
    in the search bar!
</p>

<h2>🦧 Accepted playlists</h2>
<p>Playlists that can be found include:</p>
<li>YouTube: <b>public/unlisted</b> playlists</li>
<li>Spotify: <b>public</b> playlists</li>
<li>SoundCloud: <b>public</b> playlists</li>

<h2>⚠️ Note</h2>
<p>
    In order to play full Spotify tracks, you must be currently signed in to
    <a href="https://open.spotify.com">Spotify</a> on this device. Otherwise, only
    a 30 second "preview" of the track can be played.
</p>