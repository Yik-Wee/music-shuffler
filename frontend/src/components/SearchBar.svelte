<script lang="ts">
    let platform: string = 'youtube';
    let id: string = '';
    let search: HTMLAnchorElement;
    let isValid = false;

    function validate(id: string): boolean {
        // ...
        return (id !== '' && !id.includes(' '));
    }
</script>

<div id="search-bar" class:error={!isValid}>
    <select name="platform" id="platform" bind:value={platform}>
        <option value="youtube">YouTube</option>
        <option value="spotify">Spotify</option>
        <option value="soundcloud">SoundCloud</option>
    </select>
    <input
        type="text"
        name="id"
        bind:value={id}
        on:input={() => {
            // validation here?
            id = id.trim();
            isValid = validate(id);
            console.log(isValid);
        }}
        on:keydown={({ key }) => {
            if (key === 'Enter') {
                search.click();
            }
        }}
    />
    <div id="search-button-container">
        <a
            id="search-button"
            href="/search?platform={platform}&id={encodeURIComponent(id)}"
            bind:this={search}
        >
            👌
        </a>
    </div>
</div>

<style>
    #search-bar {
        display: flex;
        flex-direction: row;
        column-gap: .5rem;
    }

    #search-bar > input {
        width: 50%;
        outline: 0;
        border: 0;
        border-bottom: 2px solid lightskyblue;
        transition: all 200ms ease-in-out;
    }

    #search-bar > input:focus {
        border-bottom: 2px solid blue;
    }

    #search-bar.error > input:focus {
        border-bottom: 2px solid red;
    }

    #search-bar.error > #search-button-container > #search-button {
        opacity: 50%;
        pointer-events: none;
    }

    #search-bar.error > #search-button-container {
        cursor: not-allowed;
    }
</style>