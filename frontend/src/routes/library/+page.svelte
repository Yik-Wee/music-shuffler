<script lang="ts">
    import { getSaved, save, type Library } from "../../library";
    // import type { Library } from "../../library";
    import { onMount } from "svelte";
    import LibraryRenderer from "./Library.svelte";

    let library: Library;

    onMount(async () => {
        // ======testing code======
        // {
            save({
                title: 'NEW MIX 01',
                playlists: [
                    {
                        id: 'TEST-YT-01',
                        platform: 'youtube',
                    },
                    {
                        id: 'TEST-SC-01',
                        platform: 'soundcloud',
                    },
                    {
                        id: 'TEST-SP-01',
                        platform: 'spotify',
                    }
                ]
            });
        //     save({
        //         id: 'PLUQKJP1sVuNMvxOYqmdyOkE8Ryd_AWbQT',
        //         platform: 'youtube',
        //     });
        //     save({
        //         id: 'PL7IgabZ8nkx39Pl2SEMXTGfMnF8PwIYQo',
        //         platform: 'youtube',
        //     });
        //     save({
        //         id: 'TEST-SC-01',
        //         platform: 'soundcloud',
        //     })
        //     save({
        //         id: 'TEST-SP-01',
        //         platform: 'spotify',
        //     })
        // }
        // ======

        // lib = await getSaved();
        library = {
            mixes: [
                {
                    title: 'NEW MIX 01',
                    playlists: [
                        {
                            id: 'TEST-YT-01',
                            platform: 'youtube',
                        },
                        {
                            id: 'TEST-SC-01',
                            platform: 'soundcloud',
                        },
                        {
                            id: 'TEST-SP-01',
                            platform: 'spotify',
                        }
                    ]
                }
            ],
            playlists: [
                {
                    platform: 'youtube',
                    playlist_id: 'TEST-YT-01',
                    title: 'test 1',
                    owner: 'buh1',
                    description: 'buh',
                    thumbnail: '',
                    etag: '',
                },
                {
                    platform: 'spotify',
                    playlist_id: 'TEST-SP-01',
                    title: 'test 2',
                    owner: 'buh2',
                    description: 'buh',
                    thumbnail: '',
                    etag: '',
                },
                {
                    platform: 'soundcloud',
                    playlist_id: 'TEST-SC-01',
                    title: 'test 3',
                    owner: 'buh3',
                    description: 'buh',
                    thumbnail: '',
                    etag: '',
                },
            ]
        }
        console.log(library);
    });
</script>

<div class="library">
    {#if library}
        <LibraryRenderer {...library} />
    {:else}
        <h1>Loading...</h1>
    {/if}
</div>

<style>
    /* :global(.library-area) {
        flex-wrap: wrap;
        display: flex;
        row-gap: 10px;
        column-gap: 10px;
    } */
</style>