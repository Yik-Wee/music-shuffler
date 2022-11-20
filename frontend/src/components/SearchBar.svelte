<script lang="ts">
    let platform: string = 'youtube';
    let id: string = '';
    let search: HTMLAnchorElement;
    let isValid = false;

    function validate(id: string) {
        // ...
        return !id.includes(' ');
    }
</script>

<div id="search-bar" class:error="{isValid}">
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
        }}
        on:keydown={({ key }) => {
            if (key === 'Enter' && isValid) {
                search.click();
            }
        }}
    />
    <!-- or use `goto()`? -->
    <a href="/search?platform={platform}&id={encodeURIComponent(id)}" bind:this={search}>👌</a>
</div>

<style>
    #search-bar.error > input {
        border: red;
    }

    #search-bar.error > a {
        pointer-events: none;
    }
</style>