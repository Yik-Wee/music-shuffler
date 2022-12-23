<!-- used to render a track list -->
<script lang="ts">
    import { TrackQueue } from '../../stores';
    import type { Track as TrackType } from '../../types/PlaylistTracks';
    import LazyTrack from './LazyTrack.svelte';
    import TrackListHeaders from './TrackListHeaders.svelte';
    import TrackListSearch from './TrackListSearch.svelte';

    export let tracklist: TrackType[];
    /** The message to display if the tracklist is empty */
    export let ifempty: string = 'Tracklist is empty!';
    /** The callback that is called when `Track` is clicked, before the `Track` is loaded */
    export let trackclick: (() => void) | undefined = undefined;

    let isSearching = false;
</script>

<div class="tracklist-wrapper">
    <TrackListSearch {tracklist} {trackclick} bind:isSearching={isSearching} />
    <TrackListHeaders hidden={isSearching} />
    <div class="tracklist" class:hidden={isSearching}>
        {#each tracklist as track, position}
            <LazyTrack
                {...track}
                {position}
                on:click={() => {
                    if (trackclick) {
                        trackclick();
                    }
                    TrackQueue.load(position);
                    TrackQueue.play();
                }}
            />
        {:else}
            <p>{ifempty}</p>
        {/each}
    </div>
</div>

<style>
    :root {
        --height: auto;
    }

    .tracklist {
        height: var(--height);
        overflow-x: hidden;
        overflow-y: auto;
    }

    .hidden {
        display: none;
    }
</style>
