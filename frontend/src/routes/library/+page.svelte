<script lang="ts">
    import { getSaved, save, type Library } from '../../library';
    // import type { Library } from "../../library";
    import { onMount } from 'svelte';
    import LibraryRenderer from './Library.svelte';

    let library: Library;

    onMount(async () => {
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
