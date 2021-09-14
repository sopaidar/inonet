// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "narengi.net" + new Date().getTime();
var filesToCache = [
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/fav-160.png",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/splashscreen.png",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/fav-160.png",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/favicon.ico",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/logo.svg",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/fav32.png",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/fav16.png",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/fav-apple.png",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/css/bootstrap.rtl.min.css",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/css/bootstrap.rtl.min.css.map",
  "https://fonts.googleapis.com/icon?family=Material+Icons",
  "https://fonts.googleapis.com/icon?family=Material+Icons+Outlined",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/js/bootstrap.bundle.min.js",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/js/bootstrap.bundle.min.js.map",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/close-red.png",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/js/autosize.js",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/js/persian-date.js",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/css/font-face.css",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim.eot",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim.woff2",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim.woff",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim.ttf",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim-Bold.eot",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim-Bold.woff2",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim-Bold.woff",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim-Bold.ttf",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim-Medium.eot",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim-Medium.woff2",
  "https://s3.ir-thr-at1.arvanstorage.com/narengi/static/fonts/Samim-Medium.woff",
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
        return caches.match("https://s3.ir-thr-at1.arvanstorage.com/narengi/static/images/favicons/splashscreen.png");
      })
  );
});
