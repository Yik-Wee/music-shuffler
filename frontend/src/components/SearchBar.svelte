<script lang="ts">
    import { parse, type ParsedUrl } from "./SearchBar/url";


    // let platform: string = 'youtube';
    // let id: string = '';
    let search: HTMLAnchorElement;
    // let isValid = false;

    // function validate(id: string): boolean {
    //     // ...
    //     return id !== '' && !id.includes(' ');
    // }

    let url: string = '';
    let parsedUrl: ParsedUrl | null = null;

    function toHref(parsedUrl: ParsedUrl | null): string {
        if (parsedUrl === null) {
            return 'javascript:void(0)';
        }
        return `/search?platform=${parsedUrl.platform}&id=${encodeURIComponent(parsedUrl.id)}`
    }
</script>

<div class="search-bar" class:error={parsedUrl === null}>
    <input
        type="text"
        name="id"
        bind:value={url}
        on:input={() => {
            url = url.trim();
            parsedUrl = parse(url);
            console.log(parsedUrl);
        }}
        on:keydown={({ key }) => {
            if (key === 'Enter') {
                search.click();
            }
        }}
    />

    <div class="search-button-container">
        <a class="search-button" href="{toHref(parsedUrl)}" bind:this={search}>👌</a>
    </div>
</div>

<style>
    .search-bar {
        display: flex;
        flex-direction: row;
        column-gap: 0.5rem;
    }

    .search-bar > input {
        width: 50%;
        outline: 0;
        border: 0;
        border-bottom: 2px solid lightskyblue;
        transition: all 200ms ease-in-out;
    }

    .search-bar > input:focus,
    .search-bar > input:hover {
        border-bottom: 2px solid blue;
    }

    .search-bar.error > input:focus,
    .search-bar.error > input:hover {
        border-bottom: 2px solid red;
    }

    .search-bar.error > .search-button-container > .search-button {
        opacity: 50%;
        pointer-events: none;
    }

    .search-bar.error > .search-button-container {
        cursor: not-allowed;
    }
</style>
