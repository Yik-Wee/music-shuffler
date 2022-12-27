import { writable, type Writable } from 'svelte/store';
import { findSavedMix } from './library';
import { getManyPlaylists, getPlaylist } from './requests';
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

type Queue = {
    position: number;
    tracklist: Track[];
    id: string;
    platform: string;
};

/**
 * manages `TrackQueue` cache e.g. queue and last played track
 */
namespace CacheManager {
    const KEYS = {
        queue: 'cached-queue',
        track: 'last-played-track'
    };

    type CacheIdentifier = {
        id: string;
        platform: string;
    };

    function parseJson<T>(
        jsonString: string,
        validate: ((value: any) => value is T) | undefined = undefined
    ): T | null {
        try {
            let parsed = JSON.parse(jsonString);
            if (!validate) {
                return parsed;
            }
            return validate(parsed) ? parsed : null;
        } catch {
            return null;
        }
    }

    function getCache<T>(
        key: string,
        validate: ((value: any) => value is T) | undefined = undefined
    ): T | null {
        let str = localStorage.getItem(key);
        if (!str) {
            return null;
        }

        return parseJson<T>(str, validate);
    }

    function isString(value: any): value is string {
        return typeof value === 'string' || value instanceof String;
    }

    function isCacheIdentifier(obj: any): obj is CacheIdentifier {
        return isString(obj.id) && isString(obj.platform);
    }

    function validatePlatform(platform: string): boolean {
        return [...supportedPlatforms, 'mix'].includes(platform);
    }

    export function setCachedQueue(queue: CacheIdentifier) {
        let { id, platform } = queue;
        localStorage.setItem(KEYS.queue, JSON.stringify({ id, platform }));
    }

    export async function getCachedQueue(): Promise<Queue | null> {
        let cachedQueueInfo = getCache<CacheIdentifier>(
            KEYS.queue,
            (value): value is CacheIdentifier => {
                return isCacheIdentifier(value) && validatePlatform(value.platform);
            }
        );

        if (!cachedQueueInfo) {
            return null;
        }

        let { platform, id } = cachedQueueInfo;
        let position = 0;
        let cachedTrackInfo = getCachedTrackInfo();

        // is not mix, just regular playlist
        if (supportedPlatforms.includes(platform.toLowerCase())) {
            let playlist = await getPlaylist(platform, id);
            if (isErrorResponse(playlist)) {
                console.log('Error fetching cached queue', playlist.error);
                return null;
            }

            position = getCachedTrackPosition(playlist.tracks, cachedTrackInfo) || 0;

            return {
                position,
                id,
                platform,
                tracklist: playlist.tracks
            };
        }

        // is mix. get mix tracks
        let savedMixInfo = findSavedMix(id);
        if (!savedMixInfo) {
            return null;
        }

        let playlistResponses = await getManyPlaylists(savedMixInfo.playlists);
        let tracklist = playlistResponses
            .map((playlist) => playlist.tracks)
            .reduce((flat, toFlatten) => flat.concat(toFlatten));
        position = getCachedTrackPosition(tracklist, cachedTrackInfo) || 0;
        return { position, tracklist, id, platform };
    }

    function getCachedTrackPosition(
        tracklist: Track[],
        trackInfo: CacheIdentifier | null
    ): number | null {
        if (!trackInfo) {
            return null;
        }

        let idx = tracklist.findIndex(
            (track) =>
                track.track_id === trackInfo.id &&
                track.platform.toLowerCase() === trackInfo.platform.toLowerCase()
        );
        return idx === -1 ? null : idx;
    }

    export function setCachedTrackInfo(trackInfo: CacheIdentifier) {
        localStorage.setItem(KEYS.track, JSON.stringify(trackInfo));
    }

    export function getCachedTrackInfo(): CacheIdentifier | null {
        return getCache<CacheIdentifier>(KEYS.track, (value): value is CacheIdentifier => {
            return isCacheIdentifier(value) && validatePlatform(value.platform);
        });
    }
}

/**
 * The namespace containing functions to control the track queue
 */
namespace TrackQueue {
    let queue: Queue = {
        position: 0,
        tracklist: [],
        id: '',
        platform: ''
    };

    export let isQueueLoading: Writable<boolean> = writable(false);

    /**
     * Loads the most recently cached queue
     */
    export async function loadCachedQueue() {
        isQueueLoading.set(true);
        let cachedQueue = await CacheManager.getCachedQueue();
        if (cachedQueue) {
            queue = cachedQueue;
        }
        isQueueLoading.set(false);
        load(queue.position);
    }

    /**
     * Set/reset the queue to store the `tracklist` and `playlists` the tracks are from.
     * @param tracklist The list of tracks stored in the queue
     * @param id The id of the playlist, or unique title of the mix.
     * @param platform the **lowercase** platform of the playlist, or 'mix' if it is a mix
     * @param position the position of the current track. default `0`
     */
    export function setQueue(
        tracklist: Track[],
        id: string,
        platform: string,
        position: number | undefined = undefined
    ) {
        // check if queue alr set to desired
        // if (id === queue.id || platform === queue.platform) {
        //     queue.position = position || 0;
        //     // play();
        //     return;
        // }

        // pause();
        queue.tracklist = tracklist;
        queue.id = id;
        queue.platform = platform;
        queue.position = position || 0;
        // play();

        CacheManager.setCachedQueue({ id, platform });
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

        CacheManager.setCachedTrackInfo({ id: track.track_id, platform: track.platform });
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
     * Swap to the specified player and `show()` it. `hide()`s and `pause()`s the current track
     * @param player the name of the player, e.g. `youtube`, `spotify`, `soundcloud`
     */
    export function swap(player: string) {
        pause();
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
