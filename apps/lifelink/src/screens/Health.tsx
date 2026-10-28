// Health: Medical ID, a portable record (FHIR IPS), wellbeing, vitals, where to get care, and trusted information.
// LifeLink doesn't diagnose: a symptom checker is a medical device that needs clinical testing and approval.
import { useEffect, useState } from "preact/hooks";
import { vault, update, logAccess, settings, type Item } from "../lib/model";
import { ipsBundle } from "../lib/fhir";
import { COUNTRIES, INFO, MEDICINE_LINKS } from "../data/health";
import { Field, Icon, Notice, Page, QR, Sheet, Spark, Toggle, download, fmtDate, fmtTime } from "../ui/ui";

export function Health() {
  const v = vault.value!; const h = v.health;
  const c = COUNTRIES.find(x => x.code === settings.value.country) || COUNTRIES[COUNTRIES.length - 1];
  const last = h.checkins.slice(-7);
  return <Page eyebrow="Health" title="Your health" sub="Your records in your hands, help when you need it, and trustworthy information.">
    <div class="grid2">
      <a class="card accent" href="#/health/medical-id"><h3><Icon n="heart" />Medical ID</h3><span class="muted">{h.medicalId.bloodType ? `Blood type ${h.medicalId.bloodType} · ` : ""}{h.allergies.length} allerg{h.allergies.length === 1 ? "y" : "ies"} · {h.medicalId.showOnLock ? "on the lock screen" : "not on the lock screen"}</span></a>
      <a class="card" href="#/health/record"><h3><Icon n="data" />Health record</h3><span class="muted">{h.conditions.length} conditions, {h.medications.length} medicines, {h.immunizations.length} vaccinations. Export in the international standard.</span></a>
      <a class="card" href="#/health/checkin"><h3><Icon n="spark" />Wellbeing</h3><span class="muted">{last.length ? `${last.length} check-ins this week` : "A daily check-in and a breathing exercise"}</span>{last.length > 1 && <Spark values={last.map(x => x.mood)} min={1} max={5} label="Mood over the last week" />}</a>
      <a class="card" href="#/health/vitals"><h3><Icon n="health" />Vitals</h3><span class="muted">{h.vitals.length ? `Latest: ${describe(h.vitals[h.vitals.length - 1])}` : "Heart rate, blood pressure, temperature, weight, oxygen"}</span></a>
    </div>
    <div class="card" style="border-color:var(--danger)"><h3>Need help now?</h3>
      <div class="row"><a class="btn btn-danger" href={`tel:${c.emergency.split(" ")[0]}`}>Emergency: {c.emergency}</a><a class="btn" href="#/health/care">Nurse and crisis lines</a></div>
      <span class="muted small">Showing {c.name}. Change your country in <a href="#/settings">Settings</a>.</span></div>
    <a class="card" href="#/health/info"><h3><Icon n="info" />Trusted health information</h3><span class="muted">WHO, MedlinePlus, healthdirect, the NHS, Hesperian, and a medicine lookup.</span></a>
    <a class="card" href="#/devices"><h3><Icon n="bt" />Connect a health device</h3><span class="muted">Heart-rate straps and watches, blood pressure cuffs, thermometers, scales and oximeters over Bluetooth.</span></a>
    <Notice kind="info">LifeLink doesn't diagnose. Symptom checkers are medical devices that need clinical testing and approval; until LifeLink has one, it points you to people and services that can help.</Notice>
  </Page>;
}

const describe = (r: { kind: string; value: number; value2?: number; unit: string }) =>
  r.kind === "bp" ? `blood pressure ${r.value}/${r.value2} ${r.unit}` : `${({ hr: "heart rate", temp: "temperature", weight: "weight", spo2: "oxygen" } as Record<string, string>)[r.kind]} ${r.value} ${r.unit}`;

