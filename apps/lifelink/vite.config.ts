import { defineConfig, type Plugin } from "vite";
import preact from "@preact/preset-vite";
import { createHash } from "node:crypto";

// Writes sw.js after the build with the exact list of files to keep for offline use.
function serviceWorker(): Plugin {
  return {
    name: "lifelink-sw",
    apply: "build",
    generateBundle(_opts, bundle) {
      const files = Object.keys(bundle).filter(f => !f.endsWith(".map") && !/(cyrillic|greek|vietnamese)/.test(f));   // other scripts download only if a page needs them
      const all = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "icon-maskable.png", "favicon.png", ...files.filter(f => f !== "index.html")];
      const version = createHash("sha256").update(files.sort().join("|")).digest("hex").slice(0, 12);
      const src = `/* LifeLink prototype service worker: keeps the app working offline. Version ${version}. */
const CACHE = "lifelink-${version}";
const FILES = ${JSON.stringify(all)};
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("lifelink-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;   // never touch other sites' requests
  if (e.request.mode === "navigate") { e.respondWith(fetch(e.request).catch(() => caches.match("index.html", { ignoreSearch: true }))); return; }
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(r => r || fetch(e.request)));
});
`;
      this.emitFile({ type: "asset", fileName: "sw.js", source: src });
    }
  };
}

export default defineConfig({
  base: "/plan-to-end-poverty/lifelink/app/",
  plugins: [preact(), serviceWorker()],
  build: { outDir: "../../docs/plan-to-end-poverty/lifelink/app", emptyOutDir: true, target: "es2022", sourcemap: false, chunkSizeWarningLimit: 700 },
  server: { port: 5199 }
});
