// Safety: features that can call for help, each with the rule that keeps it from being used to watch people.
import { useEffect, useRef, useState } from "preact/hooks";
import { vault, update, mode, logAccess, settings } from "../lib/model";
import { inside, km } from "../lib/privacy";
import { ALERTS, DEMO_PLACE } from "../data/community";
import { COUNTRIES } from "../data/health";
import { DemoNote, Field, Icon, Notice, Page, Toggle, fmtTime } from "../ui/ui";

export function Safety() {
  const v = vault.value!;
  return <Page eyebrow="Safety" title="Safety" sub="Help when you call for it, and nothing watching when you don't.">
    <a class="card" href="#/sos" style="border-color:var(--danger)"><h3 style="color:var(--danger)"><Icon n="safety" />SOS</h3>
      <span class="muted">Hold the button to alert your chosen people and call for help. <strong>The rule:</strong> only you can trigger it, and nothing listens or records until you do.</span></a>
    <Contacts />
    <AreaAlerts />
    <Report />
    {v.safety.sos.length > 0 && <div class="card"><h3>Past SOS alerts</h3><ul class="list">{v.safety.sos.slice(0, 5).map((s, i) => <li key={i}><span class="grow">{fmtTime(s.at)}</span><span class="muted small">{s.outcome}</span></li>)}</ul></div>}
  </Page>;
}

function Contacts() {
  const cs = vault.value!.safety.contacts; const consent = vault.value!.consents["health-in-sos"];
  const [n, setN] = useState(""), [p, setP] = useState(""), [r, setR] = useState("");
  return <section class="card" aria-label="Trusted contacts"><h3>People to alert</h3>
    <p class="muted small"><strong>The rule:</strong> you choose who is told. Your location is shared once, for the emergency, and then stops.</p>
    {cs.length ? <ul class="list">{cs.map((c, i) => <li key={i}><div class="grow"><strong>{c.name}</strong><div class="muted small">{c.relation} · {c.phone}</div></div>
      <button class="btn btn-small btn-ghost" aria-label={`Remove ${c.name}`} onClick={() => update(x => { x.safety.contacts.splice(i, 1); })}>Remove</button></li>)}</ul> : <p class="muted small">No one yet.</p>}
    <form class="grid3" onSubmit={e => { e.preventDefault(); if (!n.trim() || !p.trim()) return; update(x => { x.safety.contacts.push({ name: n.trim(), phone: p.trim(), relation: r.trim() || "Contact" }); }); setN(""); setP(""); setR(""); }}>
      <Field label="Name" value={n} onInput={setN} /><Field label="Mobile number" type="tel" value={p} onInput={setP} /><Field label="Who are they?" value={r} onInput={setR} placeholder="Sister" />
      <button class="btn" style="align-self:end">Add</button></form>
    <Toggle checked={consent} onChange={x => update(v => { v.consents["health-in-sos"] = x; })} label="Include my Medical ID in SOS alerts" hint="Allergies, conditions and medicines, so helpers know. Off unless you switch it on." />
  </section>;
}

