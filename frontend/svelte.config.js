// frontend/svelte.config.js
import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    adapter: adapter({ fallback: 'index.html' }),   // SPA mode
    prerender: { entries: [] }                      // skip crawling
  },

  proxy: {
    '/analyze':       'http://localhost:5000',
    '/analyze-media': 'http://localhost:5000'
  }
};
