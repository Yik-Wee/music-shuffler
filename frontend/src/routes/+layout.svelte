<script lang="ts">
    import SearchBar from '../components/SearchBar.svelte';
    import Player from '../components/Player.svelte';
    import NavBar from '../components/NavBar.svelte';
    import { supportedPlatforms, TrackQueue } from '../stores';
    import { onMount } from 'svelte';

    let loaded = false;
    let hiddenContainer: HTMLDivElement;

    function onPlayerLoad(e: CustomEvent) {
        console.info(e.detail);
        loaded = true;
        TrackQueue.hideAll();
    }

    let hidden = false;
    let prevYOffset = 0;

    onMount(() => {
        hiddenContainer.remove();
        window.addEventListener('scroll', () => {
            // make the navbar disappear
            let yOffset = window.pageYOffset;
            if (prevYOffset > yOffset) {
                hidden = false
            } else {
                hidden = true;
            }
            prevYOffset = yOffset;
        });
    });
</script>

<main>
    <div class="top-bar" class:hidden>
        <NavBar />
        <SearchBar />
    </div>
    <div id="content">
        <Player on:load={onPlayerLoad} />
        <div class="player-controls">
            <button class="prev" on:click={() => TrackQueue.loadPrev()}>Prev</button>
            <button class="toggle" on:click={() => TrackQueue.toggle()}>Play/Pause</button>
            <button class="next" on:click={() => TrackQueue.loadNext()}>Next</button>
        </div>
        {#if loaded}
            <slot />
        {/if}
    </div>
</main>
<div hidden bind:this={hiddenContainer}>
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

    :global(body) {
        margin: 0;
    }

    :global(input) {
        outline: 0;
        border: 0;
        border-bottom: 2px solid lightskyblue;
        transition: all 200ms ease-in-out;
    }

    :global(input:focus, input:hover) {
        border-bottom: 2px solid blue;
    }

    :global(button) {
        border: 1.5px solid lightblue;
        border-radius: 3px;
        padding: 0.25em 1em;
        background: none;
        transition: all 100ms ease-in-out;
    }

    :global(button:hover) {
        cursor: pointer;
        border-color: blue;
        background: rgb(255, 234, 237);
    }

    :global(.ellipsis) {
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }

    /* @media screen and (min-width: 768px) {
        .top-bar {
            display: flex;
            flex-direction: row;
        }
    } */

    .top-bar {
        height: 10vh;
        width: 100%;
        position: fixed;
        top: 0;
        z-index: 9;
        transition: opacity 75ms ease-in-out;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .top-bar.hidden {
        opacity: 0;
    }

    #content {
        margin-top: 10vh;
    }

    .player-controls > * {
        /* ... */
    }
</style>
