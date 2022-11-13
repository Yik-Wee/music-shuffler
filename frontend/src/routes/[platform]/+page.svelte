<script type="ts">
    import type { PageData } from './$types';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { isErrorResponse, type PlaylistResponse } from '../../types/PlaylistTracks';
    import { getPlaylist } from './requests';

    export let data: PageData;
    let id: string;
    let err: string | undefined;
    let playlist: PlaylistResponse | undefined;

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

        <div>(Debug) PlaylistID: {id}</div>
    {:else}
        <div>Search for a {data.platform} playlist with it's playlist ID!</div>
    {/if}

    {#if playlist}
        <div data-playlist-id={playlist.playlist_id} class="playlist-renderer">
            <h2>{playlist.owner}</h2>
            <h2>{playlist.title} ({playlist.length} Tracks)</h2>
            <div>
                <p class="playlist-description-ellipses">{playlist.description}</p>
            </div>
            <img
                src={playlist.thumbnail}
                alt="{playlist.owner} - {playlist.title}"
                class="playlist-thumbnail"
            />
            {#each playlist.tracks as track}
                <div data-track-id={track.track_id} class="track-renderer">
                    <p>{track.owner}</p>
                    <p>{track.title}</p>
                    <p>TrackID: {track.track_id}</p>
                    {#if track.duration_seconds}
                        <p>{track.duration_seconds} seconds</p>
                    {/if}
                    <img
                        src={track.thumbnail}
                        alt="{track.owner} - {track.title}"
                        class="track-thumbnail"
                    />
                </div>
            {/each}
        </div>
    {/if}
</div>
