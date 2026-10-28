// Devices: what works today with the phone and devices people already own, and the road to LifeLink's own hardware.
import { useEffect, useRef, useState } from "preact/hooks";
import { update, logAccess } from "../lib/model";
import { PROFILES, bluetoothAvailable, connect, type Reading } from "../lib/ble";
import { Icon, Notice, Page, Spark } from "../ui/ui";

const PAPER = "/plan-to-end-poverty/lifelink/";
const IMG = "/assets/lifelink/";

export function Devices() {
  return <Page eyebrow="Devices" title="Devices" sub="LifeLink starts on the phone, tablet or computer you have, then grows into a family of devices.">
    <Bluetooth />
    <FallDetection />
    <h2>The LifeLink family</h2>
    <p class="muted">Each device has its own specification. Here is what each can already do with today's technology, and what waits for LifeLink hardware.</p>
    <div class="grid2">{[
      ["smartwatch", "Smartwatch", "lifelink-smartwatch", "Heart rate, oxygen, sleep and stress; fall detection; silent SOS; tap-to-pay.", "Today: any watch or band that broadcasts heart rate over Bluetooth works with this prototype. Apple Health and Android Health Connect come with the native app in Phase 2."],
      ["ring", "Touch Smart Ring", "lifelink-touch-smart-ring", "A biometric key: tap to pay, sign in, or double-tap for silent SOS.", "Today: passkeys already turn a phone's fingerprint reader into the same kind of key. NFC payment needs the native app."],
      ["hear-buds", "Hear Buds", "lifelink-hear-buds", "Voice access to every service, live translation, hearing support.", "Today: this prototype reads every page aloud. Private, on-device translation and speech arrive on phones as browsers and the pilot app add them."],
      ["glasses", "Look Smart Glasses", "lifelink-look-smart-glasses", "Hands-free guidance, reading text aloud for people with low vision, step-by-step training.", "Today: the phone camera already reads LifeLink codes. Guided training overlays wait for affordable glasses."]
    ].map(([img, name, slug, does, today]) => <a class="card" key={slug} href={`${PAPER}${slug}/`} target="_blank" rel="noopener">
      <img src={`${IMG}${img}.jpg`} alt={`Concept rendering of the LifeLink ${name}`} width="320" height="320" loading="lazy" style="border-radius:12px;aspect-ratio:1;object-fit:cover;width:100%;max-height:200px" />
      <strong>{name}</strong><span class="small">{does}</span><span class="small muted">{today}</span><span class="small" style="color:var(--info)">Read the specification ↗</span></a>)}</div>
    <a class="card" href={`${PAPER}the-lifelink-tablet/`} target="_blank" rel="noopener"><strong>The LifeLink Tablet ("The Link") ↗</strong><span class="muted small">This prototype is the software the Tablet will run: the same app, on a solar-powered, secure device for people who don't own a phone.</span></a>
  </Page>;
}

function Bluetooth() {
  const [live, setLive] = useState<{ name: string; kind: string; stop: () => void } | null>(null), [last, setLast] = useState<Reading | null>(null), [hist, setHist] = useState<number[]>([]), [err, setErr] = useState("");
  const saved = useRef(0);
  useEffect(() => () => live?.stop(), [live]);
  if (!bluetoothAvailable()) return <div class="card"><h3><Icon n="bt" />Bluetooth health devices</h3>
    <Notice kind="info">This browser can't connect to Bluetooth devices. Chrome or Edge on a computer, or Chrome on Android, can. On iPhone and iPad, Safari doesn't support it; the pilot app will.</Notice>
    <p class="small muted">Works with devices that use the standard Bluetooth health profiles: heart-rate straps and many watches, blood pressure cuffs, thermometers, scales and pulse oximeters.</p></div>;
  const start = async (i: number) => {
    setErr(""); live?.stop(); setHist([]); setLast(null);
    try {
      const p = PROFILES[i];
      const c = await connect(p, r => {
        setLast(r); if (r.kind === "hr") setHist(h => [...h.slice(-59), r.value]);
        const now = Date.now();
        if (r.kind !== "hr" || now - saved.current > 60000) {   // heart rate streams every second: keep one a minute
          saved.current = now; update(x => { x.health.vitals.push(r); x.health.vitals = x.health.vitals.slice(-500); });
        }
      });
      setLive({ ...c, kind: p.kind }); logAccess("You", "Connected a health device", c.name);
    } catch (e) { const m = (e as Error).message || ""; setErr(/cancel/i.test(m) || (e as Error).name === "NotFoundError" ? "No device chosen." : m || "Couldn't connect."); }
  };
  return <div class="card"><h3><Icon n="bt" />Bluetooth health devices</h3>
    <p class="muted small">Readings go straight from the device to this phone or computer, using the standard Bluetooth health profiles. No account with the device maker is needed, and nothing goes to the cloud.</p>
    {live ? <div class="stack" style="gap:8px" aria-live="polite">
      <div class="row"><span class="dot-live" aria-hidden="true" /><strong>{live.name}</strong></div>
      {last ? <div class="live">{last.kind === "bp" ? `${last.value}/${last.value2}` : last.value}<span class="small muted" style="font-family:var(--body);font-size:1rem"> {last.unit}{last.pulse ? ` · pulse ${last.pulse}` : ""}</span></div> : <p class="muted">Waiting for a reading… {live.kind !== "hr" && "Take a measurement on the device."}</p>}
      {hist.length > 2 && <Spark values={hist} label="Heart rate, last minute" />}
      <button class="btn btn-small" style="align-self:flex-start" onClick={() => { live.stop(); setLive(null); }}>Disconnect</button>
      <span class="small muted">Saved to your vitals ({live.kind === "hr" ? "one reading a minute" : "each measurement"}).</span></div>
      : <div class="grid2">{PROFILES.map((p, i) => <button class="btn" key={p.kind} onClick={() => start(i)}>{p.label}</button>)}</div>}
    {err && <Notice kind="warn">{err}</Notice>}
  </div>;
}

