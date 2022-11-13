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

export type PlaylistResponse = {
    platform: string;
    playlist_id: string;
    title: string;
    owner: string;
    description: string;
    thumbnail: string;
    etag: string;
    length: number;
    tracks: Track[];
};

export type ErrorResponse = {
    error: string;
};

export function isErrorResponse(obj: PlaylistResponse | ErrorResponse): obj is ErrorResponse {
    return (obj as ErrorResponse).error !== undefined;
}
