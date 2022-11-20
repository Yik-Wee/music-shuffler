<script lang="ts">
    import { containerId } from "../../stores";
    import { createEventDispatcher } from "svelte";
    import SoundCloudPlayer from "./SoundCloudPlayer.svelte";
    import SpotifyPlayer from "./SpotifyPlayer.svelte";
    import YouTubePlayer from "./YouTubePlayer.svelte";

    let dispatch = createEventDispatcher();

    // number of players loaded
    let count = 0;
    function onLoad(e: CustomEvent) {
        count++;
        console.info(e.detail.text);
        if (count === 3) {
            dispatch('load', 'Players loaded');
        }
    }
</script>

<div id="players">
    <SoundCloudPlayer id="{containerId('soundcloud')}" on:load={onLoad} />
    <SpotifyPlayer id="{containerId('spotify')}" on:load={onLoad} />
    <YouTubePlayer id="{containerId('youtube')}" on:load={onLoad} />
</div>