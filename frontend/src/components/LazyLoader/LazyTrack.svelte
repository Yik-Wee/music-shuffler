<script lang="ts">
    import Track from "./Track.svelte";
    import IntersectionObserver from "./IntersectionObserver.svelte";

    export let track_id: string;
    export let platform: string;
    export let title: string;
    export let owner: string;
    export let thumbnail: string | undefined = undefined;
    export let duration_seconds: number | undefined = undefined;

    export let position: number;
</script>

<IntersectionObserver once={true} let:intersecting={intersecting}>
    <Track
        {track_id}
        {platform}
        {title}
        {owner}
        {thumbnail}
        {duration_seconds}
        {position}
        loaded={intersecting}
        on:click
    />
</IntersectionObserver>
