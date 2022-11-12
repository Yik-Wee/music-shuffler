// import { writable, type Writable } from 'svelte/store';
import type { SoundCloudPlayer } from './types/SoundCloudPlayer';
import type SpotifyPlayer from './types/SpotifyPlayer';
import { YouTubePlayerState, type YouTubePlayer } from './types/YouTubePlayer';

// export let youtubePlayer: Writable<YouTubePlayer | undefined> = writable(undefined);
// export let spotifyPlayer: Writable<SpotifyPlayer | undefined> = writable(undefined);
// export let soundcloudPlayer: Writable<SoundCloudPlayer | undefined> = writable(undefined);

type Players = {
    youtube: YouTubePlayer | undefined;
    spotify: SpotifyPlayer | undefined;
    soundcloud: SoundCloudPlayer | undefined;
    controller: PlayerController | undefined;
};

export let players: Players = {
    youtube: undefined,
    spotify: undefined,
    soundcloud: undefined,
    controller: undefined
};

export const playerNames = ['youtube', 'spotify', 'soundcloud'];

export const containerIds = {
    youtube: 'youtube-player-container',
    spotify: 'spotify-player-container',
    soundcloud: 'soundcloud-player-container'
};

function setContainerHidden(id: string, hidden: boolean): void {
    let container = document.getElementById(id);
    if (container) {
        container.hidden = hidden;
        // container.setAttribute('display', hidden ? 'none' : 'initial');
    }
}

interface Player {
    load(trackId: string, start?: number): void;
    play(): void;
    pause(): void;
    toggle(): void;
    show(): void;
    hide(): void;
}

class YouTubePlayerWrapper implements Player {
    load(trackId: string, start?: number | undefined): void {
        players.youtube?.loadVideoById(trackId, start);
    }

    play(): void {
        players.youtube?.playVideo();
    }

    pause(): void {
        players.youtube?.pauseVideo();
    }

    toggle(): void {
        if (players.youtube?.getPlayerState() === YouTubePlayerState.PAUSED) {
            this.play();
        } else {
            this.pause();
        }
    }

    show(): void {
        setContainerHidden(containerIds.youtube, false);
    }

    hide(): void {
        setContainerHidden(containerIds.youtube, true);
    }
}

class SpotifyPlayerWrapper implements Player {
    load(trackId: string, start?: number | undefined): void {
        players.spotify?.loadTrack(trackId);
    }

    play(): void {
        players.spotify?.playTrack();
    }

    pause(): void {
        players.spotify?.pauseTrack();
    }

    toggle(): void {
        if (players.spotify?.isPaused) {
            this.play();
        } else {
            this.pause();
        }
    }

    show(): void {
        setContainerHidden(containerIds.spotify, false);
    }

    hide(): void {
        setContainerHidden(containerIds.spotify, true);
    }
}

class SoundCloudPlayerWrapper implements Player {
    load(trackId: string, start?: number | undefined): void {
        players.soundcloud?.load(`https://soundcloud.com/tracks/${trackId}`, { auto_play: true });
    }

    play(): void {
        players.soundcloud?.play();
    }

    pause(): void {
        players.soundcloud?.pause();
    }

    toggle(): void {
        players.soundcloud?.isPaused((paused) => {
            if (paused) {
                this.play();
            } else {
                this.pause();
            }
        });
    }

    show(): void {
        setContainerHidden(containerIds.soundcloud, false);
    }

    hide(): void {
        setContainerHidden(containerIds.soundcloud, true);
    }
}

type Controllers = {
    youtube: YouTubePlayerWrapper;
    spotify: SpotifyPlayerWrapper;
    soundcloud: SoundCloudPlayerWrapper;
};

export class PlayerController implements Player {
    controllers: Controllers = {
        youtube: new YouTubePlayerWrapper(),
        spotify: new SpotifyPlayerWrapper(),
        soundcloud: new SoundCloudPlayerWrapper()
    };

    key: string = 'youtube';

    currentPlayer(): Player | undefined {
        return this.controllers[this.key as keyof Controllers];
    }

    load(trackId: string, start?: number | undefined): void {
        this.currentPlayer()?.load(trackId, start);
    }

    play(): void {
        this.currentPlayer()?.play();
    }

    toggle(): void {
        this.currentPlayer()?.toggle();
    }

    pause(): void {
        this.currentPlayer()?.pause();
    }

    show(): void {
        this.currentPlayer()?.show();
    }

    hide(): void {
        this.currentPlayer()?.hide();
    }

    swapPlayer(name: string): void {
        if (!Object.keys(this.controllers).includes(name)) return;

        this.key = name;
        this.show();
        for (let key in this.controllers) {
            if (key !== this.key) {
                let p = this.controllers[key as keyof Controllers];
                p.pause();
                p.hide();
            }
        }
    }

    hideAll(): void {
        for (let key in this.controllers) {
            this.controllers[key as keyof Controllers].hide();
        }
    }
}
