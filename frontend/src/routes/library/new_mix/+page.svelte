<script lang="ts">
    import { getSaved, getSavedMixes, save, type Library, type SavedMixInfo } from '../../../library';
    import PlaylistCard from '../../../components/PlaylistCard.svelte';
    import SelectablePlaylistCard from '../SelectablePlaylistCard.svelte';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    let newMix: SavedMixInfo = {
        title: '', // must be unique
        playlists: []
    };

    let library: Library = {
        mixes: [],
        playlists: [],
    };

    onMount(async () => {
        library = await getSaved();
    });

    function validateTitle(title: string): boolean {
        // title must be unique. Check if alr exists
        if (!title.trim()) {
            return false;
        }

        let trimmed = title.trim();
        let idx = library.mixes.findIndex((m) => m.title === trimmed);
        return idx === -1;
    }

    function validateMixLength(mix: SavedMixInfo): boolean {
        // must have more than 1 playlist
        return mix.playlists.length > 1;
    }

    let isValidTitle = false;
    let newMixError = '';
</script>

<h1>Saved Playlists</h1>
<div class="library-area">
    {#each library.playlists as playlistInfo}
        <SelectablePlaylistCard
            selectedlist={newMix.playlists}
            {playlistInfo}
        />
    {/each}
    <button disabled>Edit</button>
</div>

<h1>New Mix</h1>
<div class="library-area disabled">
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
                if (!isValidTitle) {
                    newMixError = 'Mix title must be unique';
                }

                console.log(isValidTitle);
            }}
        />
    </PlaylistCard>

    <button
        on:click={() => {
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

            library.mixes.push(newMix);
            save(newMix);
            goto('/library');
        }}
    >
        Done
        <div class="mix-error-message">
            <b>{newMixError}</b>
        </div>
    </button>
    <a href="/library">
        <button>Cancel</button>
    </a>
    <!-- <button
        on:click={() => {
            // cancel and reset everything
            goto('/library');
        }}>Cancel</button
    > -->
</div>

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

    .mix-error-message {
        color: red;
    }
</style>