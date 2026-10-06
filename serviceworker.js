// Hangarin service worker
// Bump this version whenever you change this file so old caches get cleared.
const CACHE_NAME = 'hangarin-cache-v5';

// Only things that never change per user. We deliberately do NOT cache '/'
// or any page: those show each user's own tasks and must always be fresh.
const PRECACHE_URLS = ['/offline/'];

self.addEventListener('install', function (e) {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(PRECACHE_URLS);
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (names) {
      return Promise.all(
        names
          .filter(function (name) { return name !== CACHE_NAME; })
          .map(function (name) { return caches.delete(name); })
      );
    })
  );
});

self.addEventListener('fetch', function (e) {
  // Never touch form submissions (add/edit/delete/bulk actions are POSTs).
  if (e.request.method !== 'GET') return;

  // Pages: always ask the server first; show the offline page only if that fails.
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).catch(function () {
        return caches.match('/offline/');
      })
    );
    return;
  }

  // Our own static files (icons etc.): use the cached copy if we have one,
  // otherwise fetch it and remember it for next time.
  const url = new URL(e.request.url);
  if (url.origin === self.location.origin && url.pathname.startsWith('/static/')) {
    e.respondWith(
      caches.match(e.request).then(function (cached) {
        return cached || fetch(e.request).then(function (response) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            cache.put(e.request, copy);
          });
          return response;
        });
      })
    );
  }
});