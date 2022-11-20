export type Track = {
    track_id: string;
    platform: string;
    title: string;
    owner: string;
    thumbnail: string;
    /**
     * The duration of the track in seconds.
     * On `platform = 'YOUTUBE'`, `duration_seconds` will be `null`  */
    duration_seconds?: number;
};

export type PlaylistResponse = PlaylistInfoResponse & {
    // platform: string;
    // playlist_id: string;
    // title: string;
    // owner: string;
    // description: string;
    // thumbnail: string;
    // etag: string;
    length: number;
    tracks: Track[];
};

export type PlaylistInfoResponse = {
    platform: string;
    playlist_id: string;
    title: string;
    owner: string;
    description: string;
    thumbnail: string;
    etag: string;
}

export type ErrorResponse = {
    error: string;
};

export function isErrorResponse(obj: PlaylistResponse | PlaylistInfoResponse | ErrorResponse): obj is ErrorResponse {
    return (obj as ErrorResponse).error !== undefined;
}

export function toPlaylistInfo({ length, tracks, ...info }: PlaylistResponse): PlaylistInfoResponse {
    return info;
}