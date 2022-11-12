<!-- https://developers.google.com/youtube/iframe_api_reference -->
<script lang="ts">
    import { containerIds, players } from '../../stores';
    import {
        YouTubePlayerState,
        type YouTubePlayer,
        type YouTubePlayerEvent
    } from '../../types/YouTubePlayer';
    import { onMount } from 'svelte';

    let player: YouTubePlayer | undefined;

    function onPlayerReady(event: YouTubePlayerEvent) {
        // ...
        console.log('ready');
        event.target.playVideo();
    }

    function onPlayerStateChange(event: YouTubePlayerEvent) {
        console.log(event.data, YouTubePlayerState[event.data]);
    }

    onMount(() => {
        function onYouTubeIframeAPIReady() {
            if (!(window as any).YT) {
                throw new Error('window.YT is undefined');
            }

            player = new (window as any).YT.Player('youtube-player', {
                height: '130',
                width: '290',
                videoId: 'gdZLi9oWNZg', // haha bts lol funny hehee ahaha
                // playerVars: {
                //     playsinline: 1
                // },
                events: {
                    onReady: onPlayerReady,
                    onStateChange: onPlayerStateChange
                }
            });
            // youtubePlayer.set(player);
            players.youtube = player;
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

<div id="{containerIds.youtube}">
    <div id="yt-iframe-api-container" />
    <div id="youtube-player" />
</div>
