// Shared interface pieces: icons, routing, QR codes, the camera scanner, read-aloud, sheets and notices.
import { useEffect, useRef, useState } from "preact/hooks";
import type { ComponentChildren, JSX } from "preact";
import { signal } from "@preact/signals";
import QRCode from "qrcode";
import { mode } from "../lib/model";

// ---------------------------------------------------------------- routing (hash based, so it works offline and from any folder)
export const route = signal(location.hash.slice(1) || "/");
window.addEventListener("hashchange", () => { route.value = location.hash.slice(1) || "/"; window.scrollTo(0, 0); });
export const go = (to: string) => { location.hash = to; };

// ---------------------------------------------------------------- icons
const P: Record<string, string> = {
  today: "M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z",
  id: "M3 6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM8.5 13a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM5 17c.8-1.8 2-2.6 3.5-2.6S11.2 15.2 12 17M14 9h5M14 13h4",
  wallet: "M3 7a2 2 0 0 1 2-2h13v4M3 7v10a2 2 0 0 0 2 2h15V9H5a2 2 0 0 1-2-2zM16 14h.01",
  learn: "M2 8l10-5 10 5-10 5zM6 10v5c2 2 10 2 12 0v-5M22 8v6",
  health: "M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6-8 11-8 11zM8 11h2l1-2 2 4 1-2h2",
  more: "M4 6h16M4 12h16M4 18h16",
  safety: "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM12 8v5M12 16h.01",
  voice: "M4 20h16M6 20V10M10 20V10M14 20V10M18 20V10M3 10l9-6 9 6z",
  data: "M12 3c4.4 0 8 1.3 8 3s-3.6 3-8 3-8-1.3-8-3 3.6-3 8-3zM4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6",
  devices: "M6 3h12a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zM11 18h2",
  info: "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 11v6M12 7h.01",
  settings: "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z",
  lock: "M6 11h12v10H6zM8 11V7a4 4 0 0 1 8 0v4",
  scan: "M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M7 12h10",
  speaker: "M11 5L6 9H3v6h3l5 4zM15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13",
  heart: "M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6-8 11-8 11z",
  bt: "M7 7l10 10-5 4V3l5 4L7 17",
  check: "M5 12l5 5L20 7",
  back: "M15 18l-6-6 6-6",
  arrow: "M9 18l6-6-6-6",
  alert: "M12 3l10 18H2zM12 10v4M12 17h.01",
  spark: "M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"
};
export function Icon({ n, size = 22, label }: { n: keyof typeof P | string; size?: number; label?: string }) {
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
    role={label ? "img" : undefined} aria-label={label} aria-hidden={label ? undefined : true}><path d={P[n] || P.info} /></svg>;
}

// ---------------------------------------------------------------- layout helpers
export function Page({ eyebrow, title, sub, back, children, listen }: { eyebrow?: string; title: string; sub?: ComponentChildren; back?: string; children: ComponentChildren; listen?: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => { document.title = `${title} · LifeLink prototype`; }, [title]);
  return <div class="stack fade-in" ref={ref}>
    <div class="head">
      {back && <a href={`#${back}`} class="row small muted" style="text-decoration:none;gap:4px"><Icon n="back" size={18} />Back</a>}
      {eyebrow && <span class="eyebrow">{eyebrow}</span>}
      <div class="row between" style="align-items:flex-start"><h1 tabIndex={-1} id="page-title">{title}</h1>{listen !== false && <Listen target={ref} />}</div>
      {sub && <p class="muted">{sub}</p>}
    </div>
    {children}
  </div>;
}
export function Notice({ kind = "info", children }: { kind?: "info" | "warn" | "ok" | "danger" | "demo"; children: ComponentChildren }) {
  return <div class={`notice notice-${kind}`} role={kind === "danger" ? "alert" : undefined}><Icon n={kind === "ok" ? "check" : kind === "danger" || kind === "warn" ? "alert" : "info"} size={20} /><div>{children}</div></div>;
}
export const DemoNote = ({ children }: { children: ComponentChildren }) => <Notice kind="demo"><strong>Demonstration. </strong>{children}</Notice>;
export function Sheet({ title, onClose, children }: { title: string; onClose: () => void; children: ComponentChildren }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null; ref.current?.querySelector<HTMLElement>("h2")?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", k); return () => { document.removeEventListener("keydown", k); prev?.focus?.(); };
  }, []);
  return <div class="sheet-wrap" onClick={e => { if (e.target === e.currentTarget) onClose(); }}>
    <div class="sheet" role="dialog" aria-modal="true" aria-label={title} ref={ref}>
      <div class="row between"><h2 tabIndex={-1}>{title}</h2><button class="btn btn-small btn-ghost" onClick={onClose}>Close</button></div>
      {children}
    </div>
  </div>;
}
export function Toggle({ checked, onChange, label, hint }: { checked: boolean; onChange: (v: boolean) => void; label: string; hint?: string }) {
  return <label class="toggle"><input type="checkbox" checked={checked} onChange={e => onChange((e.target as HTMLInputElement).checked)} />
    <span><strong>{label}</strong>{hint && <span class="muted small" style="display:block">{hint}</span>}</span></label>;
}
export function Field(p: { label: string; hint?: string; value: string; onInput: (v: string) => void; type?: string; placeholder?: string; area?: boolean; inputMode?: JSX.HTMLAttributes["inputMode"]; autocomplete?: string; maxLength?: number; class?: string }) {
  return <label class="field">{p.label}
    {p.area ? <textarea value={p.value} placeholder={p.placeholder} onInput={e => p.onInput((e.target as HTMLTextAreaElement).value)} />
      : <input class={p.class} type={p.type || "text"} value={p.value} placeholder={p.placeholder} inputMode={p.inputMode} autocomplete={p.autocomplete} maxLength={p.maxLength} onInput={e => p.onInput((e.target as HTMLInputElement).value)} />}
    {p.hint && <span class="hint">{p.hint}</span>}</label>;
}

