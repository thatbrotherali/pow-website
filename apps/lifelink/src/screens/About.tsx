// About: why LifeLink exists, what this prototype is and isn't, how it's built, and the road ahead.
import { useState } from "preact/hooks";
import { vault, update, mode, settings } from "../lib/model";
import { changePin } from "../lib/crypto";
import { lockNow } from "../lib/session";
import { COUNTRIES } from "../data/health";
import { Field, Notice, Page, Toggle } from "../ui/ui";

const SITE = "https://peopleoftheworld.net";

export function About() {
  return <Page eyebrow="About" title="About this prototype" sub="LifeLink, from the Plan to End Poverty by 2050.">
    <div class="card accent"><h2 style="font-size:1.25rem">Why connect every person?</h2>
      <p>Because every person matters. Much of what makes poverty hard to end is not the cost of care, but not knowing who needs what: people registered six times, payments lost to names that don't exist, others missed until they become emergencies. LifeLink lets a community count every person without watching anyone.</p>
      <p class="muted">Behind it is a simple conviction: that each person carries a portion of the Creator within, so no one is a number and no one should be left behind. <a href={`${SITE}/why.html`}>Why it all connects</a>.</p></div>

    <div class="card"><h2 style="font-size:1.25rem">What works in this prototype</h2>
      <ul style="margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px">
        <li>A digital ID you can show by QR, revealing only what you choose, checked by any phone with no internet.</li>
        <li>Unlock with a PIN or your fingerprint or face (passkeys); your biometric never leaves your device.</li>
        <li>Everything stored on your device, encrypted (AES-256, with Argon2id for the PIN).</li>
        <li>A Civic Credits wallet: earn, spend, and pay people by signed QR code, offline, with a ledger you can check for tampering.</li>
        <li>A learning guide that explains its suggestions, built-in lessons with review, signed certificates, and a map of free sources up to university.</li>
        <li>A Medical ID for the lock screen, a health record you can export in the international FHIR standard, wellbeing check-ins and live readings from Bluetooth health devices.</li>
        <li>SOS that only you can trigger, area alerts matched on your device, and anonymous needs surveys.</li>
        <li>Read-aloud on every page, larger text, high contrast, and it installs to your home screen and works offline.</li></ul></div>

    <div class="card"><h2 style="font-size:1.25rem">What it isn't, yet</h2>
      <ul style="margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px">
        <li>Credits are demonstration credits with no value. Real credits need a participating council and the legal setup in the plan.</li>
        <li>IDs and certificates are signed by a demonstration issuer whose keys are public, so they prove the technology, not a person's identity.</li>
        <li>Nothing is sent to the police, emergency services or any government. SOS prepares messages that you send.</li>
        <li>There is no symptom checker: diagnosis needs clinical testing and approval as a medical device.</li>
        <li>Bluetooth devices don't work in Safari on iPhone, and on-device AI is limited to some desktop computers, until the native app.</li>
        <li>It is in English. Translation into many languages is part of the pilot.</li>
        <li>It hasn't had an independent security audit. That comes before any real data is trusted to it.</li></ul></div>

    <div class="card"><h2 style="font-size:1.25rem">How it's built</h2>
      <p class="small">One codebase for phones, tablets and computers: a Progressive Web App written in TypeScript with Preact, using only open standards. The browser's Web Crypto for encryption and signatures; Argon2id for the PIN; passkeys (WebAuthn, with the PRF extension) for biometric unlock; selective-disclosure credentials (IETF SD-JWT, RFC 9901) with a post-quantum signature (ML-DSA, NIST FIPS 204); a hash-chained ledger; health records in HL7 FHIR (International Patient Summary); the Bluetooth SIG health profiles; randomised response for anonymous surveys. No trackers, no third-party scripts, and fonts bundled with the app.</p></div>

    <div class="card"><h2 style="font-size:1.25rem">The road ahead</h2>
      <ol style="margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px">
        <li><strong>Prototype (now):</strong> every module working on any device, all data local.</li>
        <li><strong>Pilot app:</strong> app-store versions with Apple Health, Android Health Connect and NFC; a Poverty Elimination Center issuing real IDs and certificates; the council running the credits ledger; an independent security audit; translation.</li>
        <li><strong>Pilot hardware:</strong> the LifeLink Tablet and wearables, with keys in secure hardware and mesh networking for places without coverage.</li></ol>
      <p class="small"><a href={`${SITE}/plan-to-end-poverty/lifelink/`}>LifeLink and its 32 papers</a> · <a href={`${SITE}/builders.html`}>Help build it</a></p></div>
    <p class="footer-note">LifeLink prototype · People of the World · Every person counted, no person tracked.</p>
  </Page>;
}

export function Settings() {
  const s = settings.value; const set = (fn: (x: typeof s) => void) => update(v => fn(v.settings));
  const [pin, setPin] = useState(""), [msg, setMsg] = useState("");
  return <Page eyebrow="Settings" title="Settings">
    <div class="card"><h3>Reading</h3>
      <label class="field">Text size<div class="seg" role="group" aria-label="Text size">{[90, 100, 115, 130, 150].map(n => <button key={n} aria-pressed={s.textSize === n} onClick={() => set(x => { x.textSize = n; })}>{n}%</button>)}</div></label>
      <label class="field">Appearance<div class="seg" role="group" aria-label="Appearance">{(["auto", "light", "dark"] as const).map(t => <button key={t} aria-pressed={s.theme === t} onClick={() => set(x => { x.theme = t; })} style="text-transform:capitalize">{t === "auto" ? "Match device" : t}</button>)}</div></label>
      <Toggle checked={s.contrast} onChange={x => set(y => { y.contrast = x; })} label="Higher contrast" />
      <Toggle checked={s.reduceMotion} onChange={x => set(y => { y.reduceMotion = x; })} label="Reduce motion" />
      <p class="small muted">Every page has a Listen button that reads it aloud, using your device's own voice.</p></div>
    <div class="card"><h3>Country</h3><p class="small muted">For emergency numbers and health lines.</p>
      <select class="input" value={s.country} onChange={e => set(x => { x.country = (e.target as HTMLSelectElement).value; })} aria-label="Country">{COUNTRIES.map(c => <option key={c.code} value={c.code}>{c.name}</option>)}</select></div>
    {mode.value === "own" && <div class="card"><h3>Security</h3>
      <label class="field">Lock after<select value={s.autoLockMin} onChange={e => set(x => { x.autoLockMin = Number((e.target as HTMLSelectElement).value); })}>{[1, 2, 5, 10, 30].map(n => <option key={n} value={n}>{n} minute{n > 1 ? "s" : ""} without use</option>)}</select></label>
      <Field label="New PIN" type="password" inputMode="numeric" value={pin} onInput={v => setPin(v.replace(/\D/g, ""))} class="input pin" maxLength={12} />
      <button class="btn btn-small" style="align-self:flex-start" disabled={pin.length < 6} onClick={async () => { await changePin(pin); setPin(""); setMsg("PIN changed."); }}>Change PIN</button>{msg && <p class="small" role="status">{msg}</p>}
      <button class="btn" style="align-self:flex-start" onClick={() => lockNow()}>Lock now</button></div>}
    {mode.value === "demo" && <Notice kind="info">You're in the demonstration. <button class="link" onClick={() => lockNow()}>Leave it</button> to create your own LifeLink.</Notice>}
    <p class="small muted">Signed in as {vault.value?.person.name}.</p>
  </Page>;
}
