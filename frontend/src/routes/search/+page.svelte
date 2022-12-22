<script type="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { isErrorResponse, type PlaylistInfoResponse } from '../../types/PlaylistTracks';
    import { getPlaylistInfo } from '../../requests';
    import PlaylistCard from '../../components/LibraryItem.svelte';
    import { afterNavigate, goto } from '$app/navigation';
    import { SoundCloud } from '../../url';

    let id: string;
    let platform: string;
    let domain: string;
    let err: string | undefined;
    let playlistInfo: PlaylistInfoResponse | undefined;

    async function update() {
        id = $page.url.searchParams.get('id')?.trim() || '';
        platform = $page.url.searchParams.get('platform')?.trim() || '';
        domain = $page.url.searchParams.get('domain')?.trim() || '';

        if (!id) {
            err = 'No id specified';
            return;
        }

        if (!platform) {
            err = 'No platform specified';
            return;
        }

        if (domain === 'on.soundcloud.com') {
            // check if domain is on.soundcloud.com (shortened link)
            // convert the path to the canonical permalink_url used as the id
            let reCanonicalUrl =
                /<link rel="canonical" href="(https:\/\/soundcloud\.com\/[^"]*)">/gim;
            let res = await fetch(`https://on.soundcloud.com/${id}`);
            let text = await res.text();
            if (!res.ok) {
                err = text;
                return;
            }

            let matches = reCanonicalUrl.exec(text);
            if (matches?.length !== 2) {
                err = 'Playlist not found';
                return;
            }

            let canonicalUrl = matches[1];
            let canonicalPath = SoundCloud.parsePath(canonicalUrl);
            if (!canonicalPath) {
                err = 'Playlist not found';
                return;
            }

            id = canonicalPath;
        }

        // request data from API endpoint for specified platform
        let res = await getPlaylistInfo(platform, id);
        if (isErrorResponse(res)) {
            err = res.error;
        } else {
            playlistInfo = res;
        }
    }

    // onMount for Server Side Routed page load
    onMount(update);

    // afterNavigate for Client Side Routed page load
    afterNavigate(update);

    /** height of the PlaylistCard in px */
    let height: number = 240;
</script>

<div class="search-results">
    <h1>Results for {platform} playlist "{id}"</h1>
    {#if playlistInfo}
        <PlaylistCard
            {...playlistInfo}
            --width="75%"
            --height="{height}px"
            --thumbnail-height="{0.6 * height}px"
            on:click={() => goto(`/playlist/${platform}?id=${id}`)}
        />
    {:else if err}
        <p>{err}</p>
    {/if}
</div>

<style>
    .search-results {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>