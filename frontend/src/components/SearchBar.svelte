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

<div id="search-bar">
    <select name="platform" id="platform">
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
    <a href="/{platform}/?id={encodeURIComponent(id)}" bind:this={search}>👌</a>
</div>
