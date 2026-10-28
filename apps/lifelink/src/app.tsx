// The app shell: header, navigation (bottom tabs on phones, a side rail on tablets and computers) and routes.
import { useEffect, useRef, useState } from "preact/hooks";
import { Fragment } from "preact";
import { effect } from "@preact/signals";
import { mode, vault, settings, saveState } from "./lib/model";
import { vaultExists, lockNow } from "./lib/session";
import { route, Icon } from "./ui/ui";
import { Welcome } from "./screens/Start";
import { Today } from "./screens/Today";
import { Identity } from "./screens/Identity";
import { Wallet } from "./screens/Wallet";
import { Learn, Lesson, Review } from "./screens/Learn";
import { Health, MedicalId, Record, Checkin, Vitals, Care, Info } from "./screens/Health";
import { Safety, Sos } from "./screens/Safety";
import { Voice } from "./screens/Voice";
import { MyData, Erase } from "./screens/MyData";
import { Devices } from "./screens/Devices";
import { About, Settings } from "./screens/About";

// Apply reading settings to the whole page
effect(() => {
  const s = settings.value, r = document.documentElement;
  r.style.setProperty("--scale", String(s.textSize / 100));
  if (s.theme === "auto") r.removeAttribute("data-theme"); else r.setAttribute("data-theme", s.theme);
  if (s.contrast) r.setAttribute("data-contrast", "more"); else r.removeAttribute("data-contrast");
  if (s.reduceMotion) r.setAttribute("data-motion", "reduce"); else r.removeAttribute("data-motion");
});

const NAV: [string, string, string][] = [["/", "today", "Today"], ["/id", "id", "Identity"], ["/wallet", "wallet", "Wallet"], ["/learn", "learn", "Learn"], ["/health", "health", "Health"],
  ["/safety", "safety", "Safety"], ["/voice", "voice", "Your say"], ["/devices", "devices", "Devices"], ["/data", "data", "My data"], ["/settings", "settings", "Settings"], ["/about", "info", "About"]];
const TABS: [string, string, string][] = [["/", "today", "Today"], ["/learn", "learn", "Learn"], ["/wallet", "wallet", "Wallet"], ["/health", "health", "Health"], ["/more", "more", "More"]];
const section = (r: string) => "/" + (r.split("/")[1] || "");

function screen(r: string) {
  const [, a = "", b = "", c = ""] = r.split("/");
  switch (a) {
    case "": return <Today />;
    case "id": return <Identity />;
    case "wallet": return <Wallet />;
    case "learn": return b === "lesson" ? <Lesson id={c} /> : b === "review" ? <Review /> : <Learn />;
    case "health": return b === "medical-id" ? <MedicalId /> : b === "record" ? <Record /> : b === "checkin" ? <Checkin /> : b === "vitals" ? <Vitals /> : b === "care" ? <Care /> : b === "info" ? <Info /> : <Health />;
    case "safety": return <Safety />;
    case "sos": return <Sos />;
    case "voice": return <Voice />;
    case "data": return <MyData />;
    case "devices": return <Devices />;
    case "settings": return <Settings />;
    case "about": return <About />;
    case "more": return <More />;
    default: return <Today />;
  }
}

function More() {
  return <div class="stack fade-in"><h1>More</h1><div class="grid2">{NAV.filter(([h]) => !TABS.some(([t]) => t === h)).map(([h, i, l]) =>
    <a class="card" href={`#${h}`} key={h}><div class="row"><Icon n={i} /><strong>{l}</strong></div></a>)}</div></div>;
}

export function App() {
  const [has, setHas] = useState<boolean | null>(null);
  const taps = useRef<number[]>([]);
  useEffect(() => { vaultExists().then(setHas); }, [mode.value]);
  useEffect(() => { document.getElementById("page-title")?.focus({ preventScroll: true }); }, [route.value]);
  const r = route.value, v = vault.value;
  // A quiet SOS: tap the LifeLink mark three times quickly.
  const brandTap = () => { const t = Date.now(); taps.current = [...taps.current.filter(x => t - x < 1200), t]; if (taps.current.length >= 3) { taps.current = []; location.hash = "/sos"; } else if (v) location.hash = "/"; };

  return <div class="app">
    <a class="skip" href="#main" onClick={e => { e.preventDefault(); document.getElementById("main")?.focus(); }}>Skip to content</a>
    <header class="top">
      <button class="brand" onClick={brandTap} aria-label="LifeLink home (tap three times for SOS)"><span class="logo" aria-hidden="true">L</span><span><small>People of the World</small><b>LifeLink</b></span></button>
      {mode.value === "demo" && <span class="chip chip-demo">Demo</span>}
      {mode.value === "own" && <span class="chip chip-own" title={saveState.value === "saved" ? "Saved and encrypted on this device" : ""}>{saveState.value === "saving" ? "Saving…" : saveState.value === "error" ? "Not saved" : "Encrypted"}</span>}
      <span class="spacer" />
      {v && <a class="sos-btn" href="#/sos" style="text-decoration:none;display:inline-grid;place-items:center">SOS</a>}
      {v && <button class="iconbtn" onClick={() => lockNow()} aria-label={mode.value === "demo" ? "Leave the demonstration" : "Lock"} title={mode.value === "demo" ? "Leave the demonstration" : "Lock"}><Icon n="lock" /></button>}
    </header>
    <div class="body">
      {v && <nav class="rail" aria-label="Sections">{NAV.map(([h, i, l], k) => <Fragment key={h}>
        {k === 5 && <span class="group">Community</span>}{k === 8 && <span class="group">You</span>}
        <a href={`#${h}`} aria-current={section(r) === h ? "page" : undefined}><Icon n={i} />{l}</a></Fragment>)}</nav>}
      <main class="main" id="main" tabIndex={-1}>
        {v ? screen(r) : has === null ? null : r === "/erase" ? <EraseFromLock /> : <Welcome hasVault={has} />}
      </main>
    </div>
    {v && <nav class="tabs" aria-label="Main">{TABS.map(([h, i, l]) => <a key={h} class="tab" href={`#${h}`} aria-current={(h === "/more" ? !TABS.slice(0, 4).some(([t]) => t === section(r)) : section(r) === h) ? "page" : undefined}><Icon n={i} />{l}</a>)}</nav>}
  </div>;
}

function EraseFromLock() {
  return <div class="stack" style="max-width:480px;margin:0 auto"><h1>Start again?</h1><p class="muted">If you've forgotten your PIN, the only way forward is to erase this LifeLink. Without the PIN, no one can read it, including us.</p>
    <Erase onClose={() => { location.hash = "/"; }} /></div>;
}
