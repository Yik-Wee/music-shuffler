<script lang="ts">
    import { getSaved, deleteSavedMix, deleteSavedPlaylist, type Library, getSavedMixes, type SavedPlaylistInfo, type SavedMix, type SavedMixInfo } from "../../../library";
    import { onMount } from "svelte";
    import SelectablePlaylistCard from "../SelectablePlaylistCard.svelte";

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
        <SelectablePlaylistCard
            selectedlist={selectedPlaylists}
            colorSelected="red"
            {playlistInfo}
        />
        {/each}
</div>

<h1>Delete Mixes</h1>
<div class="library-area">
    {#each library.mixes as mixInfo}
        <SelectablePlaylistCard
            selectedlist={selectedMixTitles}
            colorSelected="red"
            playlistInfo={{
                title: mixInfo.title,
                owner: 'Me',
                thumbnail: '/assets/jammies.gif',
                platform: '',
                playlist_id: '',
                description: '',
                etag: '',
                length: -1,
            }}
            intoItem={() => {
                return {
                    title: mixInfo.title,
                }
            }}
        />
    {/each}
</div>

<a href="/library">
    <button on:click={() => {
        console.log(selectedPlaylists);
        console.log(selectedMixTitles);

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