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

// =====Mix stuff======
type MixInfo = {
    /** The title of the mix */
    title: string;
    /** The (optional) description of the mix. Set to an empty string '' if no description provided */
    description: string;
    /** List of tuple(playlistID, platform) */
    playlists: [string, string][];
    // TODO possible support for "partial" mixes?
    // /** The list of tracks (may have been manually selected by the user) */
    // tracks: Track[];
    // /**
    //  * Whether the mix comprises specific tracks manually selected from each playlist (`true`)
    //  * or if the mix comprises ALL the tracks from the selected `playlists` (`false`)
    //  */
    // partial: boolean;
};

function isMixInfo(data: any): data is MixInfo {
    let m = data as MixInfo;
    return (
        m !== undefined &&
        m.playlists !== undefined &&
        m.title !== undefined &&
        m.description !== undefined
    );
}

function mixNotFound(id: string): ErrorResponse {
    return { error: `Mix ${id} not found 🦧` };
}

async function getMix(id: string): Promise<PlaylistResponse | ErrorResponse> {
    let mixInfoRaw = localStorage.getItem(id);
    if (!mixInfoRaw) {
        return mixNotFound(id);
    }

    let mixInfo: MixInfo | any;
    try {
        mixInfo = JSON.parse(mixInfoRaw);
    } catch (err) {
        // JSON decode error (SyntaxError)
        localStorage.removeItem(id);
        return mixNotFound(id);
    }

    if (!isMixInfo(mixInfo)) {
        localStorage.removeItem(id);
        return mixNotFound(id);
    }

    // // partial mix - tracks have already been selected and cached
    // if (mixInfo.partial) {
    //     return {
    //         platform: 'MIX',
    //         playlist_id: id,
    //         title: mixInfo.title,
    //         owner: 'Me',
    //         description: mixInfo.description,
    //         thumbnail: '/assets/mix.svg',  // compiled to build/ from static/ folder
    //         etag: '',
    //         length: mixInfo.tracks.length,
    //         tracks: mixInfo.tracks,
    //     }
    // }

    let tracks: Track[] = [];
    try {
        // get tracks from each playlist (in parallel)
        let responses: (PlaylistResponse | ErrorResponse)[] = await Promise.all(
            mixInfo.playlists.map(async ([id, platform]) => {
                let res = await fetch(`/api/playlist/${platform}?id=${id}`);
                return await res.json();
            })
        );

        // add each track to tracks
        for (let res of responses) {
            // if any request returned an error response, all requests are
            // considered invalid. (cannot render a complete mix)
            if (isErrorResponse(res)) {
                return res;
            }

            tracks.push(...res.tracks);
        }

        // return a playlist response once all tracks are fetched
        return {
            platform: 'MIX',
            playlist_id: id,
            title: mixInfo.title,
            owner: 'You',
            description: mixInfo.description,
            // gif from `static/assets/`, compiled to `build/assets/`
            thumbnail: '/assets/jammies.gif',
            etag: '',
            length: tracks.length,
            tracks: tracks
        };
    } catch (err) {
        return {
            error: `Error fetching playlists: ${err}`
        };
    }
}

export { getPlaylist, getPlaylistInfo };
