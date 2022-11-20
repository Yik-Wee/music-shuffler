// https://developers.soundcloud.com/docs/api/html5-widget

type WidgetParameters = {
    /** Start playing the item automatically */
    auto_play?: boolean;
    /** Hex code to color play button and other controls. e.g. “#0066CC” */
    color?: string;
    /** Show/Hide buy buttons */
    buying?: boolean;
    /** Show/Hide share buttons */
    sharing?: boolean;
    /** Show/Hide download buttons */
    download?: boolean;
    /** Show/Hide the item’s artwork */
    show_artwork?: boolean;
    /** Show/Hide number of track plays */
    show_playcount?: boolean;
    /** Show/Hide the uploader name */
    show_user?: boolean;
    /** A number from 0 to the playlist length which reselects the track in a playlist */
    start_track?: number;
    /** If set to false the multiple players on the page won’t toggle each other off when playing */
    single_active?: boolean;
};

/**
 * Typing for the `Widget` "instance" (Player instance) returned from the `SC.Widget(...)` function call
 */
interface SoundCloudPlayer {
    bind(eventName: string, listener: Function): void;
    unbind(eventName: string): void;
    load(url: string, options: WidgetParameters): void;
    play(): void;
    pause(): void;
    toggle(): void;
    seekTo(milliseconds: number): void;
    setVolume(volume: number): void;
    next(): void;
    prev(): void;
    skip(soundIndex: number): void;

    // --getters--
    getVolume(callback: (volume: number) => void): void;
    getDuration(callback: (duration: number) => void): void;
    getPosition(callback: (position: number) => void): void;
    // getSounds(callback: (sounds: Sound[]): void): void  // what is Sound?
    // getCurrentSound(callback: (sound: Sound) => void): void; // what is Sound?
    getCurrentSoundIndex(callback: (soundIndex: number) => void): void;
    isPaused(callback: (isPaused: boolean) => void): void;
}

/**
 * Typing for the `SC.Widget` function from the soundcloud player API
 * @param element Either the iframe element or the iframe ID
 * @returns {SoundCloudPlayer} The Widget instance that controls the soundcloud iframe player.
 */
type WidgetType = {
    (element: HTMLIFrameElement | string): SoundCloudPlayer,
    Events: {
        LOAD_PROGRESS: string,
        PLAY_PROGRESS: string,
        PLAY: string,
        PAUSE: string,
        FINISH: string,
        SEEK: string,
        READY: string,
        ERROR: string,
        // ...
    }
};

export type { SoundCloudPlayer, WidgetType as WidgetConstructor };
