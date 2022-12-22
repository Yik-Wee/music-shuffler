<!-- https://developers.google.com/youtube/iframe_api_reference -->

<script lang="ts">
    import {
        YouTubePlayerState,
        type YouTubePlayer,
        type YouTubePlayerEvent
    } from '../../types/YouTubePlayer';
    import { createEventDispatcher, onMount } from 'svelte';
    import { setPlayer, TrackQueue } from '../../stores';

    export let id: string | undefined = undefined;

    let player: YouTubePlayer;
    let playerId: string = 'youtube-player';

    let dispatch = createEventDispatcher();

    function onPlayerReady(event: YouTubePlayerEvent) {
        console.log('ready');
        event.target.playVideo();
    }

    function onPlayerStateChange(event: YouTubePlayerEvent) {
        switch (event.data) {
            case YouTubePlayerState.ENDED:
                console.log('youtube video ended');
                TrackQueue.loadNext();
                break;
            default:
                console.log(event.data, YouTubePlayerState[event.data]);
                break;
        }
    }

    onMount(() => {
        function onYouTubeIframeAPIReady() {
            if (!(window as any).YT) {
                throw new Error('window.YT is undefined');
            }

            player = new (window as any).YT.Player(playerId, {
                height: '100%',
                width: '100%',
                videoId: '',
                events: {
                    onReady: onPlayerReady,
                    onStateChange: onPlayerStateChange
                }
            });

            setPlayer('youtube', player);

            // players.youtube = player;
            dispatch('load', {
                text: 'YouTube player loaded'
            });
        }

        // @ts-ignore Property 'onYouTubeIframeAPIReady' does not exist on type 'Window & typeof globalThis'
        window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;

        // add the script tag after the on iframe ready function has been defined to prevent race condition
        let tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        tag.async = true;
        let container = document.getElementById('yt-iframe-api-container');
        container?.append(tag);
    });
</script>

<div {id}>
    <div id="yt-iframe-api-container" />
    <div id="{playerId}" />
</div>
