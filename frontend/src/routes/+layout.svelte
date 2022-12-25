<script lang="ts">
    import Navigation from '../components/Navigation/Navigation.svelte';
    import Player from '../components/Player/Player.svelte';
    import { TrackQueue } from '../stores';
    import { onMount } from 'svelte';

    let loaded = false;
    let prerenderedServerSideRoutes: HTMLDivElement;

    function onPlayerLoad(e: CustomEvent) {
        console.info(e.detail);
        loaded = true;
        TrackQueue.hideAll();
    }

    onMount(async () => {
        prerenderedServerSideRoutes.remove();
        await TrackQueue.loadCachedQueue();
    });
</script>

<svelte:head>
    <link rel="stylesheet" href="/css/global.css" />
</svelte:head>

<Navigation />
<main>
    <Player on:load={onPlayerLoad} />
    <div class="player-controls">
        <button class="prev" on:click={() => TrackQueue.loadPrev()}>Prev</button>
        <button class="toggle" on:click={() => TrackQueue.toggle()}>Play/Pause</button>
        <button class="next" on:click={() => TrackQueue.loadNext()}>Next</button>
    </div>
    <div class="content">
        {#if loaded}
            <slot />
        {/if}
    </div>
</main>

<!-- svelte-ignore a11y-missing-content -->
<div hidden bind:this={prerenderedServerSideRoutes}>
    <a href="/playlist/youtube"></a>
    <a href="/playlist/spotify"></a>
    <a href="/playlist/soundcloud"></a>
</div>

<style>
    .content {
        padding: 8px;
        width: 90%;
        /* background-color: var(--mid-blue); */
        color: var(--ivory);
        margin: auto;
    }

    @media screen and (min-width: 768px) {
        main {
            margin-top: calc(10vh + 8px + 4px);
        }
    }

    @media screen and (max-width: 768px) {
        main {
            margin-top: calc(7vh + 8px + 4px);
            height: calc(100vh - (7vh + 8px + 4px));
        }
    }
</style>
