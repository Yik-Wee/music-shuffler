<script type="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import {
        isErrorResponse,
        toPlaylistInfo,
        type PlaylistInfoResponse,
        type PlaylistResponse,
    } from '../../types/PlaylistTracks';
    import { getPlaylist } from '../../requests';
    import { TrackQueue } from '../../stores';
    import TrackList from '../../components/TrackList.svelte';
    import { findSavedMix, getSavedMixes, type SavedMix, type SavedMixInfo } from '../../library';

    let title: string;
    let err: string | undefined;
    let mix: SavedMix | undefined;

    function setQueueIfQueueDiff() {
        if (mix && TrackQueue.id() !== mix.title) {
            TrackQueue.setQueue(mix.tracks, mix.title);
        }
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

        let responses = await Promise.all(
            savedMixInfo.playlists.map(
                ({ platform, id }) => getPlaylist(platform, id)
            )
        );

        mix = {
            title,
            playlists: [],
            tracks: [],
        };

        responses
            .filter((res): res is PlaylistResponse => !isErrorResponse(res))
            .forEach(playlist => {
                mix?.playlists.push(toPlaylistInfo(playlist));
                mix?.tracks.push(...playlist.tracks);
            });
    });
</script>

<div>
    {#if title}
        {#if err}
            <div>{err}</div>
        {:else}
            <h2>{title}</h2>
        {/if}
    {:else}
        <div>Play a Mix in your library!</div>
    {/if}

    {#if mix}
        <div data-mix-title={mix.title} class="playlist-renderer">
            <img
                src="/assets/jammies.gif"
                alt="Mix - {mix.title}"
                class="playlist-thumbnail"
            />
        </div>

        <a href="/queue" on:click={() => {
            setQueueIfQueueDiff();
        }}>Shuffle in queue</a>

        <TrackList tracklist={mix.tracks} ifempty="Mix is empty" trackclick={setQueueIfQueueDiff} />
    {/if}
</div>