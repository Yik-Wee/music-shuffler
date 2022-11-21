<script lang="ts">
    import PlaylistCard from "../../../components/PlaylistCard.svelte";

    let info = {
        title: 'Test playlist ナイス！ a b c d e f g h i j k l m n o p q r s t u v w x y z aaaaa AAAAAAA',
        thumbnail: 'https://i.ytimg.com/vi/Fq55MMfHoJg/sddefault.jpg',
        owner: 'めっちゃめっちゃすごくセックス人 ああああああああああ！ああああああああああ！ああああああああああ！',
    };
</script>

<div class="test-playlistcard">
    <div class="test">
        <PlaylistCard {...info} />
        <PlaylistCard --width="120px" --height="240px" --lines=4 {...info} />
        <PlaylistCard --width="240px" --height="240px" --lines=5 {...info} />
        <PlaylistCard --width="75%" --height="240px" --thumbnail-height="{0.6*240}px" {...info} />
        <PlaylistCard --width="40%" --height="100%" {...info} />
        <!-- <PlaylistCard {...info} /> -->
        <!-- <PlaylistCard {...info} />
        <PlaylistCard {...info} />
        <PlaylistCard {...info} />
        <PlaylistCard {...info} />
        <PlaylistCard {...info} />
        <PlaylistCard {...info} />
        <PlaylistCard {...info} />
        <PlaylistCard {...info} />
        <PlaylistCard {...info} /> -->
    </div>
</div>

<style>
    .test {
        flex-wrap: wrap;
        display: flex;
        row-gap: 10px;
        column-gap: 10px;
    }
</style>