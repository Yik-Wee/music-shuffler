<div class="navbar">
    <div class="navbar-item">
        <a href="/queue">
            <div class="navbar-icon">
                <img src="/assets/queue.svg" alt="Queue" />
            </div>
            <div>Queue</div>
        </a>
    </div>

    <div class="navbar-item">
        <a href="/library">
            <div>
                <img src="/assets/library.svg" alt="Library" />
            </div>
            <div>Library</div>
        </a>
    </div>
</div>

<style>
    .navbar {
        height: 10vh;
        display: flex;
        flex-direction: row;
        transition: opacity 100ms ease-in-out;
    }

    .navbar-item {
        background-color: lightgreen;
        padding: 4px;
        text-align: center;
        height: calc(10vh - 8px);
        width: calc(10vh - 8px);
        transition: background-color 75ms ease-in-out;
    }

    .navbar-item:hover {
        background-color: green;
    }

    a {
        text-decoration: none;
        height: 5vh;
    }

    img {
        height: 5vh;
    }
</style>
