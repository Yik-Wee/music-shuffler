<script type="ts">
    import type { PageData } from './$types';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { isErrorResponse, type PlaylistResponse } from '../../../types/PlaylistTracks';
    import { getPlaylist } from '../../../requests';
    import { TrackQueue } from '../../../stores';
    import TrackList from '../../../components/TrackList.svelte';
    import { savePlaylist } from '../../../library';

    export let data: PageData;
    let id: string;
    let err: string | undefined;
    let playlist: PlaylistResponse | undefined;

    function setQueueIfQueueDiff() {
        if (
            playlist &&
            (TrackQueue.id() !== playlist.playlist_id ||
                TrackQueue.platform() !== playlist.platform)
        ) {
            // set current playlist to play in queue
            TrackQueue.setQueue(
                playlist.tracks,
                playlist.playlist_id,
                playlist.platform.toLowerCase()
            );
        }
    }

    onMount(async () => {
        id = $page.url.searchParams.get('id') || '';

        // request data from API endpoint for specified platform
        let res = await getPlaylist(data.platform, id);
        if (isErrorResponse(res)) {
            err = res.error;
        } else {
            playlist = res;
        }
    });
</script>

<div>
    <h1>{data.platform}</h1>
    {#if id}
        {#if err}
            <div>{err}</div>
        {/if}
    {:else}
        <div>Search for a {data.platform} playlist with it's playlist ID!</div>
    {/if}

    {#if playlist}
        <div data-playlist-id={playlist.playlist_id} class="playlist-renderer">
            <h2>{playlist.owner}</h2>
            <h2>{playlist.title}</h2>
            <div>
                <p class="playlist-description-ellipses">{playlist.description}</p>
            </div>
            <img
                src={playlist.thumbnail}
                alt="{playlist.owner} - {playlist.title}"
                class="playlist-thumbnail"
            />
        </div>

        <button
            on:click={() => {
                if (!playlist) {
                    return;
                }

                savePlaylist({ id: playlist.playlist_id, platform: data.platform });
            }}>Save playlist</button
        >

        <a
            href="/queue"
            on:click={() => {
                setQueueIfQueueDiff();
            }}>Shuffle in queue</a
        >

        <TrackList
            tracklist={playlist.tracks}
            ifempty="Playlist is empty"
            trackclick={setQueueIfQueueDiff}
        />
    {/if}
</div>
