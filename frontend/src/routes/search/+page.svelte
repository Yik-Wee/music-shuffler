<script type="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import {
        isErrorResponse,
        type PlaylistInfoResponse,
    } from '../../types/PlaylistTracks';
    import { getPlaylistInfo } from '../../requests';
    import PlaylistCard from '../../components/PlaylistCard.svelte';

    let id: string;
    let platform: string;
    let err: string | undefined;
    let playlistInfo: PlaylistInfoResponse | undefined;
    let link: HTMLAnchorElement;

    onMount(async () => {
        id = $page.url.searchParams.get('id')?.trim() || '';
        if (!id) {
            err = 'No id specified';
            return;
        }

        platform = $page.url.searchParams.get('platform')?.trim() || '';
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
    });
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
        <PlaylistCard {...playlistInfo} on:click={() => link.click()} />
        <a href="/playlist/{platform}?id={id}" bind:this={link}>Play</a>
    {/if}
</div>