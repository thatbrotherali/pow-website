/* LifeLink prototype service worker: keeps the app working offline. Version e37a03860ff0. */
const CACHE = "lifelink-e37a03860ff0";
const FILES = ["./","index.html","manifest.webmanifest","icon-192.png","icon-512.png","icon-maskable.png","favicon.png","assets/inter-latin-ext-wght-normal-DO1Apj_S.woff2","assets/inter-latin-wght-normal-Dx4kXJAl.woff2","assets/fraunces-latin-ext-wght-normal-Ca2vKHc0.woff2","assets/fraunces-latin-wght-normal-ukD16Tqj.woff2","assets/index-tNj50PRQ.css","assets/index-oteh_8hD.js","assets/jsQR-B6_eh9D_.js"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("lifelink-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;   // never touch other sites' requests
  if (e.request.mode === "navigate") { e.respondWith(fetch(e.request).catch(() => caches.match("index.html", { ignoreSearch: true }))); return; }
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});
