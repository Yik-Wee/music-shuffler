<script lang="ts">
    export let title: string;
    export let thumbnail: string;
    export let owner: string;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div on:click>
    {#if thumbnail}
        <img src="{thumbnail}" alt="{title} by {owner}">
    {/if}
    <p>Title: {title}</p>
    <p>Owner: {owner}</p>
</div>