// ---------------------------------------------------------------- Medical ID
export function MedicalId() {
  const v = vault.value!; const m = v.health.medicalId;
  const [showQr, setShowQr] = useState(false);
  const set = (k: keyof typeof m, val: string | boolean) => update(x => { (x.health.medicalId as Record<string, unknown>)[k] = val; });
  const summary = [`MEDICAL ID: ${v.person.name}, born ${v.person.birthDate}`, m.bloodType && `Blood type: ${m.bloodType}`,
    `Allergies: ${v.health.allergies.map(a => a.name + (a.severe ? " (SEVERE)" : "")).join(", ") || "none recorded"}`,
    `Conditions: ${v.health.conditions.map(c => c.name).join(", ") || "none recorded"}`,
    `Medicines: ${v.health.medications.map(c => c.name + (c.dose ? ` ${c.dose}` : "")).join("; ") || "none recorded"}`,
    m.notes && `Notes: ${m.notes}`, ...v.safety.contacts.slice(0, 2).map(c => `Contact: ${c.name} (${c.relation}) ${c.phone}`)].filter(Boolean).join("\n");
  return <Page eyebrow="Health" title="Medical ID" back="/health" sub="What a paramedic or doctor needs to know if you can't tell them.">
    <div class="grid2">
      <Field label="Blood type" value={m.bloodType} onInput={x => set("bloodType", x)} placeholder="e.g. O+" />
      <Field label="Organ donor" value={m.organDonor} onInput={x => set("organDonor", x)} placeholder="Yes / No" />
    </div>
    <Field label="Notes for responders" area value={m.notes} onInput={x => set("notes", x)} placeholder="e.g. Asthma: reliever inhaler in bag" />
    <p class="muted small">Allergies, conditions and medicines come from your <a href="#/health/record">health record</a>; emergency contacts from <a href="#/safety">Safety</a>.</p>
    <Toggle checked={m.showOnLock} onChange={x => { set("showOnLock", x); logAccess("You", x ? "Put your Medical ID on the lock screen" : "Removed your Medical ID from the lock screen", "Your choice"); }}
      label="Show on the lock screen" hint="Lets a responder read it without your PIN. Only this card is kept unencrypted; everything else stays locked." />
    <button class="btn btn-primary" onClick={() => { setShowQr(true); logAccess("You", "Showed your Medical ID code", "Your choice"); }}>Show as a code a responder can scan</button>
    {showQr && <Sheet title="Medical ID code" onClose={() => setShowQr(false)}><QR text={summary} label="Medical ID as a QR code" /><pre class="small" style="white-space:pre-wrap;margin:0">{summary}</pre>
      <p class="small muted">Plain text, so any phone camera can read it, with no app needed.</p></Sheet>}
  </Page>;
}

// ---------------------------------------------------------------- the health record
type ListKey = "conditions" | "medications" | "allergies" | "immunizations";
const LISTS: { k: ListKey; title: string; ph: string; extra?: { key: keyof Item; label: string; type?: string } }[] = [
  { k: "conditions", title: "Conditions", ph: "e.g. Asthma", extra: { key: "since", label: "Since (year)" } },
  { k: "medications", title: "Medicines", ph: "e.g. Salbutamol inhaler", extra: { key: "dose", label: "How you take it" } },
  { k: "allergies", title: "Allergies", ph: "e.g. Penicillin" },
  { k: "immunizations", title: "Vaccinations", ph: "e.g. Influenza", extra: { key: "date", label: "Date", type: "date" } }];