// Fall detection with the phone's motion sensor: a moment of free fall, then a hard impact, then stillness.
// Runs only while this page is open (browsers stop sensors in the background); the watch and the pilot app run it all day.
function FallDetection() {
  const [on, setOn] = useState(false), [state, setState] = useState<"watch" | "ask" | "">(""), [n, setN] = useState(30), [peak, setPeak] = useState(0);
  const freefall = useRef(0);
  useEffect(() => {
    if (!on) return;
    const h = (e: DeviceMotionEvent) => {
      const a = e.accelerationIncludingGravity; if (!a || a.x === null) return;
      const g = Math.hypot(a.x || 0, a.y || 0, a.z || 0) / 9.81; setPeak(p => Math.max(p * 0.98, g));
      const t = performance.now();
      if (g < 0.4) freefall.current = t;
      else if (g > 2.5 && t - freefall.current < 600 && state !== "ask") { setState("ask"); setN(30); }
    };
    addEventListener("devicemotion", h); return () => removeEventListener("devicemotion", h);
  }, [on, state]);
  useEffect(() => { if (state !== "ask") return; if (n <= 0) { location.hash = "/sos"; return; } const t = setTimeout(() => setN(n - 1), 1000); return () => clearTimeout(t); }, [state, n]);
  const enable = async () => {
    const DME = DeviceMotionEvent as unknown as { requestPermission?: () => Promise<string> };
    if (DME.requestPermission) { try { if ((await DME.requestPermission()) !== "granted") return; } catch { return; } }
    setOn(true); setState("watch");
  };
  return <div class="card"><h3><Icon n="alert" />Fall detection</h3>
    <p class="muted small">Uses the phone's motion sensor, on the device only. If it senses a fall it asks if you're OK, and starts SOS after 30 seconds without an answer. <strong>The rule:</strong> you choose who is alerted.</p>
    {typeof DeviceMotionEvent === "undefined" ? <p class="small muted">This device has no motion sensor the browser can use.</p>
      : !on ? <button class="btn btn-small" style="align-self:flex-start" onClick={enable}>Try it while this page is open</button>
      : state === "ask" ? <div class="stack" role="alert"><strong>Did you fall? Are you OK?</strong><p>Starting SOS in {n} seconds.</p><button class="btn btn-primary" onClick={() => setState("watch")}>I'm OK</button></div>
      : <div class="stack" style="gap:6px"><span class="small" role="status">Watching for a fall. Try dropping the phone gently onto a bed or cushion.</span><div class="bar" aria-hidden="true"><span style={`width:${Math.min(100, (peak / 3) * 100)}%`} /></div>
        <button class="btn btn-small" style="align-self:flex-start" onClick={() => { setOn(false); setState(""); }}>Stop</button></div>}
    <p class="small muted">A phone in a pocket or bag is a rougher sensor than a watch on the wrist: this shows the idea, not a medical alarm.</p>
  </div>;
}
