<script type="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { isErrorResponse, type PlaylistInfoResponse } from '../../types/PlaylistTracks';
    import { getPlaylistInfo } from '../../requests';
    import PlaylistCard from '../../components/PlaylistCard.svelte';
    import { afterNavigate } from '$app/navigation';

    let id: string;
    let platform: string;
    let err: string | undefined;
    let playlistInfo: PlaylistInfoResponse | undefined;
    let link: HTMLAnchorElement;

    async function update() {
        id = $page.url.searchParams.get('id')?.trim() || '';
        platform = $page.url.searchParams.get('platform')?.trim() || '';

        if (!id) {
            err = 'No id specified';
            return;
        }

        if (!platform) {
            err = 'No platform specified';
            return;
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

<div>
    <h1>{platform}</h1>
    {#if id}
        {#if err}
            <div>{err}</div>
        {/if}

        <div>(Debug) PlaylistID: {id}</div>
    {:else}
        <div>Search for a {platform} playlist with it's playlist ID!</div>
    {/if}

    {#if playlistInfo}
        <PlaylistCard
            {...playlistInfo}
            --width="75%"
            --height="{height}px"
            --thumbnail-height="{0.6 * height}px"
            on:click={() => link.click()}
        />
        <a href="/playlist/{platform}?id={id}" bind:this={link}>Play</a>
    {/if}
</div>