export function Record() {
  const v = vault.value!;
  const exportIps = () => {
    download(`health-summary-${new Date().toISOString().slice(0, 10)}.json`, JSON.stringify(ipsBundle(v.person.name, v.person.birthDate, v.health), null, 2), "application/fhir+json");
    logAccess("You", "Exported your health summary", "International Patient Summary (FHIR)");
  };
  return <Page eyebrow="Health" title="Health record" back="/health" sub="Kept on your device, encrypted. Take it to any doctor, anywhere.">
    {LISTS.map(L => <ListEditor key={L.k} {...L} />)}
    <div class="card"><h3>Take your record anywhere</h3>
      <p class="muted">Export as an International Patient Summary: the HL7 FHIR standard for a health summary that doctors' systems in many countries can read.</p>
      <button class="btn btn-primary" style="align-self:flex-start" onClick={exportIps}>Export health summary (FHIR IPS)</button>
      <p class="small muted">Self-reported: a clinic would confirm and sign entries in a pilot.</p></div>
  </Page>;
}
function ListEditor({ k, title, ph, extra }: typeof LISTS[number]) {
  const items = vault.value!.health[k] as Item[];
  const [name, setName] = useState(""), [x, setX] = useState(""), [severe, setSevere] = useState(false);
  const add = (e: Event) => { e.preventDefault(); if (!name.trim()) return;
    update(v => { const it: Item = { name: name.trim() }; if (extra && x) (it as Record<string, unknown>)[extra.key] = x; if (k === "allergies") it.severe = severe; (v.health[k] as Item[]).push(it); });
    setName(""); setX(""); setSevere(false); };
  return <section class="card" aria-label={title}><h3>{title}</h3>
    {items.length ? <ul class="list">{items.map((it, i) => <li key={i}><div class="grow"><strong>{it.name}</strong>{it.severe && <span class="pill pill-bad" style="margin-left:8px">Severe</span>}
      <div class="muted small">{[it.since && `since ${it.since}`, it.dose, it.date && fmtDate(it.date)].filter(Boolean).join(" · ")}</div></div>
      <button class="btn btn-small btn-ghost" aria-label={`Remove ${it.name}`} onClick={() => update(v => { (v.health[k] as Item[]).splice(i, 1); })}>Remove</button></li>)}</ul> : <p class="muted small">None recorded.</p>}
    <form class="row" onSubmit={add}><input class="input" style="flex:2;min-width:160px" value={name} placeholder={ph} aria-label={`Add to ${title}`} onInput={e => setName((e.target as HTMLInputElement).value)} />
      {extra && <input class="input" style="flex:1;min-width:120px" type={extra.type || "text"} value={x} placeholder={extra.label} aria-label={extra.label} onInput={e => setX((e.target as HTMLInputElement).value)} />}
      {k === "allergies" && <label class="row small"><input type="checkbox" checked={severe} onChange={e => setSevere((e.target as HTMLInputElement).checked)} />Severe</label>}
      <button class="btn">Add</button></form>
  </section>;
}

// ---------------------------------------------------------------- wellbeing
export function Checkin() {
  const v = vault.value!; const week = v.health.checkins.slice(-14);
  const [mood, setMood] = useState(3), [sleep, setSleep] = useState("7"), [energy, setEnergy] = useState(3), [note, setNote] = useState(""), [saved, setSaved] = useState(false);
  const save = () => { update(x => { x.health.checkins.push({ at: new Date().toISOString(), mood, sleep: Number(sleep) || 0, energy, note }); }); setSaved(true); setNote(""); };
  const low = week.slice(-5).filter(c => c.mood <= 2).length >= 3;
  return <Page eyebrow="Health" title="Wellbeing" back="/health" sub="A minute a day to notice how you are.">
    <div class="card">
      <span class="eyebrow">Mood</span><Scale value={mood} onChange={setMood} labels={["Very low", "Low", "Okay", "Good", "Very good"]} />
      <span class="eyebrow">Energy</span><Scale value={energy} onChange={setEnergy} labels={["Exhausted", "Tired", "Okay", "Good", "Full of energy"]} />
      <Field label="Hours of sleep last night" inputMode="decimal" value={sleep} onInput={setSleep} />
      <Field label="Anything on your mind?" hint="Private: only you can read it." area value={note} onInput={setNote} />
      <button class="btn btn-primary" onClick={save}>Save today's check-in</button>{saved && <p class="small" role="status">Saved.</p>}
    </div>
    {low && <Notice kind="warn">Your last few check-ins have been low. Talking to someone can help. <a href="#/health/care">Find a support line</a>.</Notice>}
    {week.length > 1 && <div class="card"><h3>The last two weeks</h3><Spark values={week.map(c => c.mood)} min={1} max={5} label="Mood over two weeks" />
      <span class="muted small">Average sleep {(week.filter(c => c.sleep).reduce((s, c) => s + c.sleep, 0) / Math.max(1, week.filter(c => c.sleep).length)).toFixed(1)} hours.</span></div>}
    <Breathe />
  </Page>;
}
function Scale({ value, onChange, labels }: { value: number; onChange: (n: number) => void; labels: string[] }) {
  return <div class="seg" role="group">{labels.map((l, i) => <button key={l} aria-pressed={value === i + 1} onClick={() => onChange(i + 1)}>{l}</button>)}</div>;
}
function Breathe() {
  const [on, setOn] = useState(false), [phase, setPhase] = useState(0);
  const PH = ["Breathe in", "Hold", "Breathe out", "Hold"];
  useEffect(() => { if (!on) return; const t = setInterval(() => setPhase(p => (p + 1) % 4), 4000); return () => clearInterval(t); }, [on]);
  return <div class="card soft" style="text-align:center"><h3 style="justify-content:center">Box breathing</h3>
    <p class="muted small">Four counts in, hold, out, hold. A simple way to steady yourself.</p>
    <div class="breath" style={on ? `transform:scale(${phase === 0 || phase === 1 ? 1.15 : 0.8})` : ""} aria-live="polite">{on ? PH[phase] : "Ready"}</div>
    <button class="btn" style="align-self:center" onClick={() => { setOn(!on); setPhase(0); }}>{on ? "Stop" : "Start"}</button></div>;
}

