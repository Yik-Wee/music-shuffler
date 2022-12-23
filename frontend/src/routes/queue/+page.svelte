<script lang="ts">
    import { TrackQueue } from '../../stores';
    import TrackList from '../../components/Tracks/TrackList.svelte';

    let tracklist = TrackQueue.tracklist();
    let loading = TrackQueue.isQueueLoading;

    loading.subscribe((value) => {
        if (value === false) {
            tracklist = TrackQueue.tracklist();
        }
    })
</script>

<div>
    <button
        on:click={() => {
            TrackQueue.shuffle();
            tracklist = TrackQueue.tracklist();
        }}>Shuffle</button
    >
    {#if $loading}
        <TrackList {tracklist} ifempty="Loading..." />
    {:else}
        <TrackList {tracklist} ifempty="Queue is empty" />
    {/if}
</div>