// ---------------------------------------------------------------- formatting
export const fmtDate = (iso: string, opts: Intl.DateTimeFormatOptions = { day: "numeric", month: "short", year: "numeric" }) => { try { return new Date(iso).toLocaleDateString(undefined, opts); } catch { return iso; } };
export const fmtTime = (iso: string) => { try { return new Date(iso).toLocaleString(undefined, { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" }); } catch { return iso; } };
export const isDemo = () => mode.value === "demo";

// ---------------------------------------------------------------- QR codes
export function QR({ text, label }: { text: string; label: string }) {
  const [svg, setSvg] = useState("");
  useEffect(() => { QRCode.toString(text, { type: "svg", errorCorrectionLevel: text.length > 1200 ? "L" : "M", margin: 1 }).then(setSvg).catch(() => setSvg("")); }, [text]);
  return <div class="qr" role="img" aria-label={label} dangerouslySetInnerHTML={{ __html: svg }} />;
}

// ---------------------------------------------------------------- camera scanner (BarcodeDetector where the browser has it, otherwise jsQR)
export function Scanner({ onText, onClose }: { onText: (t: string) => void; onClose: () => void }) {
  const video = useRef<HTMLVideoElement>(null);
  const [err, setErr] = useState(""); const [paste, setPaste] = useState("");
  useEffect(() => {
    let stream: MediaStream | null = null, stop = false, raf = 0;
    (async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" }, audio: false });
        const v = video.current!; v.srcObject = stream; await v.play();
        const BD = (window as unknown as { BarcodeDetector?: new (o: object) => { detect: (s: CanvasImageSource) => Promise<{ rawValue: string }[]> } }).BarcodeDetector;
        const detector = BD ? new BD({ formats: ["qr_code"] }) : null;
        const jsqr = detector ? null : (await import("jsqr")).default;
        const c = document.createElement("canvas"), ctx = c.getContext("2d", { willReadFrequently: true })!;
        const tick = async () => {
          if (stop) return;
          try {
            if (detector) { const r = await detector.detect(v); if (r[0]?.rawValue) { onText(r[0].rawValue); return; } }
            else if (v.videoWidth) {
              c.width = v.videoWidth; c.height = v.videoHeight; ctx.drawImage(v, 0, 0);
              const r = jsqr!(ctx.getImageData(0, 0, c.width, c.height).data, c.width, c.height); if (r?.data) { onText(r.data); return; }
            }
          } catch { /* keep scanning */ }
          raf = requestAnimationFrame(tick);
        };
        tick();
      } catch { setErr("The camera isn't available. You can paste the code's text instead."); }
    })();
    return () => { stop = true; cancelAnimationFrame(raf); stream?.getTracks().forEach(t => t.stop()); };
  }, []);
  return <Sheet title="Scan a LifeLink code" onClose={onClose}>
    {!err && <video ref={video} class="video" muted playsInline aria-label="Camera view" />}
    {err && <Notice kind="warn">{err}</Notice>}
    <details><summary class="small">No camera? Paste the code's text</summary>
      <div class="stack" style="margin-top:10px"><Field label="Code text" value={paste} onInput={setPaste} area />
        <button class="btn" disabled={!paste.trim()} onClick={() => onText(paste.trim())}>Use this text</button></div></details>
  </Sheet>;
}

// ---------------------------------------------------------------- read aloud (on-device speech, for people who prefer listening)
export function Listen({ target }: { target: { current: HTMLElement | null } }) {
  const [on, setOn] = useState(false);
  const supported = "speechSynthesis" in window;
  useEffect(() => () => { if (supported) speechSynthesis.cancel(); }, []);
  if (!supported) return null;
  const toggle = () => {
    if (on) { speechSynthesis.cancel(); setOn(false); return; }
    const el = target.current; if (!el) return;
    const clone = el.cloneNode(true) as HTMLElement; clone.querySelectorAll("button,svg,.qr,video,[aria-hidden=true]").forEach(n => n.remove());
    const u = new SpeechSynthesisUtterance(clone.innerText.replace(/\s+/g, " ").slice(0, 4000));
    u.onend = () => setOn(false); speechSynthesis.cancel(); speechSynthesis.speak(u); setOn(true);
  };
  return <button class="btn btn-small btn-ghost" onClick={toggle} aria-pressed={on}><Icon n="speaker" size={18} />{on ? "Stop" : "Listen"}</button>;
}

// ---------------------------------------------------------------- tiny chart
export function Spark({ values, label, min, max }: { values: number[]; label: string; min?: number; max?: number }) {
  if (values.length < 2) return null;
  const lo = min ?? Math.min(...values), hi = max ?? Math.max(...values), span = hi - lo || 1, w = 300, h = 56;
  const pts = values.map((v, i) => `${(i / (values.length - 1)) * w},${h - 6 - ((v - lo) / span) * (h - 12)}`).join(" ");
  return <svg class="spark" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" role="img" aria-label={label}>
    <polyline points={pts} fill="none" stroke="var(--accent)" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke" /></svg>;
}

// ---------------------------------------------------------------- downloads (export your data)
export function download(name: string, text: string, type = "application/json") {
  const url = URL.createObjectURL(new Blob([text], { type })); const a = document.createElement("a");
  a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
}
