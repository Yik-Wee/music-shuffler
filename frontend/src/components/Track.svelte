<script lang="ts">
    export let track_id: string;
    export let platform: string;
    export let title: string;
    export let owner: string;
    export let thumbnail: string | undefined = undefined;
    export let duration_seconds: number | undefined = undefined;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div on:click>
    {#if thumbnail}
        <img src="{thumbnail}" alt="{title} by {owner}" width="100px">
    {/if}
    <p>TrackID: {track_id}</p>
    <p>Platform: {platform}</p>
    <p>Title: {title}</p>
    <p>Owner: {owner}</p>
    <p>Duration: {duration_seconds} seconds</p>
</div>