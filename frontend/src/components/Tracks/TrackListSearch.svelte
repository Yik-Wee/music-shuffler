<script lang="ts">
    import Track from './Track.svelte';
    import type { Track as TrackType } from '../../types/PlaylistTracks';
    import { TrackQueue } from '../../stores';

    export let tracklist: TrackType[];

    /** The callback that is called when `Track` is clicked, before the `Track` is loaded */
    export let trackclick: (() => void) | undefined = undefined;

    export let isSearching: boolean;
    let searched = '';
    let searchedFrozen = '';
    let trackIndices: number[] = [];
    let search: HTMLButtonElement;

    function findTrack(titleOrOwner: string): number[] {
        let titleOrOwnerLower = titleOrOwner.toLocaleLowerCase();
        let indices: number[] = [];

        tracklist.forEach((track, idx) => {
            if (
                track.title.toLocaleLowerCase().includes(titleOrOwnerLower) ||
                track.owner.toLocaleLowerCase().includes(titleOrOwnerLower)
            ) {
                indices.push(idx);
            }
        });

        return indices;
    }
</script>

<div class="tracklist-search">
    <div class="tracklist-search-bar">
        <input
            type="text"
            placeholder="Search track by title/artist"
            bind:value={searched}
            on:input={() => {
                if (!searched.trim()) {
                    isSearching = false;
                }
            }}
            on:change={() => {
                searchedFrozen = searched.trim();
                if (!searchedFrozen) {
                    isSearching = false;
                    return;
                }
                isSearching = true;
                trackIndices = findTrack(searchedFrozen);
            }}
            on:keydown={({ key }) => {
                if (key === 'Enter') {
                    search.click();
                }
            }}
        />
        {#if isSearching}
            <button
                on:click={() => {
                    isSearching = false;
                    trackIndices = [];
                    searched = '';
                    searchedFrozen = '';
                }}
            >
                x
            </button>
        {:else}
            <button bind:this={search}>Search</button>
        {/if}
    </div>

    {#if isSearching}
        <div class="tracklist-headers track-layout">
            <div>#</div>
            <div>🖼️</div>
            <div>Title/Owner</div>
            <div>🕒</div>
        </div>

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
                highlight={searchedFrozen}
                highlightColor="lightgreen"
            />
        {:else}
            <p>No tracks found</p>
        {/each}
    {/if}
</div>

<style>
    .tracklist-search-bar {
        display: flex;
        flex-direction: row;
        column-gap: 0.5rem;
        width: 100%;
    }

    input {
        width: 100%;
    }
</style>