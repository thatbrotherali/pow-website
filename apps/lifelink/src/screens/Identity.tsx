// Identity: the LifeLink ID, shown by QR with only the details you choose, and checked by anyone, offline.
import { useEffect, useState } from "preact/hooks";
import { vault, mode, logAccess, age } from "../lib/model";
import { holderKey, present, verifyPresentation, verifyPq, disclosuresOf, type Verified } from "../lib/credentials";
import { addPasskey, removePasskey, vaultMeta, platformAuthenticator } from "../lib/crypto";
import { DEMO_ISSUER } from "../data/demo-issuer";
import { DemoNote, Icon, Notice, Page, QR, Scanner, Sheet, fmtDate } from "../ui/ui";

const LABELS: Record<string, string> = { given_name: "First name", family_name: "Family name", birthdate: "Date of birth", age_over_18: "Over 18", age_over_65: "Over 65", region: "District", lifelink_number: "LifeLink number", course: "Course", provider: "Provider", completed: "Completed", score: "Score" };
const PRESETS: { id: string; label: string; reveal: string[] }[] = [
  { id: "adult", label: "Prove I'm over 18", reveal: ["age_over_18"] },
  { id: "name", label: "Name and age check", reveal: ["given_name", "family_name", "age_over_18"] },
  { id: "full", label: "Full ID", reveal: ["given_name", "family_name", "birthdate", "region", "lifelink_number"] }
];
const show = (v: unknown) => v === true ? "Yes" : v === false ? "No" : String(v);

export function Identity() {
  const v = vault.value!; const c = v.idCredential;
  const [sheet, setSheet] = useState<"" | "show" | "scan" | "hood">("");
  const [result, setResult] = useState<Verified | null>(null);
  return <Page eyebrow="Identity" title="Your LifeLink ID" sub="A digital ID that works offline and shows only what you choose.">
    <div class="idcard" aria-label="LifeLink ID card">
      <div class="row between"><span class="label">LifeLink · People of the World</span><span class="chip" style="background:rgba(255,255,255,.15)">{mode.value === "demo" ? "Sample" : "Prototype"}</span></div>
      <div><span class="label">Name</span><div class="name">{v.person.name}</div></div>
      <div class="row" style="gap:28px">
        <div><span class="label">Age</span><div>{age(v.person.birthDate)}</div></div>
        <div><span class="label">District</span><div>{v.person.region}</div></div>
      </div>
      <div><span class="label">LifeLink number</span><div class="num">{v.idNumber}</div></div>
      <span class="small" style="color:#AFC6D9">Issued {c ? fmtDate(c.issued) : ""} by the demonstration issuer</span>
    </div>
    <div class="grid2">
      <button class="btn btn-primary" onClick={() => setSheet("show")}><Icon n="id" />Show my ID code</button>
      <button class="btn" onClick={() => setSheet("scan")}><Icon n="scan" />Check someone's code</button>
    </div>
    <Notice kind="info">Your code proves who you are without phoning home: a shop can see you're over 18 and nothing else. Any phone can check it with no internet. <button class="link" onClick={() => setSheet("hood")}>How it works</button></Notice>
    {mode.value === "own" && <PasskeySetup />}
    <h2>Certificates</h2>
    {v.certificates.length ? <ul class="list card">{v.certificates.map(cert => <li key={cert.issued}><span class="check">✓</span><div class="grow"><strong>{cert.title}</strong><div class="muted small">Signed {fmtDate(cert.issued)} · classical and post-quantum signatures</div></div></li>)}</ul>
      : <p class="muted">Finish a lesson under Learn to earn a signed certificate.</p>}
    {sheet === "show" && c && <ShowCode onClose={() => setSheet("")} />}
    {sheet === "scan" && <Scanner onClose={() => setSheet("")} onText={async t => { setSheet(""); setResult(await verifyPresentation(t.replace(/^LL1:/, ""))); }} />}
    {result && <VerifyResult r={result} onClose={() => setResult(null)} />}
    {sheet === "hood" && <UnderTheHood onClose={() => setSheet("")} />}
  </Page>;
}

function ShowCode({ onClose }: { onClose: () => void }) {
  const v = vault.value!; const c = v.idCredential!;
  const [preset, setPreset] = useState("adult"); const [code, setCode] = useState(""); const [left, setLeft] = useState(300);
  const reveal = PRESETS.find(p => p.id === preset)!.reveal;
  const make = async () => { const k = await holderKey(mode.value === "own"); setCode("LL1:" + await present(c, reveal, k)); setLeft(300); logAccess("You", "Showed your ID code", PRESETS.find(p => p.id === preset)!.label); };
  useEffect(() => { make(); }, [preset]);
  useEffect(() => { const t = setInterval(() => setLeft(l => { if (l <= 1) { make(); return 300; } return l - 1; }), 1000); return () => clearInterval(t); }, [preset]);
  return <Sheet title="Your ID code" onClose={onClose}>
    <div class="seg" role="group" aria-label="What to share">{PRESETS.map(p => <button key={p.id} aria-pressed={preset === p.id} onClick={() => setPreset(p.id)}>{p.label}</button>)}</div>
    {code && <QR text={code} label={`QR code sharing: ${reveal.map(r => LABELS[r]).join(", ")}`} />}
    <p class="small"><strong>Shares:</strong> {reveal.map(r => `${LABELS[r]}: ${show(disclosuresOf(c).find(d => d.name === r)?.value)}`).join(" · ")}</p>
    <p class="small muted">Everything else stays hidden: it can't be read from the code. This code renews in {Math.floor(left / 60)}:{String(left % 60).padStart(2, "0")}, so a photo of it soon stops working.</p>
  </Sheet>;
}

