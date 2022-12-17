<!-- Test how to check for unavailable tracks/videos -->
<script>
    import { TrackQueue } from "../../stores";

    TrackQueue.setQueue([
        {
            track_id: 'aY-VzcieGkc',
            platform: 'youtube',
            title: 'Private video',
            owner: '',
            thumbnail: '',
        },
        {
            track_id: 'z_wcL_zg2hM',
            platform: 'youtube',
            title: 'Deleted video',
            owner: '',
            thumbnail: '',
        },
        {
            track_id: '2tlQsWQCB4g3ZiCLBmrfMK',
            platform: 'spotify',
            title: 'Xue Hua Piao Trap',
            owner: '',
            thumbnail: '',
        },
    ], '', 'MIX');
</script>