<script lang="ts">
    import { getSaved, getSavedMixes, save, type Library, type SavedMixInfo } from "../../library";
    import PlaylistCard from "../../components/PlaylistCard.svelte";
    import SelectablePlaylistCard from "./SelectablePlaylistCard.svelte";
    import { goto } from "$app/navigation";
    import type { PlaylistInfoResponse } from "../../types/PlaylistTracks";
    import { onMount } from "svelte";

    export let mixes: SavedMixInfo[];
    export let playlists: PlaylistInfoResponse[];

    let selecting: boolean = false;

    let newMix: SavedMixInfo = {
        title: '',  // must be unique
        playlists: [],
    };

    let savedMixes: SavedMixInfo[];
    onMount(async () => {
        savedMixes = getSavedMixes() || [];
    });

    function gotoPlaylist(playlistInfo: PlaylistInfoResponse) {
        goto(`/playlist/${playlistInfo.platform.toLowerCase()}?id=${playlistInfo.playlist_id}`);
    }

    function gotoMix(mixInfo: SavedMixInfo) {
        goto(`/mix?title=${encodeURIComponent(mixInfo.title)}`);
    }

    function validateTitle(title: string): boolean {
        // title must be unique. Check if alr exists
        if (!title.trim()) {
            return false;
        }

        let trimmed = title.trim();
        let idx = savedMixes.findIndex(m => m.title === trimmed);
        return idx === -1;
    }

    function validateMixLength(mix: SavedMixInfo): boolean {
        // must have more than 1 playlist
        return mix.playlists.length > 1;
    }

    let isValidTitle = false;
    let newMixError = '';
</script>

{#if selecting}
    <h1>Saved Playlists</h1>
    <div class="library-area">
        {#each playlists as playlistInfo}
            <!-- {selectedlist} -->
            <SelectablePlaylistCard
                selectedlist={newMix.playlists}
                {playlistInfo}
            />
        {/each}
        <button disabled>Edit</button>
    </div>

    <h1>Saved Mixes</h1>
    <div class="library-area disabled">
        {#each mixes as mixInfo}
            <PlaylistCard
                title={mixInfo.title}
                owner="Me"
                thumbnail="/assets/jammies.gif"
            />
        {/each}

        <PlaylistCard
            title=""
            owner="Me"
            thumbnail="/assets/jammies.gif"
            editable={true}
            classlist="enabled"
        >
            <input
                class="mix-title-input"
                class:error={!isValidTitle}
                type="text"
                bind:value={newMix.title}
                on:input={() => {
                    isValidTitle = validateTitle(newMix.title);
                    console.log(isValidTitle);
                }}
            >
        </PlaylistCard>

        <button on:click={() => {            
            if (!isValidTitle) {
                newMixError = 'Mix title must be unique';
                return;
            }
            
            if (!validateMixLength(newMix)) {
                newMixError = 'Mix must include more than 1 playlist';
                return;
            }
            
            newMix.title = newMix.title.trim();
            console.log(newMix);

            selecting = false;
            mixes.push(newMix);
            save(newMix);

            newMix = {
                title: '',
                playlists: [],
            };
        }}>
            Done
            <div class="mix-error-message"><b>{newMixError}</b></div>
        </button>
        <button on:click={() => {
            // cancel and reset everything
            selecting = false;
            isValidTitle = false;
            newMixError = '';
            newMix = {
                title: '',
                playlists: [],
            };
        }}>Cancel</button>
    </div>
{:else}
    <h1>Saved Playlists</h1>
    <div class="library-area">
        {#each playlists as playlistInfo}
            <PlaylistCard
                {...playlistInfo}
                on:click={() => gotoPlaylist(playlistInfo)}
            />
        {/each}
        <button>Edit</button>
    </div>

    <h1>Saved Mixes</h1>
    <div class="library-area">
        {#each mixes as mixInfo}
            <PlaylistCard
                title={mixInfo.title}
                owner="Me"
                thumbnail="/assets/jammies.gif"
                on:click={() => gotoMix(mixInfo)}
            />
        {/each}

        <PlaylistCard
            title="Add Mix"
            owner=""
            thumbnail="/assets/plus.svg"
            on:click={() => selecting = true}
        />
    </div>
{/if}

<style>
    .library-area {
        flex-wrap: wrap;
        display: flex;
        row-gap: 10px;
        column-gap: 10px;
    }

    .library-area.disabled > :global(.playlist-card:not(.enabled)) {
        pointer-events: none;
        opacity: 0.5;
    }

    .mix-title-input {
        outline: 0;
        border: 0;
        border-bottom: 2px solid lightskyblue;
        transition: all 200ms ease-in-out;
    }

    .mix-title-input:focus,
    .mix-title-input:hover {
        border-bottom: 2px solid blue;
    }

    .mix-title-input.error,
    .mix-title-input.error:focus,
    .mix-title-input.error:hover {
        border-bottom: 2px solid red;
    }

    .mix-error-message {
        color: red;
    }
</style>