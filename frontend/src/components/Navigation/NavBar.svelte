<div class="navbar">
    <div class="navbar-item">
        <a href="/">
            <div>
                <img src="/assets/home.svg" alt="Home">
            </div>
            <div class="text">Home</div>
        </a>
    </div>

    <div class="navbar-item">
        <a href="/queue">
            <div class="navbar-icon">
                <img src="/assets/queue.svg" alt="Queue" />
            </div>
            <div class="text">Queue</div>
        </a>
    </div>

    <div class="navbar-item">
        <a href="/library">
            <div>
                <img src="/assets/library.svg" alt="Library" />
            </div>
            <div class="text">Library</div>
        </a>
    </div>
</div>

<style>
    .navbar {
        height: 10vh;
        display: flex;
        flex-direction: row;
        background-color: inherit;
    }

    .navbar-item {
        background-color: var(--radical-red);
        padding: 4px;
        text-align: center;
        height: calc(10vh - 8px);
        flex: 1 100%;
        transition: background-color 75ms ease-in-out;
    }
    
    .navbar-item:hover {
        /* background-color: rgb(255, 210, 218); */
        background-color: var(--radical-red-dim);
    }

    a {
        text-decoration: none;
        height: 5vh;
        color: black;
    }

    img {
        height: 5vh;
    }

    /* mobile - navbar at bottom */
    @media screen and (max-width: 768px) {
        .navbar {
            height: 7vh;
            width: 100%;
            bottom: 0;
            position: fixed;
        }

        .text {
            display: none;
        }

        .navbar-item {
            height: calc(7vh - 8px);
            width: calc(7vh - 8px);
        }
    }
</style>
