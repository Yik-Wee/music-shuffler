import {
    isErrorResponse,
    type ErrorResponse,
    type PlaylistInfoResponse,
    type PlaylistResponse,
    type Track
} from './types/PlaylistTracks';

function playlistEndpoint(platform: string, id: string): string {
    return `/api/playlist/${platform}?id=${id}`;
}

function playlistInfoEndpoint(platform: string, id: string): string {
    return `/api/playlist_info/${platform}?id=${id}`;
}

/**
 *
 * @param platform
 * The music platform the playlist belongs to in lowercase
 * e.g. `'youtube'`, `'spotify'`, `'soundcloud'`
 * @param id
 * The ID of the playlist being fetched
 * @returns {Promise<PlaylistResponse | ErrorResponse>}
 * The `PlaylistResponse` from the API endpoint if successful, or an `ErrorResponse` if unsuccessful.
 */
async function getPlaylist(
    platform: string,
    id: string
): Promise<PlaylistResponse | ErrorResponse> {
    id = id.trim();
    if (!id) {
        // empty string is invalid
        return { error: 'Please provide a playlistID to search for' };
    }

    let endpoint = playlistEndpoint(platform, id);
    let response = await fetch(endpoint);
    let result: PlaylistResponse | ErrorResponse; // the response as json
    let error: string | undefined;

    try {
        result = await response.json();
    } catch (e) {
        if (response.status === 404 || response.status === 500) {
            error = 'API endpoint could not be reached';
        } else {
            error = 'The API returned a non-json response';
        }
        return { error };
    }

    if (!response.ok) {
        if (isErrorResponse(result)) {
            error = result.error;
        } else {
            error = `${response.status}: ${response.statusText}`;
        }
        return { error };
    } else if (isErrorResponse(result)) {
        error = `(${response.status}: ${response.statusText}) ${result.error}`;
        return { error };
    } else {
        // playlist = result;
        // return { ...result };
        return result;
    }
}

async function getPlaylistInfo(
    platform: string,
    id: string
): Promise<PlaylistInfoResponse | ErrorResponse> {
    id = id.trim();
    if (!id) {
        // empty string is invalid
        return { error: 'Please provide a playlistID to search for' };
    }

    let endpoint = playlistInfoEndpoint(platform, id);
    let response = await fetch(endpoint);
    let result: PlaylistInfoResponse | ErrorResponse; // the response as json
    let error: string | undefined;

    try {
        result = await response.json();
    } catch (e) {
        if (response.status === 404 || response.status === 500) {
            error = 'API endpoint could not be reached';
        } else {
            error = 'The API returned a non-json response';
        }
        return { error };
    }

    if (!response.ok) {
        if (isErrorResponse(result)) {
            error = result.error;
        } else {
            error = `${response.status}: ${response.statusText}`;
        }
        return { error };
    } else if (isErrorResponse(result)) {
        error = `(${response.status}: ${response.statusText}) ${result.error}`;
        return { error };
    } else {
        // playlist = result;
        // return { ...result };
        return result;
    }
}

/**
 * Get list of all tracks from all specified playlists.
 */
async function getManyPlaylists(
    playlists: { id: string; platform: string }[],
): Promise<PlaylistResponse[]> {
    let responses = await Promise.all(
        playlists.map(({ platform, id }) => getPlaylist(platform.toLowerCase(), id))
    );

    let playlistResponses = responses
        .filter((res): res is PlaylistResponse => {
            let isErr = isErrorResponse(res);
            if (isErr) console.error('Response error:', res);
            return !isErr;
        })
    return playlistResponses;
}

export { getPlaylist, getPlaylistInfo, getManyPlaylists };
