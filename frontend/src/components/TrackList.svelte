<!-- used to render a track list -->
<script lang="ts">
    import { TrackQueue } from '../stores';
    import type { Track as TrackType } from '../types/PlaylistTracks';
    import Track from './Track.svelte';

    export let tracklist: TrackType[];
    /** The message to display if the tracklist is empty */
    export let ifempty: string = 'Tracklist is empty!';
    /** The callback that is called when `Track` is clicked, before the `Track` is loaded */
    export let trackclick: (() => void) | undefined = undefined;
</script>

<div class="tracklist">
    {#if tracklist}
        <div class="tracklist-headers track-layout">
            <div>#</div>
            <div>🖼️</div>
            <div>Title/Owner</div>
            <div>🕒</div>
        </div>
    {/if}

    {#each tracklist as track, position}
        <Track
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

<style>
    .tracklist > .tracklist-headers {
        background-color: lightpink;
    }
</style>
