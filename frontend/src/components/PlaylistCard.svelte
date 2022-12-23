<!-- @component
Renders the library item as a card (playlist or mix)

# Styling
* `--width`: width of the card
* `--height`: height of the card
* `--lines`: number of lines on `title` and `owner` text until it overflows into ellipsis

# Props
* `title`: title of the playlist/mix
* `owner`: the owner of the playlist/mix
* `thumbnail`: the playlist's thumbnail. Set to empty string `''` by default if no thumbnail
* `editable`: whether the card title should be able to be edited

# Events
* `on:click`: called when the card is clicked
 -->
<script lang="ts">
    export let title: string;
    export let owner: string;
    export let thumbnail: string = '';
    export let editable = false;
    export let classlist = '';
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="playlist-card {classlist}" on:click>
    <div class="playlist-card-thumbnail">
        {#if thumbnail}
            <img src={thumbnail} alt="{title} by {owner}" />
        {/if}
    </div>
    <div class="playlist-card-text-big">
        {#if editable}
            <slot />
        {:else}
            <span>{title}</span>
        {/if}
    </div>
    <div class="playlist-card-text-small">
        <span>{owner}</span>
    </div>
</div>

<style>
    :root {
        --width: 120px;
        --height: 220px;
        --lines: 3;
        --thumbnail-width: 90%;
        --thumbnail-height: calc(0.4 * var(--height));
        --bg-colour: whitesmoke;
        --bg-colour-hover: salmon;
    }

    .playlist-card {
        padding: 1%;
        border-radius: 4px;
        width: var(--width);
        height: var(--height);
        background: var(--bg-colour);
        overflow: hidden;
        cursor: pointer;
        grid-template-rows: [thumbnail] var(--thumbnail-height) [title] 2fr [owner] 1fr;
        transition: background 75ms ease-in;
    }

    .playlist-card:hover {
        background: var(--bg-colour-hover);
    }

    .playlist-card > .playlist-card-text-big,
    .playlist-card > .playlist-card-text-small {
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: var(--lines);
        -webkit-box-orient: vertical;
    }

    .playlist-card > .playlist-card-text-big {
        font-size: large;
    }

    .playlist-card > .playlist-card-text-small {
        font-size: smaller;
        color: grey;
    }

    .playlist-card > .playlist-card-thumbnail {
        display: flex;
        justify-content: center;
        align-items: center;
        height: var(--thumbnail-height);
    }

    .playlist-card > .playlist-card-thumbnail > img {
        border-radius: 4px;
        max-width: var(--thumbnail-width);
        max-height: var(--thumbnail-height);
    }
</style>
