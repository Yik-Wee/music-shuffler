<script lang="ts">
    import Highlighter from '../Highlighter.svelte';

    export let track_id: string;
    export let platform: string;
    export let title: string;
    export let owner: string;
    export let thumbnail: string | undefined = undefined;
    export let duration_seconds: number | undefined = undefined;

    export let position: number;

    export let loaded: boolean = true;

    export let highlight: string = '';
    export let highlightColor: string = 'lightgreen';

    function fmtDuration(seconds: number): string {
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = Math.round(seconds % 60);

        let hrsStr = hrs.toString().padStart(2, '0');
        let minsStr = mins.toString().padStart(2, '0');
        let secsStr = secs.toString().padStart(2, '0');

        let fmt = `${minsStr}:${secsStr}`;
        if (hrs > 0) {
            fmt = `${hrsStr}:${fmt}`;
        }

        return fmt;
    }

    // duration in hrs:mm:ss
    let durationString: string = duration_seconds ? fmtDuration(duration_seconds) : '';
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="track track-layout" data-track-id={track_id} data-track-platform={platform} on:click>
    {#if loaded}
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
                {#if highlight}
                    <Highlighter
                        text={title}
                        {highlight}
                        {highlightColor}
                    />
                {:else}
                    <span>{title}</span>
                {/if}
            </div>
            <div class="ellipsis">
                {#if highlight}
                    <Highlighter
                        text={owner}
                        {highlight}
                        {highlightColor}
                    />
                {:else}
                    <span>{owner}</span>
                {/if}
            </div>
        </div>
        <div class="ellipsis">
            <span>{durationString}</span>
        </div>
    {/if}
</div>

<style>
    @import './track-layout.css';

    .track {
        background-color: var(--mid-blue);
        cursor: pointer;
        transition: background-color 100ms ease-in;
    }

    .track:hover {
        background-color: var(--light-blue);
    }
</style>
