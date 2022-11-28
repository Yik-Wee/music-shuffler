<script lang="ts">
    import { getSaved, save, type Library } from "../../library";
    // import type { Library } from "../../library";
    import { onMount } from "svelte";
    import LibraryRenderer from "./Library.svelte";

    let library: Library;

    onMount(async () => {
        // ======testing code======
        {
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
                save({
                    id: 'PLUQKJP1sVuNMvxOYqmdyOkE8Ryd_AWbQT',
                    platform: 'youtube',
                });
                save({
                    id: 'PL7IgabZ8nkx39Pl2SEMXTGfMnF8PwIYQo',
                    platform: 'youtube',
                });
                save({
                    id: 'TEST-SC-01',
                    platform: 'soundcloud',
                })
                save({
                    id: 'TEST-SP-01',
                    platform: 'spotify',
                })
        }
        // ======

        library = await getSaved();
    });
</script>

<div class="library">
    {#if library}
        <LibraryRenderer {...library} />
    {:else}
        <h1>Loading...</h1>
    {/if}
</div>
