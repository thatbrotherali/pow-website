// My data: what LifeLink holds, who has looked, what you've agreed to, and export or erase it all.
import { useState } from "preact/hooks";
import { vault, update, mode, logAccess, flush } from "../lib/model";
import { ipsBundle } from "../lib/fhir";
import { eraseEverything, lockNow } from "../lib/session";
import { DemoNote, Notice, Page, Sheet, Toggle, download, fmtTime } from "../ui/ui";

const CONSENTS: { id: string; label: string; hint: string }[] = [
  { id: "health-in-sos", label: "Include my Medical ID in SOS alerts", hint: "So the people you alert know your allergies and conditions." },
  { id: "share-learning-with-pec", label: "Share my learning progress with my Poverty Elimination Center", hint: "So staff can suggest training and confirm certificates. Only progress, never your answers." },
  { id: "research-totals", label: "Count me in area totals", hint: "Your answers to needs surveys are added to anonymous totals, using randomised response." }
];

export function MyData() {
  const v = vault.value!;
  const [confirm, setConfirm] = useState(false);
  const counts = [["Identity", `1 ID, ${v.certificates.length} certificates`], ["Wallet", `${v.ledger.length} ledger entries`], ["Learning", `${Object.keys(v.learning.done).length} lessons, ${v.learning.saved.length} saved sources`],
    ["Health", `${v.health.conditions.length + v.health.medications.length + v.health.allergies.length + v.health.immunizations.length} record entries, ${v.health.vitals.length} readings, ${v.health.checkins.length} check-ins`],
    ["Safety", `${v.safety.contacts.length} contacts, ${v.safety.reports.length} reports`], ["Your say", `${Object.keys(v.voice.votes).length} votes`]];
  const exportAll = async () => { await flush(); download(`lifelink-data-${new Date().toISOString().slice(0, 10)}.json`, JSON.stringify({ exported: new Date().toISOString(), note: "Everything LifeLink held about you on this device.", data: v }, null, 2)); logAccess("You", "Exported all your data", "Your choice"); };
  return <Page eyebrow="My data" title="Your data, your rules" sub="Everything LifeLink holds about you is on this device. Here is all of it.">
    {mode.value === "demo" ? <DemoNote>Amara's data lives only in this browser tab's memory. Close the tab and it's gone.</DemoNote>
      : <Notice kind="ok">Stored only on this device, encrypted with AES-256. No copy exists on any server: not ours, not a government's.</Notice>}
    <div class="card"><h3>In plain words</h3>
      <ul class="small" style="margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px">
        <li>LifeLink keeps what you put in, and nothing it hasn't told you about. No advertising, no tracking, no analytics.</li>
        <li>Your fingerprint or face never reaches LifeLink. Your phone checks it and releases a key.</li>
        <li>Your location is read only when you ask (area alerts, SOS) and is never stored or sent.</li>
        <li>Anything you share, such as an ID code or a health summary, is shared by you, and written in your access log.</li>
        <li>You can take everything with you, or erase it, at any time.</li></ul></div>
    <div class="card"><h3>What's here</h3><table class="table"><tbody>{counts.map(([a, b]) => <tr key={a}><th>{a}</th><td>{b}</td></tr>)}</tbody></table></div>
    <div class="card"><h3>What you've agreed to</h3><p class="muted small">Each is off unless you switch it on, and you can change your mind at any time.</p>
      {CONSENTS.map(c => <Toggle key={c.id} checked={!!v.consents[c.id]} label={c.label} hint={c.hint} onChange={x => { update(y => { y.consents[c.id] = x; }); logAccess("You", x ? "Gave consent" : "Withdrew consent", c.label); }} />)}</div>
    <div class="card"><h3>Who has looked</h3><p class="muted small">Every time your record is opened, shared or changed by anyone, it's written here.</p>
      <ul class="list">{v.access.slice(0, 25).map((a, i) => <li key={i}><div class="grow"><strong>{a.who}</strong> <span class="muted">{a.what.toLowerCase()}</span><div class="muted small">{a.why} · {fmtTime(a.at)}</div></div></li>)}</ul></div>
    <div class="card"><h3>Take it with you</h3>
      <div class="row"><button class="btn" onClick={exportAll}>Export everything (JSON)</button>
        <button class="btn" onClick={() => { download("health-summary.json", JSON.stringify(ipsBundle(v.person.name, v.person.birthDate, v.health), null, 2), "application/fhir+json"); logAccess("You", "Exported your health summary", "FHIR IPS"); }}>Export health summary (FHIR IPS)</button></div>
      <p class="small muted">Exports are not encrypted. Keep them somewhere safe.</p></div>
    {mode.value === "own" && <div class="card" style="border-color:var(--danger)"><h3>Erase everything</h3><p class="muted small">Deletes your LifeLink from this device for good: ID, keys, credits, health record, everything.</p>
      <button class="btn btn-danger" style="align-self:flex-start" onClick={() => setConfirm(true)}>Erase my LifeLink</button></div>}
    {mode.value === "demo" && <button class="btn" onClick={() => lockNow()}>Leave the demonstration</button>}
    {confirm && <Erase onClose={() => setConfirm(false)} />}
  </Page>;
}

export function Erase({ onClose }: { onClose: () => void }) {
  const [text, setText] = useState("");
  return <Sheet title="Erase your LifeLink?" onClose={onClose}>
    <p>This can't be undone. Type <strong>ERASE</strong> to confirm.</p>
    <input class="input" value={text} onInput={e => setText((e.target as HTMLInputElement).value)} aria-label="Type ERASE to confirm" />
    <button class="btn btn-danger" disabled={text !== "ERASE"} onClick={async () => { await eraseEverything(); location.hash = "/"; location.reload(); }}>Erase everything</button>
  </Sheet>;
}
