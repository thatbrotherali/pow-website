// Wallet: Civic Credits (demonstration). Earn by serving the community, spend on essentials, pay people by QR, even offline.
import { useState } from "preact/hooks";
import { vault, update, mode, logAccess } from "../lib/model";
import { append, balance, verifyChain, type Entry } from "../lib/ledger";
import { holderKey, signPayment, verifyPayment } from "../lib/credentials";
import { TASKS, SERVICES } from "../data/community";
import { DemoNote, Field, Icon, Notice, Page, QR, Scanner, Sheet, fmtDate } from "../ui/ui";

export function Wallet() {
  const v = vault.value!; const bal = balance(v.ledger);
  const [sheet, setSheet] = useState<"" | "pay" | "scan" | "check">("");
  const [msg, setMsg] = useState<{ kind: "ok" | "danger"; text: string } | null>(null);
  const record = async (e: Omit<Entry, "n" | "prev" | "hash" | "at">) => { const next = await append(vault.value!.ledger, e); update(x => { x.ledger = next; }); };
  const spend = async (id: string) => {
    const s = SERVICES.find(x => x.id === id)!;
    if (s.credits > bal) return setMsg({ kind: "danger", text: `You need ${s.credits} credits for that. Under the plan, no one is refused essentials: a PEC worker can always step in.` });
    await record({ kind: "spend", amount: s.credits, memo: s.title, party: "Riverside PEC" }); logAccess("You", `Spent ${s.credits} credits`, s.title);
    setMsg({ kind: "ok", text: `Paid ${s.credits} credits for: ${s.title}.` });
  };
  const verifyTask = async (id: string) => {
    const t = TASKS.find(x => x.id === id)!;
    await record({ kind: "earn", amount: t.credits, memo: t.title, party: t.who });
    update(x => { x.tasks[id] = "verified"; }); logAccess(t.who, "Confirmed your service", t.title);
    setMsg({ kind: "ok", text: `${t.who} confirmed your service. ${t.credits} credits added.` });
  };
  const receive = async (text: string) => {
    setSheet(""); const r = await verifyPayment(text.replace(/^LLPAY:/, ""));
    if (!r.ok || !r.payment) return setMsg({ kind: "danger", text: r.problem || "That code isn't a payment." });
    const p = r.payment;
    if (p.from === vault.value!.idNumber) return setMsg({ kind: "danger", text: "That's your own payment code. The person you paid scans it on their phone." });
    if (vault.value!.ledger.some(e => e.proof === p.nonce)) return setMsg({ kind: "danger", text: "This payment has already been received." });
    await record({ kind: "receive", amount: p.amount, memo: p.memo || "Payment", party: `${p.fromName} (${p.from})`, proof: p.nonce });
    logAccess(p.fromName, `Paid you ${p.amount} credits`, p.memo || "Payment");
    setMsg({ kind: "ok", text: `Received ${p.amount} credits from ${p.fromName}. The signature checks out.` });
  };

  return <Page eyebrow="Wallet" title="Civic Credits" sub="Earned by serving your community; spent on the essentials of life.">
    <DemoNote>These are demonstration credits with no value. In a pilot, credits are issued by the participating council and backed by income from public resources.</DemoNote>
    <div class="hero"><span class="eyebrow" style="color:var(--band-muted)">Balance</span><span class="big" style="font-size:3rem">{bal}</span><span class="muted">credits</span>
      <div class="row"><button class="btn btn-primary" onClick={() => setSheet("pay")}>Pay someone</button><button class="btn" onClick={() => setSheet("scan")}><Icon n="scan" />Receive a payment</button></div></div>
    {msg && <Notice kind={msg.kind}>{msg.text}</Notice>}

    <h2>Earn credits</h2>
    <ul class="list card">{TASKS.map(t => { const st = v.tasks[t.id]; return <li key={t.id}>
      <div class="grow"><strong>{t.title}</strong><div class="muted small">{t.hours} h · {t.who} · {t.verify}</div></div>
      {st === "verified" ? <span class="pill pill-ok">Done</span> : st === "claimed" ?
        <button class="btn btn-small" onClick={() => verifyTask(t.id)} title="In a pilot the coordinator scans your code">Simulate confirmation</button> :
        <button class="btn btn-small btn-primary" onClick={() => { update(x => { x.tasks[t.id] = "claimed"; }); setMsg({ kind: "ok", text: `Signed up. After your ${t.title.toLowerCase()}, ${t.who} confirms it and ${t.credits} credits arrive.` }); }}>+{t.credits}</button>}
    </li>; })}</ul>

    <h2>Spend at the centre</h2>
    <ul class="list card">{SERVICES.map(s => <li key={s.id}><div class="grow"><strong>{s.title}</strong><div class="muted small">{s.note}</div></div>
      {s.credits ? <button class="btn btn-small" onClick={() => spend(s.id)}>{s.credits} credits</button> : <span class="pill pill-ok">Free</span>}</li>)}</ul>

    <div class="row between"><h2>History</h2><button class="btn btn-small" onClick={() => setSheet("check")}><Icon n="check" size={18} />Check the ledger</button></div>
    <ul class="list card">{[...v.ledger].reverse().map(e => <li key={e.hash}>
      <div class="grow"><strong>{e.memo}</strong><div class="muted small">{e.party} · {fmtDate(e.at)}</div></div>
      <span class={`amount ${e.kind === "spend" || e.kind === "pay" ? "minus" : "plus"}`}>{e.kind === "spend" || e.kind === "pay" ? "−" : "+"}{e.amount}</span></li>)}</ul>

    <details class="card"><summary>Where do credits come from?</summary>
      <p class="muted" style="margin-top:8px">In the Plan to End Poverty, Civic Credits pay for service to the community, from nursing and teaching to volunteering. The money that backs them comes from what the public owns together: the sale or licensing of public resources, and income from public works and utilities. Every payment is signed and every ledger can be checked, so people can see where public money goes. <a href="https://peopleoftheworld.net/plan-to-end-poverty/civic-credits/">Read the plan</a>.</p></details>

    {sheet === "pay" && <Pay onClose={() => setSheet("")} onPaid={async (amt, memo, to) => { await record({ kind: "pay", amount: amt, memo, party: to }); logAccess("You", `Paid ${amt} credits`, memo); }} max={bal} />}
    {sheet === "scan" && <Scanner onClose={() => setSheet("")} onText={receive} />}
    {sheet === "check" && <CheckLedger onClose={() => setSheet("")} />}
  </Page>;
}

