<script lang="ts">
    import { setPlayer, TrackQueue } from '../../stores';
    import { createEventDispatcher, onMount, setContext } from 'svelte';
    import SpotifyPlayer from '../../types/SpotifyPlayer';

    export let id: string | undefined = undefined;

    let player: SpotifyPlayer;
    let iframeId: string = 'spotify-player-iframe';

    let dispatch = createEventDispatcher();

    // setContext('spotify', {
    //     getPlayer: () => player,
    // });

    onMount(() => {
        player = new SpotifyPlayer(iframeId, {
            onEnded: (target: SpotifyPlayer) => {
                console.log('spotify track ended');
                TrackQueue.loadNext();
            },
            onReady: (target: SpotifyPlayer) => {
                console.log('spotify track ready');
                console.log(target);
                target.playTrack();
            }
        });

        setPlayer('spotify', player);

        dispatch('load', {
            text: 'Spotify player loaded'
        });
        // players.spotify = player;
    });
</script>

<div {id}>
    <iframe
        id={iframeId}
        title="insert title here"
        frameborder="0"
        src="https://open.spotify.com/embed/track/"
    />
</div>
<!-- src="https://open.spotify.com/embed/track/5NDAjPZGAlMz3PqyttrE2s" -->
<!-- <script src="https://open.spotify.com/embed-podcast/iframe-api/v1" async></script> -->
<!-- <div id="spotify-iframe-api-container"></div>
<div id="embed-iframe" /> -->
