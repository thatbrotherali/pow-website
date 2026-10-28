// Welcome, create your LifeLink, unlock, and the emergency Medical ID shown on the lock screen.
import { useEffect, useState } from "preact/hooks";
import { Field, Icon, Notice, Sheet } from "../ui/ui";
import { startDemo, createOwn, unlock, unlockPasskey } from "../lib/session";
import { vaultMeta, platformAuthenticator } from "../lib/crypto";
import { db } from "../lib/db";

export function Welcome({ hasVault }: { hasVault: boolean }) {
  const [step, setStep] = useState<"intro" | "create">("intro");
  const [busy, setBusy] = useState(false);
  if (hasVault) return <Unlock />;
  if (step === "create") return <Create onBack={() => setStep("intro")} />;
  return <div class="stack fade-in" style="max-width:640px;margin:0 auto">
    <div class="hero">
      <span class="eyebrow" style="color:var(--band-muted)">End Poverty by Design · Prototype</span>
      <h1>One link to every public service.</h1>
      <p class="muted">LifeLink gives every person a secure identity and wallet, free, on a phone they already own. Through it people receive Civic Credits, learn, see a doctor, call for help and take part in decisions.</p>
      <p class="muted">This prototype shows what can be built today. It runs on phones, tablets and computers, works offline, and keeps everything on your device, encrypted.</p>
    </div>
    <div class="grid2">
      <div class="card accent">
        <h2 class="h3" style="font-size:1.1rem;display:flex;gap:8px;align-items:center"><Icon n="spark" />Explore with a sample person</h2>
        <span class="muted">Meet Amara, who already uses LifeLink. Nothing you do is saved. The quickest way to see everything.</span>
        <button class="btn btn-primary" style="align-self:flex-start" disabled={busy} onClick={async () => { setBusy(true); await startDemo(); }}>{busy ? "Opening…" : "Explore the demo"}</button>
      </div>
      <div class="card">
        <h2 style="font-size:1.1rem;display:flex;gap:8px;align-items:center"><Icon n="lock" />Create your own</h2>
        <span class="muted">Set a PIN and try LifeLink with your own details. Everything stays on this device, encrypted, and you can erase it in one step.</span>
        <button class="btn" style="align-self:flex-start" onClick={() => setStep("create")}>Create my LifeLink</button>
      </div>
    </div>
    <Notice kind="info">A working prototype, not a public service yet. Credits are demonstration credits with no value, and nothing is sent to any government, police or emergency service. <a href="#/about">What it is and isn't</a>.</Notice>
  </div>;
}

function Create({ onBack }: { onBack: () => void }) {
  const [name, setName] = useState(""), [birth, setBirth] = useState(""), [region, setRegion] = useState("");
  const [pin, setPin] = useState(""), [pin2, setPin2] = useState(""), [err, setErr] = useState(""), [busy, setBusy] = useState(false);
  const submit = async (e: Event) => {
    e.preventDefault(); setErr("");
    if (name.trim().length < 2) return setErr("Please enter your name.");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(birth) || new Date(birth) > new Date()) return setErr("Please enter your date of birth.");
    if (!/^\d{6,}$/.test(pin)) return setErr("Your PIN needs at least 6 digits.");
    if (/^(\d)\1+$/.test(pin) || "0123456789".includes(pin) || "9876543210".includes(pin)) return setErr("That PIN is too easy to guess. Avoid repeated or sequential digits.");
    if (pin !== pin2) return setErr("The two PINs don't match.");
    setBusy(true);
    try { await createOwn(name, birth, region || "Not given", pin); }
    catch { setErr("Something went wrong creating your vault. Is private browsing switched on? It can block storage."); setBusy(false); }
  };
  return <form class="stack fade-in" style="max-width:520px;margin:0 auto" onSubmit={submit}>
    <button type="button" class="link small" style="align-self:flex-start" onClick={onBack}>← Back</button>
    <h1>Create your LifeLink</h1>
    <p class="muted">In a real rollout, staff at a Poverty Elimination Center would check your identity in person before issuing your LifeLink ID. Here, what you enter is self-declared.</p>
    <Field label="Your name" value={name} onInput={setName} autocomplete="name" />
    <Field label="Date of birth" type="date" value={birth} onInput={setBirth} autocomplete="bday" />
    <Field label="Town or district" hint="Optional. Used for local proposals and alerts." value={region} onInput={setRegion} />
    <Field label="Choose a PIN" hint="At least 6 digits. It unlocks your LifeLink and can't be recovered, so remember it." type="password" inputMode="numeric" autocomplete="new-password" value={pin} onInput={v => setPin(v.replace(/\D/g, ""))} class="input pin" maxLength={12} />
    <Field label="Enter the PIN again" type="password" inputMode="numeric" autocomplete="new-password" value={pin2} onInput={v => setPin2(v.replace(/\D/g, ""))} class="input pin" maxLength={12} />
    {err && <Notice kind="danger">{err}</Notice>}
    <button class="btn btn-primary btn-block" disabled={busy}>{busy ? "Creating your encrypted vault…" : "Create my LifeLink"}</button>
    <p class="small muted">Your PIN is stretched with Argon2id into a key that encrypts everything with AES-256. You can add fingerprint or face unlock afterwards, under Identity.</p>
  </form>;
}

