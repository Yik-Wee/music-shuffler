<script type="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import {
        isErrorResponse,
        toPlaylistInfo,
        type PlaylistResponse
    } from '../../types/PlaylistTracks';
    import { getPlaylist } from '../../requests';
    import { TrackQueue } from '../../stores';
    import TrackList from '../../components/Tracks/TrackList.svelte';
    import { findSavedMix, type SavedMix } from '../../library';

    let title: string;
    let err: string | undefined;
    let mix: SavedMix | undefined;

    function setQueueIfQueueDiff() {
        if (mix && (TrackQueue.platform() !== 'mix' || TrackQueue.id() !== mix.title)) {
            TrackQueue.setQueue(mix.tracks, mix.title, 'mix');
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
            savedMixInfo.playlists.map(({ platform, id }) => getPlaylist(platform.toLowerCase(), id))
        );

        mix = {
            title,
            playlists: [],
            tracks: []
        };

        responses
            .filter((res): res is PlaylistResponse => {
                let isErr = !isErrorResponse(res);
                if (isErr) {
                    console.error('Response error:', res);
                }
                return isErr;
            })
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
                setQueueIfQueueDiff();
            }}>Shuffle in queue</a
        >

        <TrackList tracklist={mix.tracks} ifempty="Mix is empty" trackclick={setQueueIfQueueDiff} />
    {:else if err}
        <h2>An error occurred :/</h2>
        <p>{err}</p>
    {:else if !title}
        <p>You can find or create a mix from your <a href="/library">library</a>!</p>
    {/if}
</div>