// ---------------------------------------------------------------- vitals
export function Vitals() {
  const v = vault.value!; const all = v.health.vitals;
  const [kind, setKind] = useState("hr"), [a, setA] = useState(""), [b, setB] = useState("");
  const U: Record<string, string> = { hr: "bpm", bp: "mmHg", temp: "°C", weight: "kg", spo2: "%" };
  const add = (e: Event) => { e.preventDefault(); const val = Number(a); if (!val) return;
    update(x => { x.health.vitals.push({ kind: kind as "hr", at: new Date().toISOString(), value: val, value2: kind === "bp" ? Number(b) : undefined, unit: U[kind], source: "Manual" }); }); setA(""); setB(""); };
  return <Page eyebrow="Health" title="Vitals" back="/health" sub="Readings you enter or that come from your health devices.">
    <form class="card" onSubmit={add}><h3>Add a reading</h3>
      <div class="seg" role="group" aria-label="Kind of reading">{[["hr", "Heart rate"], ["bp", "Blood pressure"], ["temp", "Temperature"], ["weight", "Weight"], ["spo2", "Oxygen"]].map(([k, l]) =>
        <button type="button" key={k} aria-pressed={kind === k} onClick={() => setKind(k)}>{l}</button>)}</div>
      <div class="row"><input class="input" style="flex:1;min-width:120px" inputMode="decimal" value={a} onInput={e => setA((e.target as HTMLInputElement).value)} aria-label={kind === "bp" ? "Systolic (top number)" : "Value"} placeholder={kind === "bp" ? "Top number" : U[kind]} />
        {kind === "bp" && <input class="input" style="flex:1;min-width:120px" inputMode="decimal" value={b} onInput={e => setB((e.target as HTMLInputElement).value)} aria-label="Diastolic (bottom number)" placeholder="Bottom number" />}
        <button class="btn btn-primary">Add</button></div>
      <a class="small" href="#/devices">Or connect a Bluetooth device →</a></form>
    {all.length ? <ul class="list card">{[...all].reverse().slice(0, 40).map((r, i) => <li key={i}><div class="grow"><strong>{describe(r)}</strong><div class="muted small">{fmtTime(r.at)} · {r.source}</div></div></li>)}</ul> : <p class="muted">No readings yet.</p>}
  </Page>;
}

