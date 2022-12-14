/**
 * Functions to manage saved playlists and mixes in the library
 */

import { getPlaylistInfo } from './requests';
import {
    isErrorResponse,
    type PlaylistInfoResponse,
    type PlaylistResponse,
    type Track
} from './types/PlaylistTracks';

const MIXES_KEY = 'saved-mixes';
const PLAYLISTS_KEY = 'saved-playlists';

type SavedPlaylistInfo = {
    id: string;
    /** lowercase platform */
    platform: string;
};

type SavedMixInfo = {
    /** Title of the mix. Must be unique. */
    title: string;
    playlists: SavedPlaylistInfo[];
};

type SavedMix = {
    title: string;
    /** playlist ids */
    playlists: PlaylistInfoResponse[];
    tracks: Track[];
};

function isSavedPlaylist(value: any): value is SavedPlaylistInfo {
    let info = value as SavedPlaylistInfo;
    return info !== undefined && info.platform !== undefined && info.id !== undefined;
}

function isSavedMix(value: any): value is SavedMixInfo {
    let info = value as SavedMixInfo;
    return (
        info !== undefined && info.playlists !== undefined && info.title !== undefined
        // info.id !== undefined
    );
}

function saveMix(mix: SavedMixInfo) {
    // get alr saved mixes
    let saved = getSavedMixes();

    // check if no saved mixes
    if (!saved) {
        let newSaved = JSON.stringify([mix]);
        localStorage.setItem(MIXES_KEY, newSaved);
        return;
    }

    // check if this mix is alr saved
    // if (saved.some((obj) => obj.id === mix.id)) {
    if (saved.some((obj) => obj.title === mix.title)) {
        return;
    }

    // add to saved mixes
    saved.push(mix);
    let newSaved = JSON.stringify(saved);
    localStorage.setItem(MIXES_KEY, newSaved);
}

function savePlaylist(playlist: SavedPlaylistInfo) {
    // get alr saved playlists
    let saved = getSavedPlaylists();

    // check if no saved playlists
    if (!saved) {
        let newSaved = JSON.stringify([playlist]);
        localStorage.setItem(PLAYLISTS_KEY, newSaved);
        return;
    }

    // check if this mix is alr saved
    if (saved.some((obj) => obj.id === playlist.id)) {
        return;
    }

    // add to saved mixes
    saved.push(playlist);
    let newSaved = JSON.stringify(saved);
    localStorage.setItem(PLAYLISTS_KEY, newSaved);
}

function save(item: SavedMixInfo | SavedPlaylistInfo) {
    if (isSavedMix(item)) {
        saveMix(item);
    } else if (isSavedPlaylist(item)) {
        savePlaylist(item);
    } else {
        console.warn('Unable to save item to library as it is not a mix or playlist\n>', item);
    }
}

function getSavedMixes(): SavedMixInfo[] | null {
    let savedRaw = localStorage.getItem(MIXES_KEY);
    if (!savedRaw) {
        return null;
    }

    // validate saved mixes
    let saved;
    try {
        saved = JSON.parse(savedRaw);
    } catch (err) {
        console.warn('Error while parsing saved mixes: ', err);
        localStorage.removeItem(MIXES_KEY);
        return null;
    }

    if (!Array.isArray(saved)) {
        localStorage.removeItem(MIXES_KEY);
        return null;
    }

    // check if any object in the arr is invalid (true if invalid)
    let validSavedMixes = saved.filter(isSavedMix);
    return validSavedMixes;
}

function findSavedMix(title: string): SavedMixInfo | null {
    let mixes = getSavedMixes();
    if (!mixes) {
        return null;
    }

    let found = mixes.find((mixInfo) => mixInfo.title === title);
    if (!found) {
        return null;
    }

    return found;
}

function getSavedPlaylists(): SavedPlaylistInfo[] | null {
    let savedRaw = localStorage.getItem(PLAYLISTS_KEY);
    if (!savedRaw) {
        return null;
    }

    // validate saved playlists
    let saved;
    try {
        saved = JSON.parse(savedRaw);
    } catch (err) {
        console.warn('Error while parsing saved playlists: ', err);
        localStorage.removeItem(PLAYLISTS_KEY);
        return null;
    }

    if (!Array.isArray(saved)) {
        localStorage.removeItem(PLAYLISTS_KEY);
        return null;
    }

    // check if any object in the arr is invalid (true if invalid)
    let validSavedMixes = saved.filter(isSavedPlaylist);
    return validSavedMixes;
}

type LibraryInfo = {
    mixes: SavedMixInfo[];
    playlists: SavedPlaylistInfo[];
};

type Library = {
    mixes: SavedMixInfo[];
    playlists: PlaylistInfoResponse[];
};

function getSavedInfo(): LibraryInfo {
    return {
        mixes: getSavedMixes() || [],
        playlists: getSavedPlaylists() || []
    };
}

async function getSaved(): Promise<Library> {
    let saved = getSavedInfo();
    console.log(saved.mixes);
    console.log(saved.playlists);
    let responses = await Promise.all(
        saved.playlists.map(({ platform, id }) => getPlaylistInfo(platform, id))
    );
    console.log(responses);
    return {
        mixes: saved.mixes,
        playlists: responses.filter((res): res is PlaylistInfoResponse => !isErrorResponse(res))
    };
}

/**
 * Delete the specified playlist from the library
 * @param playlistInfo the specified playlist
 */
function deleteSavedPlaylist(playlistInfo: SavedPlaylistInfo) {
    console.log('Deleting playlist from library:', playlistInfo);

    let saved = getSavedPlaylists();
    if (!saved) {
        return;
    }

    let idx = saved.findIndex(({ id, platform }) => {
        return id === playlistInfo.id && platform === playlistInfo.platform;
    });

    if (idx === -1) {
        return;
    }

    saved.splice(idx, 1);
    let newSaved = JSON.stringify(saved);
    localStorage.setItem(PLAYLISTS_KEY, newSaved);
}

/**
 * Delete the specified mix from the library
 * @param title the title of the mix
 */
function deleteSavedMix(title: string) {
    console.log('Deleting mix from library:', title);

    let saved = getSavedMixes();
    if (!saved) {
        return;
    }

    let idx = saved.findIndex(mix => mix.title === title);
    if (idx === -1) {
        return;
    }

    saved.splice(idx, 1);
    let newSaved = JSON.stringify(saved);
    localStorage.setItem(MIXES_KEY, newSaved);
}

export {
    save,
    saveMix,
    savePlaylist,
    getSaved,
    getSavedMixes,
    findSavedMix,
    getSavedPlaylists,
    deleteSavedMix,
    deleteSavedPlaylist
};
export type { SavedPlaylistInfo, SavedMixInfo, SavedMix, Library };
