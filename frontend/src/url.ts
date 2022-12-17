/**
 * Functions to parse & validate URLs for different platforms
 */

type ParsedUrl = {
    platform: string;
    id: string;
    domain: string;
};

const RE_URL = /^(?:https?:\/\/)?(\w+(?:\.\w+)+)\/(.+)$/i;

/**
 * @param url The url to parse e.g. from youtube, spotify, soundcloud
 * @returns {ParsedUrl | null} `ParsedUrl` or `null` if invalid url
 * 
 * # Note
 * For souncloud urls, the path returned as the id does not have trailing
 * or starting slash (e.g. `user/sets/album`) and is not normalised, so
 * path may be relative (e.g. `user/sets/../sets/album`)
 */
function parse(url: string): ParsedUrl | null {
    let matches = RE_URL.exec(url);
    if (matches?.length !== 3) {
        return null;
    }

    let [_, domain, path] = matches;

    if (!domain || !path) {
        return null;
    }

    if (YouTube.RE_DOMAIN.test(domain)) {
        // handle youtube request path
        let id = YouTube.parseId(path);
        console.log('youtube', id);
        if (!id) {
            return null;
        }

        return {
            platform: 'youtube',
            id,
            domain,
        };
    }

    if (SoundCloud.RE_DOMAIN.test(domain)) {
        // handle soundcloud request path
        let scPath = SoundCloud.parsePath(path);
        console.log('souncloud', scPath);
        if (!scPath) {
            return null;
        }

        return {
            platform: 'soundcloud',
            id: scPath,
            domain,
        };
    }

    if (Spotify.RE_DOMAIN.test(domain)) {
        // handle spotify request path
        let id = Spotify.parseId(path);
        console.log('spotify', id);
        if (!id) {
            return null;
        }

        return {
            platform: 'spotify',
            id,
            domain,
        };
    }

    return null;
}

function removeTrailingSlash(path: string): string {
    if (!path.endsWith('/')) {
        return path;
    }

    return path.slice(0, path.length - 1);
}

/**
 * Valid youtube domains:
 * - youtube.com
 * - www.youtube.com
 * - youtu.be
 * - m.youtube.com
 */
namespace YouTube {
    export const RE_DOMAIN = /^(((www\.|m\.)?youtube\.com)|(youtu\.be))$/i;
    const RE_ID =
        /^\/?playlist\/?\?(?:[\w\-%]+(?:=[^\/&]*)?&)*list=([^\/&]+)(?:&[\w\-%]+(?:=[^&]*)?)*/i;
    export function parseId(path: string): string | null {
        let matches = RE_ID.exec(path);
        if (matches?.length !== 2) {
            return null;
        }

        return removeTrailingSlash(matches[1]);
    }
}

/**
 * Valid soundcloud domains:
 * - soundcloud.com
 * - www.soundcloud.com
 * - on.soundcloud.com
 */
namespace SoundCloud {
    export const RE_DOMAIN = /^(www\.|on\.)?soundcloud\.com$/i;
    const RE_PATH = /^\/?([^\?\n]+)+\/?(?:\?.*)?/i;
    export function parsePath(path: string): string | null {
        let matches = RE_PATH.exec(path);
        if (matches?.length !== 2) {
            return null;
        }

        return removeTrailingSlash(matches[1]);
    }
}

/**
 * Valid spotify domains:
 * - spotify.com
 * - play.spotify.com
 * - open.spotify.com
 * - www.spotify.com
 */
namespace Spotify {
    export const RE_DOMAIN = /^(open\.|play\.|www\.)?spotify\.com$/i;
    // https://developer.spotify.com/documentation/web-api/
    // playlist ID is base-62
    const RE_ID = /^\/?(?:playlist|album)\/([0-9a-zA-Z]+)\/?(?:\?.*)?$/i;
    export function parseId(path: string): string | null {
        let matches = RE_ID.exec(path);
        if (matches?.length !== 2) {
            return null;
        }

        return removeTrailingSlash(matches[1]);
    }
}

export { parse, type ParsedUrl, YouTube, SoundCloud, Spotify };