function Unlock() {
  const [pin, setPin] = useState(""), [err, setErr] = useState(""), [busy, setBusy] = useState(false);
  const [hasPasskey, setHasPasskey] = useState(false), [medical, setMedical] = useState(false), [showMed, setShowMed] = useState(false);
  useEffect(() => { (async () => { const m = await vaultMeta(); setHasPasskey(!!m?.passkey && await platformAuthenticator()); setMedical(!!(await db.get("lock-medical-id"))); })(); }, []);
  const go = async (e: Event) => { e.preventDefault(); setBusy(true); setErr(""); if (!(await unlock(pin))) { setErr("That PIN didn't work."); setPin(""); } setBusy(false); };
  const bio = async () => { setErr(""); const r = await unlockPasskey(); if (r) setErr(r); };
  return <div class="stack fade-in" style="max-width:420px;margin:0 auto;text-align:center">
    <div class="logo" style="width:64px;height:64px;font-size:30px;margin:10px auto 0;border-radius:18px">L</div>
    <h1>Welcome back</h1>
    <p class="muted">Your LifeLink is locked and encrypted on this device.</p>
    {hasPasskey && <button class="btn btn-primary btn-block" onClick={bio}><Icon n="lock" />Unlock with fingerprint or face</button>}
    <form class="stack" onSubmit={go}>
      <Field label="PIN" type="password" inputMode="numeric" autocomplete="current-password" value={pin} onInput={v => setPin(v.replace(/\D/g, ""))} class="input pin" maxLength={12} />
      {err && <Notice kind="danger">{err}</Notice>}
      <button class={`btn btn-block ${hasPasskey ? "" : "btn-primary"}`} disabled={busy || pin.length < 6}>{busy ? "Unlocking…" : "Unlock"}</button>
    </form>
    {medical && <button class="btn btn-danger btn-block" onClick={() => setShowMed(true)}>Emergency Medical ID</button>}
    <p class="small muted">Forgot your PIN? It can't be recovered: that is what keeps your data safe. You can <a href="#/erase">erase this LifeLink</a> and start again.</p>
    {showMed && <LockMedical onClose={() => setShowMed(false)} />}
  </div>;
}

type LockMed = { name: string; birthDate: string; bloodType: string; notes: string; organDonor: string; allergies: { name: string; severe?: boolean }[]; conditions: { name: string }[]; medications: { name: string; dose?: string }[]; contacts: { name: string; phone: string; relation: string }[] };
function LockMedical({ onClose }: { onClose: () => void }) {
  const [m, setM] = useState<LockMed | null>(null);
  useEffect(() => { db.get<LockMed>("lock-medical-id").then(x => setM(x ?? null)); }, []);
  if (!m) return null;
  return <Sheet title="Emergency Medical ID" onClose={onClose}>
    <p class="muted small">Shown without unlocking because the owner chose to, so responders can help.</p>
    <dl class="stack" style="gap:10px;margin:0">
      <div><dt class="eyebrow">Name</dt><dd style="margin:0" class="big" >{m.name}</dd><span class="muted">Born {m.birthDate}</span></div>
      {m.bloodType && <div><dt class="eyebrow">Blood type</dt><dd style="margin:0">{m.bloodType}</dd></div>}
      <div><dt class="eyebrow">Allergies</dt><dd style="margin:0">{m.allergies.length ? m.allergies.map(a => a.name + (a.severe ? " (severe)" : "")).join(", ") : "None recorded"}</dd></div>
      <div><dt class="eyebrow">Conditions</dt><dd style="margin:0">{m.conditions.map(c => c.name).join(", ") || "None recorded"}</dd></div>
      <div><dt class="eyebrow">Medicines</dt><dd style="margin:0">{m.medications.map(c => c.name + (c.dose ? `: ${c.dose}` : "")).join("; ") || "None recorded"}</dd></div>
      {m.notes && <div><dt class="eyebrow">Notes</dt><dd style="margin:0">{m.notes}</dd></div>}
      {m.organDonor && <div><dt class="eyebrow">Organ donor</dt><dd style="margin:0">{m.organDonor}</dd></div>}
      {!!m.contacts.length && <div><dt class="eyebrow">Emergency contacts</dt><dd style="margin:0">{m.contacts.map(c => <div key={c.phone}><a href={`tel:${c.phone.replace(/\s/g, "")}`}>{c.name} ({c.relation}): {c.phone}</a></div>)}</dd></div>}
    </dl>
  </Sheet>;
}
