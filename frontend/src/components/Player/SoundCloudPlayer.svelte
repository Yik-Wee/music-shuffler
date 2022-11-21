<!-- https://developers.soundcloud.com/docs/api/html5-widget -->
<script lang="ts">
    import type { SoundCloudPlayer, WidgetType } from "../../types/SoundCloudPlayer";
    import { createEventDispatcher, onMount, setContext } from "svelte";
    import { setPlayer, TrackQueue } from "../../stores";

    export let id: string | undefined = undefined;

    let iframeId: string = 'soundcloud-player-iframe';
    let player: SoundCloudPlayer;

    let dispatch = createEventDispatcher();

    // setContext('soundcloud', {
    //     getPlayer: () => player,
    // });

    onMount(() => {
        // @ts-ignore
        let Widget: WidgetType = window.SC.Widget;
        player = Widget(iframeId);
        player.bind(Widget.Events.READY, () => { player.play() });
        player.bind(Widget.Events.FINISH, () => {
            TrackQueue.loadNext();
        });

        setPlayer('soundcloud', player);

        dispatch('load', {
            text: 'SoundCloud player loaded'
        });
    });
</script>

<div {id}>
    <script src="https://w.soundcloud.com/player/api.js" async></script>
    <iframe
        title="SoundCloud Player"
        id={iframeId}
        width="100%"
        height="166"
        scrolling="no"
        frameborder="no"
        allow="autoplay"
        src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/"
    />
</div>
<!-- src="https://w.soundcloud.com/player/?url=https://soundcloud.com/uyn_yn/school-acoustic-ver" -->
<!-- src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/293&amp;" -->
