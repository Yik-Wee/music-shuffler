// https://developers.google.com/youtube/iframe_api_reference

interface YouTubePlayer {
    loadVideoById(videoId: string, startSeconds?: number | undefined): void;
    playVideo(): void;
    pauseVideo(): void;
    seekTo(seconds: number, allowSeekAhead: boolean): void;
    mute(): void;
    unMute(): void;
    isMuted(): boolean;
    setSize(width: number, height: number): object;
    getPlayerState(): number;
    getIframe(): HTMLIFrameElement;
    destroy(): void;
    // ...
}

enum YouTubePlayerState {
    UNSTARTED = -1,
    ENDED,
    PLAYING,
    PAUSED,
    BUFFERING,
    CUED,
}

type YouTubePlayerEvent = {
    target: YouTubePlayer,
    /**
     * The player state, given by `YT.PlayerState` or `YouTubePlayerState`
     */
    data: number,
}

export { type YouTubePlayer, YouTubePlayerState, type YouTubePlayerEvent };
