<script lang="ts">
    export let track_id: string;
    export let platform: string;
    export let title: string;
    export let owner: string;
    export let thumbnail: string | undefined = undefined;
    export let duration_seconds: number | undefined = undefined;

    export let position: number;

    // duration in min:ss
    let durationString: string = duration_seconds
        ? `${Math.floor(duration_seconds / 60)}:${duration_seconds % 60}`
        : '';
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="track track-layout" data-track-id={track_id} data-track-platform={platform} on:click>
    <div class="track-position">
        {position}
    </div>
    <div class="ellipsis">
        {#if thumbnail}
            <img src={thumbnail} alt="{title} by {owner}" width="40px" />
        {/if}
    </div>
    <div class="ellipsis">
        <div class="ellipsis">
            <span>{title}</span>
        </div>
        <div class="ellipsis">
            <span>{owner}</span>
        </div>
    </div>
    <div class="ellipsis">
        <span>{durationString}</span>
    </div>
</div>

<style>
    :global(.track-layout) {
        border: 1px solid transparent;
        border-radius: 4px;
        height: 60px;
        position: relative;
        column-gap: 8px;
        padding: 0 16px;
        display: grid;
        grid-template-columns: 20px 40px 4fr minmax(0, 1fr);
        align-items: center;
    }

    .track {
        background-color: whitesmoke;
        cursor: pointer;
        transition: background-color 100ms ease-in;
    }

    .track:hover {
        background-color: lightblue;
    }
</style>
