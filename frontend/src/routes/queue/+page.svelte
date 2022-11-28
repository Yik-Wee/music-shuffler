<script lang="ts">
    import { TrackQueue } from '../../stores';
    import TrackList from '../../components/TrackList.svelte';

    let tracklist = TrackQueue.tracklist();
</script>

<div>
    <button
        on:click={() => {
            console.log('clicked');
            TrackQueue.shuffle();
            tracklist = TrackQueue.tracklist();
            console.log(tracklist.map(({ title }) => title));
        }}>Shuffle</button
    >
    <TrackList {tracklist} ifempty="Queue is empty" />
</div>
