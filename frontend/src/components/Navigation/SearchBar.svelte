<script lang="ts">
    import { parse, type ParsedUrl } from '../../url';

    let searchButton: HTMLAnchorElement;

    function getHref(parsedUrl: ParsedUrl | null): string {
        if (parsedUrl === null) {
            return 'javascript:void(0)';
        }

        let platform = parsedUrl.platform;
        let encodedId = encodeURIComponent(parsedUrl.id);
        let encodedDomain = encodeURIComponent(parsedUrl.domain);
        return `/search?platform=${platform}&id=${encodedId}&domain=${encodedDomain}`;
    }

    let url: string = '';
    $: parsedUrl = parse(url.trim());
    $: href = getHref(parsedUrl);
</script>

<div class="search-bar" class:error={parsedUrl === null}>
    <input
        type="text"
        name="id"
        placeholder="Playlist URL"
        bind:value={url}
        on:keydown={({ key }) => {
            if (key === 'Enter') {
                searchButton.click();
            }
        }}
    />

    <div class="search-button-container">
        <a class="search-button" {href} bind:this={searchButton}>👌</a>
    </div>
</div>

<style>
    .search-bar {
        display: flex;
        flex-direction: row;
        column-gap: 0.5rem;
        width: 100%;
        height: inherit;
        background-color: inherit;
    }

    .search-bar > input {
        width: 100%;
        background-color: inherit;
    }

    @media screen and (max-width: 768px) {
        .search-bar {
            position: fixed;
            top: 0;
            height: 7vh;
            padding: 4px;
        }

        .search-button {
            width: 2.5rem;
        }
    }

    .search-bar.error > input:focus,
    .search-bar.error > input:hover {
        border-bottom: 2px solid red;
    }

    .search-button {
        display: flex;
        height: 100%;
        justify-content: center;
        align-items: center;
        width: 5rem;
        border: 1.5px solid rgb(255, 199, 208);
        border-radius: 3px;
        transition: border 100ms ease-in-out;
    }

    .search-button:hover {
        border: 1.5px solid rgb(255, 157, 173);
    }

    .search-bar.error > .search-button-container > .search-button {
        opacity: 50%;
        pointer-events: none;
        align-items: center;
    }

    .search-bar.error > .search-button-container {
        cursor: not-allowed;
    }
</style>
