<!-- @component
Renders the `PlaylistCard` that can be selected and unselected on click.
 -->
<script lang="ts">
    import PlaylistCard from '../../components/PlaylistCard.svelte';

    export let title: string;
    export let owner: string;
    export let thumbnail: string;

    type T = $$Generic;

    /** The list of items that will add or remove the current item */
    export let selectedlist: T[];

    /** The current item that will be added or removed from the `selectedlist` on click */
    export let item: T;

    export let onselect: (() => void) | undefined = undefined;
    export let onunselect: (() => void) | undefined = undefined;

    /** The colour of the card when selected */
    export let colorSelected: string = 'greenyellow';

    /** The colour of the card when unselected */
    export let colorUnselected: string = 'whitesmoke';

    let isSelected: boolean = false;

    /** This item's index in the `selectedlist` */
    let idx: number = -1;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class:isSelected>
    <PlaylistCard
        --bg-colour-hover="var(--bg-colour)"
        --bg-colour={isSelected ? colorSelected : colorUnselected}
        {title}
        {owner}
        {thumbnail}
        on:click={() => {
            if (isSelected) {
                // unselect the item - remove the item from the selectedlist with its index
                selectedlist.splice(idx, 1);
                isSelected = false;
                if (onunselect) onunselect();
            } else {
                // select the item - push to selectedlist
                selectedlist.push(item);
                idx = selectedlist.length - 1;
                isSelected = true;
                if (onselect) onselect();
            }
        }}
    />
</div>
