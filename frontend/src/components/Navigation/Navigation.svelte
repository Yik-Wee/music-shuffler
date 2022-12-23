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
        background-color: rgb(255, 233, 236);
    }

    @media screen and (min-width: 768px) {
        .top-bar {
            height: 10vh;
            width: 100%;
            position: fixed;
            top: 0;
            z-index: 9;
            transition: opacity 175ms ease-in-out;
            display: flex;
            flex-direction: row;
            column-gap: 4px;
            padding: 4px;
            align-items: center;
        }

        .top-bar.hidden {
            opacity: 0;
        }
    }
</style>