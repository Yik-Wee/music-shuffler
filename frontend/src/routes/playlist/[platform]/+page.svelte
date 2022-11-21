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
    import { TrackQueue } from '../../../stores';
    import TrackList from '../../../components/TrackList.svelte';

    export let data: PageData;
    let id: string;
    let err: string | undefined;
    // let playlistInfo: PlaylistInfoResponse | undefined;
    let playlist: PlaylistResponse | undefined;

    function isNotAlreadyInQueue(): boolean {
        let queueIds = TrackQueue.playlists().map(p => p.playlist_id);
        return queueIds.length !== 1 || queueIds[0] !== id;
    }

    function setQueueIfQueueDiff() {
        if (isNotAlreadyInQueue() && playlist) {
            // set current playlist to play in queue
            TrackQueue.setQueue(playlist.tracks, [toPlaylistInfo(playlist)]);
        }
    }

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

        <button on:click={() => {
            if (!playlist) {
                return;
            }

            // save playlist to localStorage
            let savedRaw = localStorage.getItem('savedPlaylists');
            if (!savedRaw) {
                localStorage.setItem('savedPlaylists', `[${playlist.playlist_id}]`);
                return;
            }

            // check if this playlist alr saved
            let saved;
            try {
                saved = JSON.parse(savedRaw);
            } catch (err) {
                // json decode error => overwrite savedPlaylists
                localStorage.setItem('savedPlaylists', `[${playlist.playlist_id}]`);
                return;
            }

            if (!(Array.isArray(saved))) {
                localStorage.setItem('savedPlaylists', `[${playlist.playlist_id}]`);
                return;
            }

            let item = `${data.platform}:${playlist.playlist_id}`;
            if (saved.includes(item)) {
                console.log('Playlist already saved to library');
                return;
            };

            saved.push(item);
            localStorage.setItem('savedPlaylists', JSON.stringify(saved));
        }}>Save playlist</button>

        <a href="/queue" on:click={() => {
            setQueueIfQueueDiff();
        }}>Shuffle in queue</a>

        <TrackList tracklist={playlist.tracks} ifempty="Playlist is empty" trackclick={setQueueIfQueueDiff} />
    {/if}
</div>