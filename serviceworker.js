// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "narengi.net" + new Date().getTime();
var filesToCache = [
  "/static/images/favicons/fav-160.png",
  "/static/images/favicons/splashscreen.png",
  "/static/images/favicons/favicon.ico",
  "/static/images/logo.svg",
  "/static/images/favicons/fav32.png",
  "/static/images/favicons/fav16.png",
  "/static/images/favicons/fav-apple.png",
  "/static/css/bootstrap.rtl.min.css",
  "/static/css/bootstrap.rtl.min.css.map",
  "https://fonts.googleapis.com/icon?family=Material+Icons",
  "https://fonts.googleapis.com/icon?family=Material+Icons+Outlined",
  "/static/js/bootstrap.bundle.min.js",
  "/static/js/bootstrap.bundle.min.js.map",
  "/static/images/close-red.png",
  "/static/js/autosize.js",
  "/static/js/persian-date.js",
  "/static/css/font-face.css",
  "/static/fonts/Samim.eot",
  "/static/fonts/Samim.woff2",
  "/static/fonts/Samim.woff",
  "/static/fonts/Samim.ttf",
  "/static/fonts/Samim-Bold.eot",
  "/static/fonts/Samim-Bold.woff2",
  "/static/fonts/Samim-Bold.woff",
  "/static/fonts/Samim-Bold.ttf",
  "/static/fonts/Samim-Medium.eot",
  "/static/fonts/Samim-Medium.woff2",
  "/static/fonts/Samim-Medium.woff",
];

// Cache on install
self.addEventListener("install", (event) => {
  this.skipWaiting();
  event.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      return cache.addAll(filesToCache);
    })
  );
});

// Clear cache on activate
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => cacheName.startsWith("django-pwa-"))
          .filter((cacheName) => cacheName !== staticCacheName)
          .map((cacheName) => caches.delete(cacheName))
      );
    })
  );
});

// Serve from Cache
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
      .catch(() => {
        return caches.match("/static/images/favicons/splashscreen.png");
      })
  );
});
