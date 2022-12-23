<script type="ts">
    import type { PageData } from './$types';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { isErrorResponse, type PlaylistResponse } from '../../../types/PlaylistTracks';
    import { getPlaylist } from '../../../requests';
    import { TrackQueue } from '../../../stores';
    import TrackList from '../../../components/Tracks/TrackList.svelte';
    import { savePlaylist } from '../../../library';

    export let data: PageData;
    let id: string;
    let err: string | undefined;
    let playlist: PlaylistResponse | undefined;

    let hideDesc: boolean = true;

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
        if (!id) {
            return;
        }

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
    {#if playlist}
        <div data-playlist-id={playlist.playlist_id} class="playlist-renderer">
            <h2>{playlist.owner}</h2>
            <h2>{playlist.title}</h2>
            {#if playlist.description}
                <div>
                    <p class="playlist-description" class:ellipsis={hideDesc}>{playlist.description}</p>
                    {#if hideDesc}
                        <button on:click={() => hideDesc = false}>Show More</button>
                    {:else}
                        <button on:click={() => hideDesc = true}>Show Less</button>
                    {/if}
                </div>
            {/if}
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
    {:else if err}
        <h2>An error occurred :/</h2>
        <p>{err}</p>
    {:else if !id}
        <p>Search for a {data.platform} playlist with it's playlist ID!</p>
    {:else}
        <p>Fetching tracks... This may take a while</p>
    {/if}
</div>

<style>
    .playlist-description {
        white-space: pre-wrap;
    }

    .playlist-thumbnail {
        max-height: 100px;
    }

    .ellipsis {
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }
</style>
