<script lang="ts">
    import type { Track } from '../../types/PlaylistTracks';
    import TrackList from '../../components/TrackList.svelte';
    import { TrackQueue } from '../../stores';

    let tracklist: Track[] = [
        {
            track_id: 'e0T0rI-GiR4',
            platform: 'YOUTUBE',
            title: 'Super Mario World Game Over LoFi Hip Hop Remix',
            thumbnail: 'https://i.ytimg.com/vi/e0T0rI-GiR4/sddefault.jpg',
            owner: 'Phillip Schlosser [HephestosMusic]',
        },
        {
            track_id: '5mwlU71S7TA',
            platform: 'YOUTUBE',
            title: 'jump man 93 - oldbandstuffs 1',
            thumbnail: 'https://i.ytimg.com/vi/TKM4IfADlPk/sddefault.jpg',
            owner: 'AnimeVibe',
        },
        {
            track_id: '1H9RGVK5hw404lHcKCSA67',
            platform: 'SPOTIFY',
            title: 'サンセット・ロード	',
            thumbnail: 'https://i.scdn.co/image/ab67616d00001e029435433ea249b8284eae5182',
            owner: '高橋玲子',
            duration_seconds: 258,
        },
        {
            track_id: '756210154',
            platform: 'SOUNDCLOUD',
            title: 'Arise',
            owner: 'Shogonodo',
            thumbnail: 'https://i1.sndcdn.com/artworks-wD4JohKo1P1NnscC-0N1Axg-t500x500.jpg',
            duration_seconds: 160,
        }
    ];

    let isSet = false;
</script>

<div>
    <TrackList {tracklist} trackclick={() => {
        if (!isSet) {
            isSet = true;
            TrackQueue.setQueue(tracklist, []);
        }
    }} />
</div>