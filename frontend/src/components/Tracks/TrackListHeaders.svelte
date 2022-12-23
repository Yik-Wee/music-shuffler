<script lang="ts">
    export let hidden: boolean = false;
</script>

<div class="tracklist-headers track-layout" class:hidden>
    <div>#</div>
    <div>🖼️</div>
    <div>Title/Owner</div>
    <div>🕒</div>
</div>

<style>
    @import './track-layout.css';

    .tracklist-headers {
        background-color: lightpink;
    }

    .hidden {
        display: none;
    }
</style>