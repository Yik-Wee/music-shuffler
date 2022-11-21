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
<div class="track" data-track-id={track_id} data-track-platform={platform} on:click>
    <div class="track-position">
        {position}
    </div>
    <div class="track-thumbnail">
        {#if thumbnail}
            <img src={thumbnail} alt="{title} by {owner}" width="40px" />
        {/if}
    </div>
    <div class="track-title">
        <span>{title}</span>
    </div>
    <div class="track-owner">
        <span>{owner}</span>
    </div>
    <div class="track-duration">
        <p>{durationString}</p>
    </div>
</div>

<style>
    .track {
        border: 1px solid transparent;
        border-radius: 4px;
        height: 60px;
        position: relative;
        column-gap: 8px;
        display: grid;
        padding: 0 16px;
        grid-template-columns: [index] 8px [first] 40px [var1] 2.75fr [var2] 1.75fr [last] 0.25fr;
        align-items: center;
        background-color: whitesmoke;
        cursor: pointer;
        transition: background-color 100ms ease-in;
    }

    .track:hover {
        background-color: lightblue;
    }

    /* TODO wrap 2 lines then ellipses */
    .track > .track-title,
    .track > .track-owner {
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }
</style>
