import { writable, type Writable } from 'svelte/store';
import { findSavedMix } from './library';
import { getPlaylist } from './requests';
import { isErrorResponse, type PlaylistResponse, type Track } from './types/PlaylistTracks';
import { type SoundCloudPlayer, scGet } from './types/SoundCloudPlayer';
import type SpotifyPlayer from './types/SpotifyPlayer';
import { YouTubePlayerState, type YouTubePlayer } from './types/YouTubePlayer';

type Players = {
    youtube: YouTubePlayer | undefined;
    soundcloud: SoundCloudPlayer | undefined;
    spotify: SpotifyPlayer | undefined;
};

let players: Players = {
    youtube: undefined,
    soundcloud: undefined,
    spotify: undefined
};

let supportedPlatforms = Object.keys(players);

function setPlayer(key: string, player: any) {
    players[key as keyof typeof players] = player;
}

function getPlayer<T = YouTubePlayer | SoundCloudPlayer | SpotifyPlayer | undefined>(
    key: string
): T {
    return players[key as keyof typeof players] as T;
}

function containerId(player: string): string {
    let idPart = player.replaceAll(' ', '-');
    return `${idPart}-player-container`;
}

/**
 * The namespace containing functions to control the track queue
 */
namespace TrackQueue {
    type Queue = {
        position: number;
        tracklist: Track[];
        id: string;
        platform: string;
    };

    let queue: Queue = {
        position: 0,
        tracklist: [],
        id: '',
        platform: ''
    };

    export let isQueueLoading: Writable<boolean> = writable(false);

    function isString(value: any): value is string {
        return typeof value === 'string' || value instanceof String;
    }

    /**
     * Get the cached queue.
     * @returns {Promise<Queue>} The queue that was cached, or a default empty queue
     * no queue was cached or the cache was not found.
     */
    async function getCachedQueue(): Promise<Queue> {
        let raw = localStorage.getItem('queue');

        if (!raw) {
            console.log('No cached queue found');
            return queue;
        }

        let withoutTracks: any;
        try {
            withoutTracks = JSON.parse(raw);
        } catch {
            console.log('Unable to parse cached queue');
            return queue;
        }

        let { id, platform } = withoutTracks;
        let position = 0;
        let trackRaw = localStorage.getItem('last-played');
        let track = null;
        let trackId = '';
        let trackPlatform = '';

        if (trackRaw) {
            try {
                track = JSON.parse(trackRaw);
                trackId = track.track_id || '';
                trackPlatform = track.platform.toLowerCase() || '';
            } catch (err) {
                console.error(err);
                localStorage.removeItem('last-played');
            }
        }

        console.log(track, trackId, trackPlatform);

        if (!(isString(id) && isString(platform))) {
            console.log('Invalid cached queue types');
            return queue;
        }

        id = id.trim();
        // is not mix, just regular playlist
        if (supportedPlatforms.includes(platform.toLowerCase())) {
            let playlist = await getPlaylist(platform, id);
            if (isErrorResponse(playlist)) {
                console.log('Error fetching cached queue', playlist.error);
                return queue;
            }

            if (track) {
                position = playlist.tracks.findIndex(
                    (track) => track.track_id === trackId && track.platform.toLowerCase() === trackPlatform
                );
                if (position === -1) {
                    position = 0;
                }
                console.log('last played track at position', position);
            }
    
            console.log('cached queue was playlist. success');
            return {
                position,
                id,
                platform,
                tracklist: playlist.tracks
            };
        }

        if (platform.toLowerCase() !== 'mix') {
            console.log('cached queue invalid platform', platform);
            return queue;
        }

        // is mix. get mix tracks
        let savedMixInfo = findSavedMix(id);

        if (!savedMixInfo) {
            console.log('no cached queue mix with title', id);
            return queue;
        }

        let responses = await Promise.all(
            savedMixInfo.playlists.map(({ platform, id }) =>
                getPlaylist(platform.toLowerCase(), id)
            )
        );

        let tracklist: Track[] = [];

        tracklist = responses
            .filter((res): res is PlaylistResponse => {
                let isErr = isErrorResponse(res);
                if (isErr) {
                    console.error('Response error:', res);
                }
                return !isErr;
            })
            .map((playlist) => playlist.tracks)
            .reduce((flat, toFlatten) => flat.concat(toFlatten));

        if (track) {
            position = tracklist.findIndex(
                (track) => track.track_id === trackId && track.platform.toLowerCase() === trackPlatform
            );
            if (position === -1) {
                position = 0;
            }
            console.log('last played track at position', position);
        }

        console.log('cached queue was mix. success');

        return { position, tracklist, id, platform };
    }

    /**
     * Loads the most recently cached queue
     */
    export async function loadCachedQueue() {
        isQueueLoading.set(true);
        queue = await getCachedQueue();
        isQueueLoading.set(false);
        load(queue.position);
    }

    /**
     * Set/reset the queue to store the `tracklist` and `playlists` the tracks are from.
     * @param tracklist The list of tracks stored in the queue
     * @param id The id of the playlist, or unique title of the mix.
     * @param platform the platform of the playlist, or 'mix' if it is a mix
     */
    export function setQueue(tracklist: Track[], id: string, platform: string) {
        pause();
        queue.tracklist = tracklist;
        queue.position = 0;
        queue.id = id;
        queue.platform = platform;
        load(0);
        play();

        // cache the queue so it remains the same on reload
        localStorage.setItem('queue', JSON.stringify({ id, platform }));
    }

    /**
     * @returns {string} the id of the playlist or unique title of the mix in the queue
     */
    export function id(): string {
        return queue.id;
    }

    /**
     *
     * @returns {string} the platform of the playlist, or 'mix' if a mix is in the queue
     */
    export function platform(): string {
        return queue.platform;
    }

