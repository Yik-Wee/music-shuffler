<script lang="ts">
    import { onMount } from 'svelte';
    import { getSaved, type Library } from '../../library';
    import LibraryItem from '../../components/LibraryItem.svelte';
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
        <LibraryItem
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
        <LibraryItem
            title={mixInfo.title}
            owner="Me"
            thumbnail="/assets/jammies.gif"
            on:click={() => goto(`/mix?title=${encodeURIComponent(mixInfo.title)}`)}
        />
    {/each}

    <LibraryItem
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
</style>
