import { writable } from 'svelte/store';

export let topic = writable("");
export let text = writable("");
export let ownTextSelected = writable();
export let route = writable("analyze");