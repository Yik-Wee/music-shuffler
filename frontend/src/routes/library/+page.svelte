<script lang="ts">
    import { getSaved, getSavedMixes, getSavedPlaylists, save, type Library } from "../../library";
    import { onMount } from "svelte";
    import PlaylistCard from "../../components/PlaylistCard.svelte";

    let lib: Library;

    onMount(async () => {
        // ======testing code======
        // save({
        //     id: 'MIX-01',
        //     title: 'Test Mix',
        //     playlists: [
        //         {
        //             id: 'TEST-YT-01',
        //             platform: 'youtube',
        //         },
        //         {
        //             id: 'TEST-SC-01',
        //             platform: 'soundcloud',
        //         },
        //         {
        //             id: 'TEST-SP-01',
        //             platform: 'spotify',
        //         }
        //     ]
        // });
        // save({
        //     id: 'PLUQKJP1sVuNMvxOYqmdyOkE8Ryd_AWbQT',
        //     platform: 'youtube',
        // });
        // save({
        //     id: 'PL7IgabZ8nkx39Pl2SEMXTGfMnF8PwIYQo',
        //     platform: 'youtube',
        // });
        // save({
        //     id: 'TEST-SC-01',
        //     platform: 'soundcloud',
        // })
        // save({
        //     id: 'TEST-SP-01',
        //     platform: 'spotify',
        // })
        // ======

        lib = await getSaved();
        console.log(lib);
    });
</script>

<div class="library">
    {#if lib}
        <h1>Saved Playlists</h1>
        <div class="library-area">
            {#each lib.playlists as playlistInfo}
                <PlaylistCard {...playlistInfo} />
            {/each}
        </div>

        <h1>Saved Mixes</h1>
        <div class="library-area">
            {#each lib.mixes as mixInfo}
                <PlaylistCard title={mixInfo.title} owner='Me' thumbnail='/assets/jammies.gif' />
            {/each}
        </div>
    {:else}
        <h1>Loading...</h1>
    {/if}
</div>

<style>
    .library > .library-area {
        flex-wrap: wrap;
        display: flex;
        row-gap: 10px;
        column-gap: 10px;
    }
</style>