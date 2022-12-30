<script lang="ts">
    import { setPlayer, TrackQueue } from '../../stores';
    import { createEventDispatcher, onMount } from 'svelte';
    import SpotifyPlayer from '../../types/SpotifyPlayer';

    export let id: string | undefined = undefined;

    let player: SpotifyPlayer;
    let iframeId: string = 'spotify-player-iframe';

    let dispatch = createEventDispatcher();

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
    });
</script>

<div {id}>
    <iframe
        id={iframeId}
        title="Spotify Player"
        frameborder="0"
        src="https://open.spotify.com/embed/track/"
        allow="encrypted-media"
    />
</div>

<style src="./players.css"></style>
