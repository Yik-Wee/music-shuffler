<script lang="ts">
    import { getSaved, getSavedMixes, save, type Library, type SavedMixInfo } from '../../../library';
    import LibraryItem from '../../../components/LibraryItem.svelte';
    import SelectableLibraryItem from '../SelectableLibraryItem.svelte';
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

    let mixTrackCount = 0;

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

    function validateMix(mix: SavedMixInfo, mixTrackCount: number): [boolean, string] {
        if (!validateTitle(mix.title)) {
            return [false, 'Invalid title. Title must be unique'];
        }

        if (mix.playlists.length === 0) {
            return [false, 'Mix must have >1 playlist'];
        }

        if (mixTrackCount > 50000) {
            return [false, 'Mix must have ≤50000 tracks'];
        }

        return [true, ''];
    }

    $: isValidTitle = validateTitle(newMix.title);
    $: [isValidMix, errorMsg] = validateMix(newMix, mixTrackCount);
</script>

<h1>Saved Playlists</h1>
<div class="library-area">
    {#each library.playlists as playlistInfo}
        <SelectableLibraryItem
            selectedlist={newMix.playlists}
            item={{
                platform: playlistInfo.platform,
                id: playlistInfo.playlist_id,
            }}
            onselect={() => mixTrackCount += playlistInfo.length}
            onunselect={() => mixTrackCount -= playlistInfo.length}
            {...playlistInfo}
        />
    {/each}
    <button disabled>Edit</button>
</div>

<h1>New Mix</h1>
<div class="library-area disabled">
    <LibraryItem
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
        />
    </LibraryItem>

    <button
        disabled={!isValidMix}
        on:click={() => {
            if (!isValidMix) {
                return;
            }

            newMix.title = newMix.title.trim();
            library.mixes.push(newMix);
            save(newMix);
            goto('/library');
        }}
    >
        Done
        <div class="mix-error-message">
            <b>{errorMsg}</b>
        </div>
    </button>
    <a href="/library">
        <button>Cancel</button>
    </a>
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

    .mix-title-input.error,
    .mix-title-input.error:focus,
    .mix-title-input.error:hover {
        border-bottom: 2px solid red;
    }

    .mix-error-message {
        color: red;
    }
</style>