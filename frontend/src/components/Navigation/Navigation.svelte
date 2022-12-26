<script>
    import { onMount } from "svelte";
    import NavBar from "./NavBar.svelte";
    import SearchBar from "./SearchBar.svelte";

    let hidden = false;
    let prevYOffset = 0;

    onMount(() => {
        window.addEventListener('scroll', () => {
            let yOffset = window.pageYOffset;
            // hide when navbar scrolled down
            hidden = prevYOffset <= yOffset;
            prevYOffset = yOffset;
        });
    });
</script>

<div class="top-bar" class:hidden>
    <NavBar />
    <SearchBar />
</div>

<style>
    .top-bar {
        /* background-color: rgb(255, 233, 236); */
        background-color: var(--black);
        color: var(--ivory);
        z-index: 9;
        position: fixed;
    }

    @media screen and (min-width: 768px) {
        .top-bar {
            height: 10vh;
            width: 100%;
            top: 0;
            transition: all 175ms ease-in-out;
            display: flex;
            flex-direction: row;
            column-gap: 4px;
            padding: 4px;
            align-items: center;
        }

        .top-bar.hidden {
            opacity: 0;
            top: calc(-10vh - (2 * 4px));
        }
    }
</style>