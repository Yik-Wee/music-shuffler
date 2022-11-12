<script lang="ts">
    import { containerIds, players } from '../../stores';
    import { onMount } from 'svelte';
    import SpotifyPlayer from '../../types/SpotifyPlayer';

    let player: SpotifyPlayer | undefined;

    onMount(() => {
        player = new SpotifyPlayer('spotify-player-iframe', {
            onEnded: (target: SpotifyPlayer) => {
                console.log('spotify track ended');
                // target.loadTrack(/*...*/);
                // target.play();
            },
            onReady: (target: SpotifyPlayer) => {
                console.log('spotify track ready');
                console.log(target);
                target.playTrack();
            }
        });
        // spotifyPlayer.set(player);
        players.spotify = player;
    });
</script>

<div id="{containerIds.spotify}">
    <iframe
        id="spotify-player-iframe"
        title="insert title here"
        src="https://open.spotify.com/embed/track/5NDAjPZGAlMz3PqyttrE2s"
        frameborder="0"
    />
    <!-- <script src="https://open.spotify.com/embed-podcast/iframe-api/v1" async></script> -->
    <!-- <div id="spotify-iframe-api-container"></div>
    <div id="embed-iframe" /> -->
</div>
