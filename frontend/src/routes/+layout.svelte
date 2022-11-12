<script lang="ts">
    import { PlayerController, playerNames, players } from '../stores';
    import { onMount } from 'svelte';
    import SoundCloudPlayer from '../components/Player/SoundCloudPlayer.svelte';
    import SpotifyPlayer from '../components/Player/SpotifyPlayer.svelte';
    import YouTubePlayer from '../components/Player/YouTubePlayer.svelte';

    onMount(() => {
        players.controller = new PlayerController();
        let recentlyPlayedString = localStorage.getItem('recentlyPlayed');
        let recentlyPlayed = recentlyPlayedString ? JSON.parse(recentlyPlayedString) : undefined;
        if (!recentlyPlayed) {
            players.controller?.hideAll();
        }
        players.controller?.swapPlayer(playerNames[0]);
    });
</script>

<main data-sveltekit-prefetch>
    <div id="players-container">
        <SpotifyPlayer />
        <YouTubePlayer />
        <SoundCloudPlayer />
    </div>
    <!-- <button
        id="play-prev"
        on:click={() => {
            idx -= 1;
            if (idx < 0) {
                idx = playerNames.length - 1;
            }
            players.controller?.swapPlayer(playerNames[idx]);
        }}>◀️</button
    > -->
    <button
        id="play-pause"
        on:click={() => {
            players.controller?.toggle();
        }}>⏯️</button
    >
    <!-- <button
        id="play-next"
        on:click={() => {
            idx = (idx + 1) % playerNames.length;
            players.controller?.swapPlayer(playerNames[idx]);
        }}>▶️</button
    > -->
    <slot />
</main>

<style>
    :global(.track-thumbnail) {
        max-height: 100px;
        max-width: 100px;
    }

    :global(.playlist-thumbnail) {
        max-height: 200px;
        max-width: 200px;
    }

    :global(.playlist-description-ellipses) {
        text-overflow: ellipsis;
    }

    :global(.playlist-description-expanded) {
        text-overflow: unset;
    }
</style>