    /**
     * @returns {Track | null} the track currently being played in the queue or null if no track
     */
    export function nowPlaying(): Track | null {
        if (queue.position >= queue.tracklist.length || queue.position < 0) {
            return null;
        }

        return queue.tracklist[queue.position];
    }

    /**
     * @returns {Track[]} the list of tracks stored in the queue
     */
    export function tracklist(): Track[] {
        return queue.tracklist;
    }

    /**
     * Shuffles the queue's tracklist, setting the track now playing to be the first track in the queue
     */
    export function shuffle() {
        let n = queue.tracklist.length - 1;
        if (n <= 0) {
            return;
        }

        // set current track to the first position
        if (queue.position !== 0) {
            let idx = queue.position;
            [queue.tracklist[idx], queue.tracklist[0]] = [queue.tracklist[0], queue.tracklist[idx]];
            queue.position = 0;
        }

        for (let i = n; i > 1; i--) {
            let r = Math.floor(1 + Math.random() * (i - 1));
            [queue.tracklist[i], queue.tracklist[r]] = [queue.tracklist[r], queue.tracklist[i]];
        }
    }

    /**
     * Loads the track at the specified position in the tracklist
     * @param position the position of the track in the tracklist
     * @returns {boolean} `true` if loaded successfully, `false` otherwise
     */
    export function load(position: number): boolean {
        console.log(`load(${position})`, queue);
        if (position >= queue.tracklist.length || position < 0) {
            return false;
        }

        // pause the current track if the next track is playing in a different player
        pause();

        queue.position = position;

        // get track at new position
        let track = nowPlaying();
        if (track === null) {
            return false;
        }

        let platform = track.platform.toLowerCase();
        let player = getPlayer(platform);
        switch (platform) {
            case 'youtube':
                (player as YouTubePlayer).loadVideoById(track.track_id);
                break;
            case 'soundcloud':
                (player as SoundCloudPlayer).load(
                    `https://api.soundcloud.com/tracks/${track.track_id}`,
                    { auto_play: true }
                );
                break;
            case 'spotify':
                (player as SpotifyPlayer).loadTrack(track.track_id);
                break;
            default:
                return false;
        }
        swap(platform);

        localStorage.setItem('last-played', JSON.stringify(track));

        return true;
    }

    /**
     * Load the next track, relative to the current track playing
     * @returns {boolean} `true` if loaded successfully, `false` otherwise
     */
    export function loadNext(): boolean {
        return load(queue.position + 1);
    }

    /**
     * Load the previous track, relative to the current track playing
     * @returns {boolean} `true` if loaded successfully, `false` otherwise
     */
    export function loadPrev(): boolean {
        return load(queue.position - 1);
    }

    /**
     * Play the current track
     */
    export function play() {
        let track = nowPlaying();
        if (track === null) {
            return;
        }

        let platform = track.platform.toLowerCase();
        let player = getPlayer(platform);

        switch (platform) {
            case 'youtube':
                (player as YouTubePlayer).playVideo();
                break;
            case 'soundcloud':
                (player as SoundCloudPlayer).play();
                break;
            case 'spotify':
                (player as SpotifyPlayer).playTrack();
                break;
        }
    }

    /**
     * Pause the current track
     */
    export function pause() {
        let track = nowPlaying();
        if (track === null) {
            return;
        }

        let platform = track.platform.toLowerCase();
        let player = getPlayer(platform);
        switch (platform) {
            case 'youtube':
                (player as YouTubePlayer).pauseVideo();
                break;
            case 'soundcloud':
                (player as SoundCloudPlayer).pause();
                break;
            case 'spotify':
                (player as SpotifyPlayer).pauseTrack();
                break;
        }
    }

    /**
     * @returns {boolean} `true` if track is playing, `false` otherwise
     */
    async function isPlaying(): Promise<boolean> {
        let track = nowPlaying();
        if (track === null) {
            return false;
        }

        let platform = track.platform.toLowerCase();
        let player = getPlayer(platform);
        switch (platform) {
            case 'youtube':
                let state = (player as YouTubePlayer).getPlayerState();
                return state === YouTubePlayerState.PLAYING;
            case 'soundcloud':
                let playing = !(await scGet((player as SoundCloudPlayer).isPaused.bind(player)));
                return playing;
            case 'spotify':
                return !(player as SpotifyPlayer).isPaused;
            default:
                // platform is not supported (invalid) => that platform's player
                // doesn't exist so it's not playing
                return false;
        }
    }

    /**
     * Toggles between play and pause on the current track
     */
    export async function toggle() {
        console.log(await isPlaying());
        if (await isPlaying()) {
            console.log('toggle pause()');
            pause();
        } else {
            console.log('toggle play()');
            play();
        }
    }

    /**
     * Swap to the specified player and `show()` it. `hide()`s and `pause()`s all other players
     * @param player the name of the player, e.g. `youtube`, `spotify`, `soundcloud`
     */
    export function swap(player: string) {
        show(player);
        Object.keys(players)
            .filter((key) => key !== player)
            .forEach((key) => hide(key));
    }

    function setVisible(player: string, visible: boolean) {
        let id = containerId(player);
        let container = document.getElementById(id);
        if (container) {
            container.hidden = !visible;
        }
    }

    /**
     * Hide the specified player
     * @param player the name of the player, as the key of `players`
     */
    function hide(player: string) {
        setVisible(player, false);
    }

    export function hideAll() {
        Object.keys(players).forEach(hide);
    }

    /**
     * Show the specified player, making it visible
     * @param player the name of the player, as the key of `players`
     */
    function show(player: string) {
        setVisible(player, true);
    }
}

export { supportedPlatforms, setPlayer, getPlayer, containerId, TrackQueue };
