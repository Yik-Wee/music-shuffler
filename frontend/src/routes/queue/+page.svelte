<script lang="ts">
    import { TrackQueue } from "../../stores";
    import Track from "../../components/Track.svelte";

    let tracklist = TrackQueue.tracklist();
</script>

<div>
    <div id="queue-playlist-info">
        {#each TrackQueue.playlists() as { playlist_id, title, owner, thumbnail }}
            <div class="playlist-info-shortened">
                {#if thumbnail}
                    <img src="{thumbnail}" alt="{title} by {owner}" width="200px">
                {/if}
                <p>{playlist_id}</p>
                <p>{title}</p>
                <p>{owner}</p>
            </div>
        {/each}
    </div>

    <button on:click={() => {
        console.log('clicked');
        TrackQueue.shuffle();
        tracklist = TrackQueue.tracklist();
        console.log(tracklist.map(({ title }) => title));
    }}>Shuffle</button>

    {#each tracklist as track, position}
        <Track {...track} on:click={() => {
            TrackQueue.load(position);
            TrackQueue.play();
        }}/>
    {:else}
        <h1>No tracks in the queue</h1>
    {/each}
</div>