function Pay({ onClose, onPaid, max }: { onClose: () => void; onPaid: (a: number, memo: string, to: string) => Promise<void>; max: number }) {
  const [amount, setAmount] = useState(""), [memo, setMemo] = useState(""), [to, setTo] = useState(""), [code, setCode] = useState(""), [err, setErr] = useState("");
  const make = async () => {
    const a = Math.round(Number(amount)); setErr("");
    if (!a || a < 1) return setErr("Enter an amount."); if (a > max) return setErr(`You have ${max} credits.`);
    const k = await holderKey(mode.value === "own"); const v = vault.value!;
    setCode("LLPAY:" + await signPayment({ from: v.idNumber, fromName: v.person.name.split(" ")[0], to: to || "anyone", amount: a, memo }, k));
    await onPaid(a, memo || "Payment", to || "Paid by QR");
  };
  return <Sheet title="Pay someone" onClose={onClose}>
    {!code ? <>
      <Field label="Amount (credits)" inputMode="numeric" value={amount} onInput={x => setAmount(x.replace(/\D/g, ""))} />
      <Field label="Who is it for?" hint="Optional: a name, to help you remember." value={to} onInput={setTo} />
      <Field label="What for?" value={memo} onInput={setMemo} placeholder="Garden help" />
      {err && <Notice kind="danger">{err}</Notice>}
      <button class="btn btn-primary" onClick={make}>Create payment code</button>
      <p class="small muted">The payment is signed by your phone's private key. The other person scans it under "Receive a payment", and their phone checks your signature, with no internet needed.</p>
    </> : <>
      <QR text={code} label="Signed payment QR code" />
      <Notice kind="ok">Paid {amount} credits. Ask the other person to scan this code.</Notice>
      <p class="small muted">Offline payments are settled when either phone next connects, which is how double-spending is caught. In this prototype a code can be received once per wallet.</p>
    </>}
  </Sheet>;
}

function CheckLedger({ onClose }: { onClose: () => void }) {
  const [res, setRes] = useState<string>(""), [tamper, setTamper] = useState("");
  const run = async () => { const r = await verifyChain(vault.value!.ledger); setRes(r.ok ? `All ${vault.value!.ledger.length} entries are intact: every link in the chain matches.` : `Broken at entry ${r.brokenAt}.`); };
  const tryTamper = async () => {
    const copy = structuredClone(vault.value!.ledger); if (copy.length < 2) return;
    const i = Math.floor(copy.length / 2); copy[i].amount += 100;
    const r = await verifyChain(copy); setTamper(`We secretly added 100 credits to entry ${copy[i].n} in a copy of your ledger. The check caught it at entry ${r.brokenAt}: the change breaks the seal on that entry and every one after it.`);
  };
  return <Sheet title="Check the ledger" onClose={onClose}>
    <p class="muted">Each entry carries a seal made from its own contents and the seal of the entry before it. Change any past entry and the seals stop matching.</p>
    <button class="btn btn-primary" onClick={run}>Check my ledger</button>{res && <Notice kind={res.startsWith("All") ? "ok" : "danger"}>{res}</Notice>}
    <button class="btn" onClick={tryTamper}>Try tampering with a copy</button>{tamper && <Notice kind="warn">{tamper}</Notice>}
  </Sheet>;
}
