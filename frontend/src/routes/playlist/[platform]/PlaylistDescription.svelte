<script lang="ts">
    export let description: string;
    let hideDesc: boolean = true;
</script>

{#if description}
    <div>
        <p class="playlist-description" class:ellipsis={hideDesc}>{description}</p>
        {#if hideDesc}
            <button on:click={() => (hideDesc = false)}>Show More</button>
        {:else}
            <button on:click={() => (hideDesc = true)}>Show Less</button>
        {/if}
    </div>
{/if}

<style>
    .playlist-description {
        white-space: pre-wrap;
    }
</style>
