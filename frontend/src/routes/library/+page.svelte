<!-- <script lang="ts">
    import { onMount } from "svelte";
    import PlaylistCard from "../../components/PlaylistCard.svelte";
    import { getPlaylistInfo } from "../../requests";
    import { supportedPlatforms } from "../../stores";
    import { isErrorResponse, type ErrorResponse, type PlaylistInfoResponse } from "../../types/PlaylistTracks";

    type PlaylistEntry = [string, string];

    function isStringArray(arr: any[]): arr is string[] {
        return arr.some(v => typeof v !== 'string' && !(v instanceof String));
    }

    function getSavedPlaylistIdsPlatforms(savedRaw: string | null): PlaylistEntry[] | null {
        if (!savedRaw) {
            return null;
        }

        let saved;
        try {
            saved = JSON.parse(savedRaw);
        } catch (err) {
            return null;
        }

        if (!Array.isArray(saved)) {
            return null;
        }

        if (!isStringArray(saved)) {
            return null;
        }

        let validEntries = saved.filter((v, i) => {
            let pair = v.split(':');
            if (pair && pair.length !== 2) {
                return false;
            }

            let [platform, playlistId] = pair;
            if (!platform || !playlistId || !supportedPlatforms.includes(platform)) {
                return false;
            }

            return true;
        }).map(x => (x.split(':') as PlaylistEntry));

        return validEntries;
    }

    /**
     * Get saved playlists and playlist mixes
     */
    async function getSaved(): Promise<PlaylistInfoResponse[]> {
        // get saved playlists
        let savedRaw = localStorage.getItem('savedPlaylists');
        let saved = getSavedPlaylistIdsPlatforms(savedRaw);

        // get saved mixes
        // ...

        if (saved) {
            let responses: (PlaylistInfoResponse | ErrorResponse)[] = await Promise.all(
                saved.map(([platform, id]) => getPlaylistInfo(platform, id))
            );

            let allInfos = responses.filter(function (res): res is PlaylistInfoResponse {
                return !isErrorResponse(res);
            });
            return allInfos;
        }
        return [];
    }

    let library: PlaylistInfoResponse[];

    onMount(async () => {
        library = await getSaved();
    });
</script>

<div>
    {#each library as info}
        <PlaylistCard {...info} />
    {/each}
</div> -->