<script lang="ts">
    import type { PlaylistInfoResponse } from '../../types/PlaylistTracks';
    import PlaylistCard from '../../components/PlaylistCard.svelte';
    import type { SavedPlaylistInfo } from '../../library';

    export let playlistInfo: PlaylistInfoResponse;
    let { playlist_id, platform, title, owner, thumbnail } = playlistInfo;
    // export let title: string;
    // export let owner: string;
    // export let thumbnail: string;

    export let intoItem = (): any => {
        return {
            id: playlist_id,
            platform,
        };
    };

    /** The list of items that will add or remove the current item */
    export let selectedlist: any[];
    // export let selectedlist: SavedPlaylistInfo[];
    
    export let colorSelected: string = 'greenyellow';
    export let colorUnselected: string = 'whitesmoke';

    let selected: boolean = false;
    let idx: number = -1;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class:selected>
    <PlaylistCard
        --bg-colour-hover="var(--bg-colour)"
        --bg-colour={selected ? colorSelected : colorUnselected}
        {title}
        {owner}
        {thumbnail}
        on:click={() => {
            if (selected) {
                // let idx = selectedlist.findIndex((info) => {
                //     return info.id === playlist_id && info.platform === platform;
                // });

                // if (idx === -1) {
                //     return;
                // }

                selectedlist.splice(idx, 1);
                selected = false;
            } else {
                selectedlist.push(intoItem());
                idx = selectedlist.length - 1;
                selected = true;
            }
        }}
    />
</div>
