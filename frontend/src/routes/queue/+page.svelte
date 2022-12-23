<script lang="ts">
    import { TrackQueue } from '../../stores';
    import TrackList from '../../components/Tracks/TrackList.svelte';

    let tracklist = TrackQueue.tracklist();
</script>

<div>
    <button
        on:click={() => {
            TrackQueue.shuffle();
            tracklist = TrackQueue.tracklist();
        }}>Shuffle</button
    >
    <TrackList {tracklist} ifempty="Queue is empty" />
</div>
