<script lang="ts">
    import { onMount } from 'svelte';
    // import LibraryRenderer from './Library.svelte';
    import { getSaved, type Library } from '../../library';
    import PlaylistCard from '../../components/PlaylistCard.svelte';
    import { goto } from '$app/navigation';

    let library: Library = {
        mixes: [],
        playlists: [],
    };

    onMount(async () => {
        library = await getSaved();
        console.log('library', library);
    });
</script>

<a href="/library/edit">Edit Library</a>

<h1>Saved Playlists</h1>
<div class="library-area">
    {#each library.playlists as playlistInfo}
        <PlaylistCard
            {...playlistInfo}
            on:click={() => goto(
                `/playlist/${playlistInfo.platform.toLowerCase()}?id=${playlistInfo.playlist_id}`
            )}
        />
    {/each}
</div>

<h1>Saved Mixes</h1>
<div class="library-area">
    {#each library.mixes as mixInfo}
        <PlaylistCard
            title={mixInfo.title}
            owner="Me"
            thumbnail="/assets/jammies.gif"
            on:click={() => goto(`/mix?title=${encodeURIComponent(mixInfo.title)}`)}
        />
    {/each}

    <PlaylistCard
        title="Add Mix"
        owner=""
        thumbnail="/assets/plus.svg"
        on:click={() => goto('/library/new_mix')}
    />
</div>

<style>
    .library-area {
        flex-wrap: wrap;
        display: flex;
        row-gap: 10px;
        column-gap: 10px;
    }

    /* .library-area.disabled > :global(.playlist-card:not(.enabled)) {
        pointer-events: none;
        opacity: 0.5;
    }

    .mix-title-input {
        outline: 0;
        border: 0;
        border-bottom: 2px solid lightskyblue;
        transition: all 200ms ease-in-out;
    }

    .mix-title-input:focus,
    .mix-title-input:hover {
        border-bottom: 2px solid blue;
    }

    .mix-title-input.error,
    .mix-title-input.error:focus,
    .mix-title-input.error:hover {
        border-bottom: 2px solid red;
    }

    .mix-error-message {
        color: red;
    } */
</style>