function AreaAlerts() {
  const v = vault.value!;
  const [where, setWhere] = useState<{ lat: number; lon: number; label: string } | null>(v.location || null), [msg, setMsg] = useState("");
  const locate = () => {
    if (mode.value === "demo") { setWhere({ ...DEMO_PLACE }); setMsg("Using Amara's sample location."); return; }
    if (!navigator.geolocation) { setMsg("This device can't share its location with the browser."); return; }
    setMsg("Finding where you are…");
    navigator.geolocation.getCurrentPosition(p => { setWhere({ lat: p.coords.latitude, lon: p.coords.longitude, label: "Your location just now" }); setMsg("Checked on this device. Your location wasn't saved or sent."); },
      () => setMsg("Location wasn't shared. You can still read every alert below."), { timeout: 10000, maximumAge: 60000 });
  };
  return <section class="card" aria-label="Area alerts"><h3>Alerts for your area</h3>
    <p class="muted small"><strong>The rule:</strong> alerts are sent to an area, and your device decides whether you're in it. Your location goes nowhere.</p>
    <button class="btn btn-small" style="align-self:flex-start" onClick={locate}>Check where I am now</button>{msg && <p class="small" role="status">{msg}</p>}
    <ul class="list">{ALERTS.map(a => { const inArea = where ? inside([where.lat, where.lon], a.area) : null;
      const near = where && !inArea ? km([where.lat, where.lon], a.area[0]) : null;
      return <li key={a.id}><div class="grow"><strong>{a.title}</strong><div class="small">{a.detail}</div><div class="muted small">{a.kind} · from {a.by}</div></div>
        {inArea === null ? <span class="pill">Not checked</span> : inArea ? <span class="pill pill-bad">You're in this area</span> : <span class="pill">{near !== null && near < 50 ? `${near.toFixed(1)} km away` : "Not your area"}</span>}</li>; })}</ul>
    {mode.value === "demo" && <p class="small muted">Sample alerts for the demonstration district.</p>}
  </section>;
}

function Report() {
  const [kind, setKind] = useState("Something unsafe"), [text, setText] = useState(""), [anon, setAnon] = useState(true), [done, setDone] = useState(false);
  return <section class="card" aria-label="Report"><h3>Report something</h3>
    <p class="muted small"><strong>The rule:</strong> reports are logged and can be audited, with protections against false reports. Witnesses take part only if they agree.</p>
    {done ? <Notice kind="ok">Saved on your device. In a pilot it goes to the right service, and you can follow what happens to it.</Notice> : <>
      <label class="field">What kind?<select value={kind} onChange={e => setKind((e.target as HTMLSelectElement).value)}>{["Something unsafe", "A crime", "A hazard (fire, flood, damage)", "Corruption or misuse of public money"].map(k => <option key={k}>{k}</option>)}</select></label>
      <Field label="What happened?" area value={text} onInput={setText} />
      <Toggle checked={anon} onChange={setAnon} label="Report anonymously" hint="Your name and LifeLink number are left off the report." />
      <button class="btn btn-primary" style="align-self:flex-start" disabled={!text.trim()} onClick={() => { update(x => { x.safety.reports.unshift({ at: new Date().toISOString(), kind, text, anonymous: anon }); }); logAccess("You", "Made a report", kind); setDone(true); }}>Save report</button>
      <DemoNote>Nothing is sent to the police or any authority.</DemoNote></>}
  </section>;
}

// ---------------------------------------------------------------- SOS: hold, count down (cancel any time), then alert
export function Sos() {
  const v = vault.value!; const c = COUNTRIES.find(x => x.code === settings.value.country) || COUNTRIES[COUNTRIES.length - 1];
  const [stage, setStage] = useState<"ready" | "count" | "active">("ready"), [n, setN] = useState(5), [held, setHeld] = useState(0);
  const [loc, setLoc] = useState<string>(""), hold = useRef<number | undefined>(undefined);
  useEffect(() => { if (stage !== "count") return; if (n <= 0) { activate(); return; } const t = setTimeout(() => setN(n - 1), 1000); return () => clearTimeout(t); }, [stage, n]);
  const startHold = () => { const t0 = Date.now(); hold.current = window.setInterval(() => { const p = Math.min(1, (Date.now() - t0) / 2000); setHeld(p); if (p >= 1) { clearInterval(hold.current); setStage("count"); setN(5); } }, 50); };
  const endHold = () => { clearInterval(hold.current); if (stage === "ready") setHeld(0); };
  const activate = () => {
    setStage("active");
    if (mode.value === "demo") setLoc(`${DEMO_PLACE.lat.toFixed(5)}, ${DEMO_PLACE.lon.toFixed(5)}`);
    else navigator.geolocation?.getCurrentPosition(p => setLoc(`${p.coords.latitude.toFixed(5)}, ${p.coords.longitude.toFixed(5)}`), () => setLoc(""), { enableHighAccuracy: true, timeout: 10000 });
    update(x => { x.safety.sos.unshift({ at: new Date().toISOString(), outcome: mode.value === "demo" ? "Demonstration" : "Alert prepared" }); });
    logAccess("You", "Triggered SOS", "Emergency");
  };
  const med = v.consents["health-in-sos"] ? ` Medical: allergies ${v.health.allergies.map(a => a.name).join(", ") || "none"}; ${v.health.conditions.map(x => x.name).join(", ")}.` : "";
  const msg = `SOS from ${v.person.name} via LifeLink. I need help.${loc ? ` My location: https://www.openstreetmap.org/?mlat=${loc.split(", ")[0]}&mlon=${loc.split(", ")[1]}#map=17/${loc.replace(", ", "/")}` : ""}${med}`;
  const demo = mode.value === "demo";
  return <Page eyebrow="Safety" title="SOS" back="/safety" listen={false}>
    {stage === "ready" && <div class="stack" style="text-align:center">
      <p class="muted">Press and hold for two seconds. You'll have five seconds to cancel.</p>
      <button class="sos-hold" onPointerDown={startHold} onPointerUp={endHold} onPointerLeave={endHold} onContextMenu={e => e.preventDefault()}
        onKeyDown={e => { if ((e.key === "Enter" || e.key === " ") && !e.repeat) { e.preventDefault(); startHold(); } }} onKeyUp={endHold} aria-label="Hold for SOS">
        <span class="ring" style={`transform:scale(${1 + held * 0.15});opacity:${0.25 + held * 0.6}`} />SOS</button>
      <p class="small muted">Only you can trigger this. Nothing listens or records until you do.</p>
    </div>}
    {stage === "count" && <div class="stack" style="text-align:center" role="alert"><p>Sending SOS in</p><div class="countdown">{n}</div>
      <button class="btn btn-block" style="min-height:64px;font-size:1.2rem" onClick={() => { setStage("ready"); setHeld(0); }}>Cancel</button></div>}
    {stage === "active" && <div class="stack">
      {demo ? <DemoNote>In the demonstration nothing is sent and no call is made. This is what Amara would see.</DemoNote>
        : <Notice kind="danger">The prototype runs in a browser, which can't send messages by itself. Use the buttons below; the LifeLink app and devices send alerts automatically.</Notice>}
      <a class="btn btn-danger btn-block" style="min-height:64px;font-size:1.2rem" href={demo ? undefined : `tel:${c.emergency.split(" ")[0]}`} aria-disabled={demo} onClick={e => { if (demo) e.preventDefault(); }}>Call emergency services ({c.emergency})</a>
      <div class="card"><h3>Alert your people</h3>
        {v.safety.contacts.length ? v.safety.contacts.map(ct => <a key={ct.phone} class="btn" href={demo ? undefined : `sms:${ct.phone.replace(/\s/g, "")}?&body=${encodeURIComponent(msg)}`} onClick={e => { if (demo) e.preventDefault(); }}>Message {ct.name} ({ct.relation})</a>)
          : <p class="muted">No contacts yet. <a href="#/safety">Add them under Safety</a>.</p>}
        {"share" in navigator && !demo && <button class="btn" onClick={() => navigator.share({ title: "SOS", text: msg }).catch(() => {})}>Send with another app</button>}
        <p class="small muted">Message: “{msg}”</p></div>
      <p class="small muted">{loc ? "Your location was read once, for this alert. It isn't being tracked." : "Location isn't available; the message is sent without it."}</p>
      <button class="btn btn-block" onClick={() => { update(x => { if (x.safety.sos[0]) x.safety.sos[0].outcome = "Ended: safe"; }); setStage("ready"); setHeld(0); }}>I'm safe now</button>
    </div>}
  </Page>;
}
