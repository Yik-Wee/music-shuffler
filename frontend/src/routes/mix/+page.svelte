<script type="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { toPlaylistInfo } from '../../types/PlaylistTracks';
    import { getManyPlaylists } from '../../requests';
    import { TrackQueue } from '../../stores';
    import TrackList from '../../components/Tracks/TrackList.svelte';
    import { findSavedMix, type SavedMix } from '../../library';

    let title: string;
    let err: string | undefined;
    let mix: SavedMix | undefined;
    let currentPos = 0;

    function setQueue() {
        if (!mix) return;
        TrackQueue.setQueue(
            mix.tracks,
            mix.title,
            'mix',
            currentPos,
        );
    }

    onMount(async () => {
        title = $page.url.searchParams.get('title') || '';

        if (!title) {
            err = 'No Mix specified';
            return;
        }

        let savedMixInfo = findSavedMix(title);

        if (!savedMixInfo) {
            err = 'Mix Not Found';
            return;
        }

        let playlistResponses = await getManyPlaylists(savedMixInfo.playlists);
        mix = {
            title,
            playlists: [],
            tracks: [],
        }

        playlistResponses
            .forEach((playlist) => {
                mix?.playlists.push(toPlaylistInfo(playlist));
                mix?.tracks.push(...playlist.tracks);
            });
        });
</script>

<div>
    {#if mix}
        <div data-mix-title={mix.title} class="playlist-renderer">
            <img src="/assets/jammies.gif" alt="Mix - {mix.title}" class="playlist-thumbnail" />
        </div>

        <a
            href="/queue"
            on:click={() => {
                setQueue();
            }}>Shuffle in queue</a
        >

        <TrackList
            tracklist={mix.tracks}
            ifempty="Mix is empty"
            trackclick={(_track, position) => {
                currentPos = position;
                setQueue();
            }}
        />
    {:else if err}
        <h2>An error occurred :/</h2>
        <p>{err}</p>
    {:else if !title}
        <p>You can find or create a mix from your <a href="/library">library</a>!</p>
    {/if}
</div>
