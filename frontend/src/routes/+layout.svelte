<script lang="ts">
    import SearchBar from '../components/SearchBar.svelte';
    import Player from '../components/Player/Player.svelte';
    import NavBar from '../components/NavBar.svelte';
    import { TrackQueue } from '../stores';

    let loaded = false;
    // dont load player every hot reload during debugging
    let debug = false;

    function onPlayerLoad(e: CustomEvent) {
        console.info(e.detail);
        loaded = true;
        TrackQueue.hideAll();
    }
</script>

<main>
    {#if debug}
        <NavBar />
        <SearchBar />
        <slot />
    {:else}
        <NavBar />
        <SearchBar />
        <Player on:load={onPlayerLoad} />
        <div class="player-controls">
            <button class="prev" on:click={() => TrackQueue.loadPrev()}>Prev</button>
            <button class="toggle" on:click={() => TrackQueue.toggle()}>Play/Pause</button>
            <button class="next" on:click={() => TrackQueue.loadNext()}>Next</button>
        </div>
        {#if loaded}
            <slot />
        {/if}
    {/if}
</main>
<div hidden>
    <a href="/playlist/youtube">Search YouTube Playlist</a>
    <a href="/playlist/spotify">Search Spotify Playlist</a>
    <a href="/playlist/soundcloud">Search SoundCloud Playlist</a>
</div>

<style>
    @font-face {
        font-family: 'Varela';
        src: url('/fonts/VarelaRound/VarelaRound-Regular.ttf');
    }

    :root,
    :global(input, textarea, button, option, select) {
        font-family: 'Varela';
        font-size: 13px;
    }

    :global(.ellipsis) {
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }

    .player-controls > * {
        /* ... */
    }
</style>
