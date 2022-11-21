<!-- used to render a track list -->
<script lang="ts">
    import { TrackQueue } from "../stores";
    import type { Track as TrackType } from "../types/PlaylistTracks";
    import Track from "./Track.svelte";

    export let tracklist: TrackType[];
    /** The message to display if the tracklist is empty */
    export let ifempty: string = 'Tracklist is empty!';
    /** The callback that is called when `Track` is clicked, before the `Track` is loaded */
    export let trackclick: (() => void) | undefined = undefined;
</script>

<div class="tracklist">
    {#if tracklist}
        <div class="tracklist-headers">
            <div>#</div>
            <div></div>
            <div>Title</div>
            <div>Owner</div>
            <div>🕒</div>
        </div>
    {/if}

    {#each tracklist as track, position}
        <Track {...track} {position} on:click={() => {
            if (trackclick) {
                trackclick();
            }
            TrackQueue.load(position);
            TrackQueue.play();
        }} />
    {:else}
        <p>{ifempty}</p>
    {/each}
</div>

<style>
    /* .tracklist {
        height: 65vh;
        overflow-y: auto;
    } */

    .tracklist > .tracklist-headers {
        border: 1px solid transparent;
        border-radius: 4px;
        height: 60px;
        position: relative;
        column-gap: 8px;
        display: grid;
        padding: 0 16px;
        grid-template-columns: [index] 8px [first] 40px [var1] 2.75fr [var2] 1.75fr [last] .25fr;
        align-items: center;
        background-color: lightpink;
        transition: background-color 100ms ease-in;
    }
</style>