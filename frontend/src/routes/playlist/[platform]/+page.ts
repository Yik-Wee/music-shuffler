import type { PageData, PageLoadEvent } from './$types';

/** @type {import('./$types').PageLoad} */
export function load({ params }: PageLoadEvent): PageData {
    return { platform: params.platform };
}
