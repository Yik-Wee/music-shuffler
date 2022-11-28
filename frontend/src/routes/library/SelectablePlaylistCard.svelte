<script lang="ts">
    import type { PlaylistInfoResponse } from '../../types/PlaylistTracks';
    import PlaylistCard from '../../components/PlaylistCard.svelte';
    import type { SavedPlaylistInfo } from '../../library';

    export let playlistInfo: PlaylistInfoResponse;
    let { playlist_id, platform, title, owner, thumbnail } = playlistInfo;

    export let selectedlist: SavedPlaylistInfo[];

    let selected: boolean = false;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class:selected>
    <PlaylistCard
        --bg-colour-hover="var(--bg-colour)"
        --bg-colour={selected ? 'greenyellow' : 'whitesmoke'}
        {title}
        {owner}
        {thumbnail}
        on:click={() => {
            if (selected) {
                let idx = selectedlist.findIndex((info) => {
                    return info.id === playlist_id && info.platform === platform;
                });

                if (idx === -1) {
                    return;
                }

                selectedlist.splice(idx, 1);
                selected = false;
            } else {
                selectedlist.push({
                    id: playlist_id,
                    platform
                });
                selected = true;
            }
        }}
    />
</div>
