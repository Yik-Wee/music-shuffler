<script lang="ts">
    import { getSaved, deleteSavedMix, deleteSavedPlaylist, type Library, getSavedMixes, type SavedPlaylistInfo, type SavedMix, type SavedMixInfo } from "../../../library";
    import { onMount } from "svelte";
    import SelectableLibaryItem from "../SelectableLibraryItem.svelte";

    let library: Library = {
        mixes: [],
        playlists: [],
    };

    let selectedPlaylists: SavedPlaylistInfo[] = [];
    let selectedMixTitles: string[] = [];

    onMount(async () => {
        library = await getSaved();
    });
</script>

<h1>Delete Playlists</h1>
<div class="library-area">
    {#each library.playlists as playlistInfo}
        <SelectableLibaryItem
            selectedlist={selectedPlaylists}
            colorSelected="red"
            item={{
                id: playlistInfo.playlist_id,
                platform: playlistInfo.platform,
            }}
            {...playlistInfo}
        />
        {/each}
</div>

<h1>Delete Mixes</h1>
<div class="library-area">
    {#each library.mixes as mixInfo}
        <SelectableLibaryItem
            selectedlist={selectedMixTitles}
            colorSelected="red"
            item={mixInfo.title}
            title={mixInfo.title}
            owner="Me"
            thumbnail="/assets/jammies.gif"
        />
    {/each}
</div>

<a href="/library">
    <button on:click={() => {
        selectedPlaylists.forEach(pl => deleteSavedPlaylist(pl));
        selectedMixTitles.forEach(title => deleteSavedMix(title));
    }}>Done</button>
</a>

<style>
    .library-area {
        flex-wrap: wrap;
        display: flex;
        row-gap: 10px;
        column-gap: 10px;
    }
</style>