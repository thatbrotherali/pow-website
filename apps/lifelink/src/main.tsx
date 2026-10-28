import { render } from "preact";
import "./styles.css";
import { App } from "./app";
import { watchIdle } from "./lib/session";

render(<App />, document.getElementById("app")!);
watchIdle();

// Keep the app available offline. The service worker caches only the app itself, never personal data.
if ("serviceWorker" in navigator && import.meta.env.PROD) {
  addEventListener("load", () => { navigator.serviceWorker.register("sw.js").catch(() => {}); });
}
