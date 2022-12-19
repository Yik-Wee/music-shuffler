<!-- used to render a track list -->
<script lang="ts">
    import { TrackQueue } from '../stores';
    import type { Track as TrackType } from '../types/PlaylistTracks';
    import LazyTrack from './LazyLoader/LazyTrack.svelte';
    import Track from './LazyLoader/Track.svelte';

    export let tracklist: TrackType[];
    /** The message to display if the tracklist is empty */
    export let ifempty: string = 'Tracklist is empty!';
    /** The callback that is called when `Track` is clicked, before the `Track` is loaded */
    export let trackclick: (() => void) | undefined = undefined;

    // stuff to search for tracks in the tracklist & display them
    let isSearching = false;
    let searchedTitle = '';
    let trackIndices: number[] = [];
    let search: HTMLButtonElement;

    function findTrack(title: string): number[] {
        let titleLower = title.toLocaleLowerCase();
        let indices: number[] = [];

        tracklist.forEach((track, idx) => {
            if (track.title.toLocaleLowerCase().includes(titleLower)) {
                indices.push(idx);
            }
        });

        return indices;
    }
</script>

<div class="tracklist-search">
    <input
        type="text"
        placeholder="Track title"
        bind:value={searchedTitle}
        on:input={() => {
            if (!searchedTitle.trim()) {
                isSearching = false;
            }
        }}
        on:change={() => {
            let title = searchedTitle.trim();
            if (!title) {
                isSearching = false;
            }
            isSearching = true;
            trackIndices = findTrack(title);
        }}
        on:keydown={({ key }) => {
            if (key === 'Enter' && searchedTitle.trim().length > 0) {
                isSearching = true;
                search.click();
            }
        }}
    >
    <button bind:this={search}>Search</button>
    <button on:click={() => {
        isSearching = false;
        trackIndices = [];
        searchedTitle = '';
    }}>x</button>

    {#if isSearching}
        <div class="tracklist-headers track-layout">
            <div>#</div>
            <div>🖼️</div>
            <div>Title/Owner</div>
            <div>🕒</div>
        </div>

        <h3>Tracks with "{searchedTitle.trim()}" in its title</h3>
        {#each trackIndices as position}
            <Track
                {...tracklist[position]}
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
            <p>No tracks found</p>
        {/each}
    {/if}
</div>

<div class="tracklist" hidden={isSearching}>
    <div class="tracklist-headers track-layout">
        <div>#</div>
        <div>🖼️</div>
        <div>Title/Owner</div>
        <div>🕒</div>
    </div>

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

<style>
    .tracklist-headers {
        background-color: lightpink;
    }
</style>