function VerifyResult({ r, onClose }: { r: Verified; onClose: () => void }) {
  return <Sheet title={r.ok ? "Verified" : "Not verified"} onClose={onClose}>
    <Notice kind={r.ok ? "ok" : "danger"}>{r.ok ? "Signed by the issuer, unaltered, and shown from the holder's own device just now." : r.problems.join(" ")}</Notice>
    {Object.keys(r.claims).length > 0 && <table class="table"><tbody>{Object.entries(r.claims).map(([k, val]) => <tr key={k}><th>{LABELS[k] || k}</th><td>{show(val)}</td></tr>)}</tbody></table>}
    {r.holderNumber && <p class="small muted">Holder's device: <span class="mono">{r.holderNumber}</span>{r.ageSeconds !== undefined && ` · shown ${Math.max(0, r.ageSeconds)} seconds ago`}</p>}
    {r.issuerKnown && <DemoNote>Issued by the {DEMO_ISSUER.name}. Its keys are public so anyone can try the prototype, so this proves the technology works, not who someone is.</DemoNote>}
    <p class="small muted">Checked on this device with no internet. Nothing about this check was sent anywhere.</p>
  </Sheet>;
}

function UnderTheHood({ onClose }: { onClose: () => void }) {
  const v = vault.value!; const c = v.idCredential!;
  const pqOk = verifyPq(c);
  return <Sheet title="How your ID works" onClose={onClose}>
    <ol class="stack" style="padding-left:20px;margin:0">
      <li><strong>Each detail is sealed separately.</strong> The issuer signs a fingerprint (a SHA-256 hash) of each detail, not the details themselves. This is the IETF SD-JWT format (RFC 9901).</li>
      <li><strong>You choose what to open.</strong> Your code includes only the details you pick. The rest can't be worked out from it.</li>
      <li><strong>Only your phone can show it.</strong> Your phone holds a private key that can never be copied out of the browser. It signs each code, with the time, so a screenshot or a copy goes stale within minutes.</li>
      <li><strong>Anyone can check it, offline.</strong> A checker needs only the issuer's public key, which the app already has.</li>
      <li><strong>Ready for quantum computers.</strong> Your ID also carries a second signature using ML-DSA (NIST FIPS 204), designed to resist quantum computers. Check on this device: <strong>{pqOk ? "valid ✓" : "not valid"}</strong>.</li>
    </ol>
    <details class="card"><summary>See the raw credential</summary><p class="mono small" style="margin-top:8px">{c.sdjwt}</p></details>
    <p class="small muted">In a pilot, a Poverty Elimination Center issues IDs after an in-person check, using the OpenID4VCI standard, and wallets can present them through the browser's Digital Credentials API (now in Chrome and Safari).</p>
  </Sheet>;
}

function PasskeySetup() {
  const [has, setHas] = useState<boolean | null>(null), [can, setCan] = useState(false), [msg, setMsg] = useState(""), [busy, setBusy] = useState(false);
  const refresh = async () => { setHas(!!(await vaultMeta())?.passkey); setCan(await platformAuthenticator()); };
  useEffect(() => { refresh(); }, []);
  if (has === null) return null;
  return <div class="card"><h3><Icon n="lock" />Fingerprint or face unlock</h3>
    {has ? <><span class="muted">On. Your fingerprint or face never leaves this device's secure hardware; it releases a secret that unlocks your vault. Your PIN still works.</span>
      <button class="btn btn-small" style="align-self:flex-start" onClick={async () => { await removePasskey(); setMsg("Turned off."); refresh(); }}>Turn off</button></>
      : can ? <><span class="muted">Unlock with your fingerprint or face instead of your PIN. The biometric itself is never seen by LifeLink.</span>
        <button class="btn btn-primary btn-small" style="align-self:flex-start" disabled={busy} onClick={async () => { setBusy(true); const r = await addPasskey(vault.value!.person.name); setMsg(r || "Done: you can now unlock with your fingerprint or face."); setBusy(false); refresh(); }}>Set it up</button></>
      : <span class="muted">This device or browser doesn't offer fingerprint or face sign-in to websites. Your PIN keeps your data safe.</span>}
    {msg && <p class="small" role="status">{msg}</p>}
  </div>;
}
