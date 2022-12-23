<script lang="ts">
    export let text: string;
    export let highlight: string;
    export let highlightColor: string;

    $: idxStart = text.toLocaleLowerCase().indexOf(highlight.toLocaleLowerCase());

    // highlighted subtext is found in original text
    $: idxEnd = idxStart + highlight.length;
</script>

{#if idxStart === -1}
    <span>{text}</span>
{:else}
    <span class="no-gap">
        <span>{text.substring(0, idxStart)}</span>
        <span style="background-color: {highlightColor}; border-radius: 2px; margin: 0;">
            {text.substring(idxStart, idxEnd)}
        </span>
        <span>{text.substring(idxEnd)}</span>
    </span>
{/if}

<style>
    .no-gap {
        display: flex;
        flex-direction: row;
        white-space: pre;
    }
</style>
