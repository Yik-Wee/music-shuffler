type SpotifyIframeEventData = {
    payload?: {
        duration: number; // total duration of song (NOT in seconds)
        isBuffering: boolean;
        isPaused: boolean;
        position: number; // current timestamp in the song (NOT in seconds)
    };
    type: string;
};

function isSpotifyIframeEventData(
    data: SpotifyIframeEventData | object
): data is SpotifyIframeEventData {
    return (data as SpotifyIframeEventData) !== undefined;
}

function isIframe(element: HTMLElement): element is HTMLIFrameElement {
    return (element as HTMLIFrameElement) !== undefined;
}

type SpotifyEventCallback = {
    (target: SpotifyPlayer): void;
};

type PlayerOptions = {
    onEnded: SpotifyEventCallback;
    onReady: SpotifyEventCallback;
};

class SpotifyPlayer {
    private static isOnMessageCreated: boolean = false;

    // isEnded: boolean = false;
    private _isPaused: boolean = true;

    public get isPaused(): boolean {
        return this._isPaused;
    }

    private set isPaused(value: boolean) {
        this._isPaused = value;
    }

    private iframe: HTMLIFrameElement;
    private onEnded: SpotifyEventCallback;
    private onReady: SpotifyEventCallback;

    constructor(iframeId: string, options: PlayerOptions) {
        let iframe = document.getElementById(iframeId);
        if (!iframe) {
            throw new Error(`Couldn\'t create new SpotifyPlayer: no iframe with id ${iframeId}`);
        }

        if (!isIframe(iframe)) {
            throw new Error(
                `Couldn\'t create new SpotifyPlayer: element with id ${iframeId} is not an iframe`
            );
        }

        this.iframe = iframe;
        this.onEnded = options.onEnded;
        this.onReady = options.onReady;

        if (!SpotifyPlayer.isOnMessageCreated) {
            window.addEventListener('message', (e: MessageEvent) => {
                if (e.origin === 'https://open.spotify.com') {
                    this.handleIframeMessage(e);
                }
            });
            SpotifyPlayer.isOnMessageCreated = true;
        }
    }

    loadTrack(trackId: string) {
        this.iframe.src = `https://open.spotify.com/embed/track/${trackId}`;
    }

    playTrack() {
        if (this.isPaused) {
            this.toggle();
        }
    }

    pauseTrack() {
        if (!this.isPaused) {
            this.toggle();
        }
    }

    /**
     * Reference: https://stackoverflow.com/questions/71979852/how-to-play-and-pause-spotify-embed-with-javascript
     *
     * Toggles between play and pause. Requires the spotify iframe to have already been manually
     * focussed e.g. user manually clicked on the iframe
     */
    toggle() {
        this.iframe.contentWindow?.postMessage({ command: 'toggle' }, '*');
    }

    // --private methods--
    private handleIframeMessage(e: MessageEvent<SpotifyIframeEventData | object>) {
        console.log(e);

        if (!isSpotifyIframeEventData(e.data)) {
            return;
        }

        if (e.data.type === 'ready') {
            this.isPaused = true;
            this.onReady(this);
            return;
        }

        if (!e.data.payload) {
            return;
        }

        let { duration, position, isBuffering, isPaused } = e.data.payload;

        if (isBuffering) {
            return;
        }

        // track has ended
        if (position >= duration) {
            // this.isEnded = true;
            this.onEnded(this);
        }

        // changed from pause -> play, or play -> pause. Update accordingly
        if (isPaused !== this.isPaused) {
            this.isPaused = isPaused;
        }
    }
}

export default SpotifyPlayer;
