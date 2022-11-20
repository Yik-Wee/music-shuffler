<script type="ts">
    import type { PageData } from './$types';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import {
        isErrorResponse,
        toPlaylistInfo,
        type PlaylistResponse,
    } from '../../../types/PlaylistTracks';
    import { getPlaylist } from '../../../requests';
    import Track from '../../../components/Track.svelte';
    import { TrackQueue } from '../../../stores';

    export let data: PageData;
    let id: string;
    let err: string | undefined;
    // let playlistInfo: PlaylistInfoResponse | undefined;
    let playlist: PlaylistResponse | undefined;

    
    onMount(async () => {
        id = $page.url.searchParams.get('id') || '';

        // request data from API endpoint for specified platform
        // let res = await getPlaylistInfo(data.platform, id);
        let res = await getPlaylist(data.platform, id);
        if (isErrorResponse(res)) {
            err = res.error;
        } else {
            // playlistInfo = res;
            playlist = res
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

        <a href="/queue" on:click={() => {
            if (!playlist) {
                return;
            }

            // check if current playlist already playing in queue
            let queueIds = TrackQueue.playlists().map(p => p.playlist_id);
            if (queueIds.length !== 1 || queueIds[0] !== id) {
                // set current playlist to play in queue
                TrackQueue.setQueue(playlist.tracks, [toPlaylistInfo(playlist)]);
            }
        }}>Shuffle in queue</a>

        {#each playlist.tracks as track, position}
            <Track {...track} on:click={() => {
                if (!playlist) {
                    return;
                }

                // check if current playlist already playing in queue
                let queueIds = TrackQueue.playlists().map(p => p.playlist_id);
                if (queueIds.length !== 1 || queueIds[0] !== id) {
                    // set current playlist to play in queue
                    TrackQueue.setQueue(playlist.tracks, [toPlaylistInfo(playlist)]);
                }

                // play the track
                TrackQueue.load(position)
                TrackQueue.play();
            }} />
        {:else}
            <p>Playlist is empty</p>
        {/each}
    {/if}
</div>