// ---------------------------------------------------------------- where to get care
export function Care() {
  const [code, setCode] = useState(settings.value.country);
  const c = COUNTRIES.find(x => x.code === code) || COUNTRIES[COUNTRIES.length - 1];
  return <Page eyebrow="Health" title="Where to get help" back="/health">
    <label class="field" style="max-width:320px">Country<select value={code} onChange={e => { const val = (e.target as HTMLSelectElement).value; setCode(val); update(x => { x.settings.country = val; }); }}>
      {COUNTRIES.map(x => <option value={x.code} key={x.code}>{x.name}</option>)}</select></label>
    <a class="btn btn-danger btn-block" href={`tel:${c.emergency.split(" ")[0]}`}>Emergency: call {c.emergency}</a>
    <ul class="list card">{c.lines.map(l => <li key={l.label}><div class="grow"><strong>{l.label}</strong><div class="muted small">{l.note}</div></div>
      <div class="row" style="justify-content:flex-end">{l.number && <a class="btn btn-small btn-primary" href={`tel:${l.number.replace(/[^\d+]/g, "")}`}>{l.number}</a>}{l.url && <a class="btn btn-small" href={l.url} target="_blank" rel="noopener">Website ↗</a>}</div></li>)}</ul>
    <p class="small muted">Checked October 2026. If you are in another country, <a href="https://findahelpline.com/" target="_blank" rel="noopener">Find a Helpline</a> lists crisis lines worldwide.</p>
  </Page>;
}

// ---------------------------------------------------------------- trusted information and medicine lookup
export function Info() {
  return <Page eyebrow="Health" title="Trusted information" back="/health" sub="Sources run by health authorities and non-profits, not advertisers.">
    <div class="grid2">{INFO.map(s => <a class="card" key={s.url} href={s.url} target="_blank" rel="noopener"><strong>{s.name} ↗</strong><span class="muted small">{s.by}</span><span class="small">{s.note}</span></a>)}</div>
    <MedicineLookup />
  </Page>;
}
function MedicineLookup() {
  const [q, setQ] = useState(""), [res, setRes] = useState<{ name: string; purpose?: string; warnings?: string } | null>(null), [err, setErr] = useState("");
  const run = async (e: Event) => {
    e.preventDefault(); const term = q.trim().toLowerCase().replace(/"/g, ""); if (!term) return; setErr(""); setRes(null);
    try {
      const r = await fetch(`https://api.fda.gov/drug/label.json?search=openfda.generic_name:"${encodeURIComponent(term)}"+openfda.brand_name:"${encodeURIComponent(term)}"&limit=1`);
      if (r.status === 404) { setErr("No label found for that name in the US FDA database. Try the generic name."); return; }
      const d = (await r.json()).results?.[0]; if (!d) { setErr("No label found."); return; }
      const first = (x?: string[]) => x?.[0]?.replace(/\s+/g, " ").slice(0, 600);
      setRes({ name: d.openfda?.generic_name?.[0] || term, purpose: first(d.purpose) || first(d.indications_and_usage), warnings: first(d.warnings) || first(d.boxed_warning) });
    } catch { setErr("The FDA database can't be reached from here right now."); }
  };
  return <div class="card"><h3>Look up a medicine</h3>
    <form class="row" onSubmit={run}><input class="input" style="flex:1;min-width:160px" value={q} onInput={e => setQ((e.target as HTMLInputElement).value)} placeholder="e.g. ibuprofen" aria-label="Medicine name" /><button class="btn">Look up</button></form>
    {err && <Notice kind="warn">{err}</Notice>}
    {res && <div class="stack" style="gap:8px"><strong style="text-transform:capitalize">{res.name.toLowerCase()}</strong>{res.purpose && <p class="small"><strong>Used for:</strong> {res.purpose}…</p>}{res.warnings && <p class="small"><strong>Warnings:</strong> {res.warnings}…</p>}
      <p class="small muted">From the US label (openFDA). Labels differ between countries. Ask a pharmacist before taking anything new.</p></div>}
    <p class="small muted">Plain-language guides: {MEDICINE_LINKS.map((l, i) => <span key={l.url}>{i ? " · " : ""}<a href={l.url} target="_blank" rel="noopener">{l.name}</a></span>)}</p>
  </div>;
}
