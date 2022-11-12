<!-- https://developers.soundcloud.com/docs/api/html5-widget -->
<script lang="ts">
    import { containerIds, players } from '../../stores';
    import type { WidgetConstructor } from '../../types/SoundCloudPlayer';
    import { onMount } from 'svelte';

    onMount(() => {
        // @ts-ignore
        let Widget: WidgetConstructor = window.SC.Widget;
        let player = Widget('soundcloud-player-iframe');
        // soundcloudPlayer.set(player);
        players.soundcloud = player;
    });
</script>

<div id="{containerIds.soundcloud}">
    <script src="https://w.soundcloud.com/player/api.js" async></script>
    <iframe
        title="insert title here"
        id="soundcloud-player-iframe"
        width="100%"
        height="166"
        scrolling="no"
        frameborder="no"
        allow="autoplay"
        src="https://w.soundcloud.com/player/?url=https://soundcloud.com/uyn_yn/school-acoustic-ver"
    />
    <!-- src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/293&amp;" -->
</div>
