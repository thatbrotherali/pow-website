// Learn: the AI Teacher, starting as an explainable guide. It builds a plan from your goals and always says why.
import { useEffect, useMemo, useRef, useState } from "preact/hooks";
import { vault, update, mode, logAccess } from "../lib/model";
import { append } from "../lib/ledger";
import { holderKey, publicJwk, issue } from "../lib/credentials";
import { GOALS, SOURCES, STAGES, type Source } from "../data/learning";
import { LESSONS, type Lesson as L } from "../data/lessons";
import { Icon, Notice, Page, go } from "../ui/ui";

const host = (u: string) => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch { return u; } };
function SourceCard({ s, why }: { s: Source; why?: string }) {
  const saved = vault.value!.learning.saved.includes(s.id);
  return <div class="card">
    <div class="row between" style="align-items:flex-start"><div><strong>{s.name}</strong><div class="muted small">{s.by}</div></div>
      <button class="btn btn-small btn-ghost" aria-pressed={saved} onClick={() => update(v => { v.learning.saved = saved ? v.learning.saved.filter(x => x !== s.id) : [...v.learning.saved, s.id]; })}>{saved ? "Saved ✓" : "Save"}</button></div>
    <span>{s.free}</span>
    <span class="small muted"><strong>Certificate:</strong> {s.certificate} · <strong>Languages:</strong> {s.languages}{s.offline ? <> · <strong>Offline:</strong> {s.offline}</> : null}</span>
    {why && <span class="small" style="color:var(--info)">Why this: {why}</span>}
    <a class="btn btn-small" style="align-self:flex-start" href={s.url} target="_blank" rel="noopener">Open {host(s.url)} ↗</a>
  </div>;
}

export function Learn() {
  const v = vault.value!; const l = v.learning;
  const plan = useMemo(() => GOALS.filter(g => l.goals.includes(g.id)), [l.goals]);
  const due = Object.values(l.review).filter(r => new Date(r.due) <= new Date()).length;
  const [stage, setStage] = useState(STAGES[0].id);
  return <Page eyebrow="Learn" title="Learning for life" sub="From first letters to a university degree, free. A guide builds your plan and always tells you why.">
    <div class="card accent">
      <h2 style="font-size:1.2rem">What would you like to do?</h2>
      <div class="row" role="group" aria-label="Your goals">{GOALS.map(g => <button key={g.id} class="btn btn-small" aria-pressed={l.goals.includes(g.id)} style={l.goals.includes(g.id) ? "background:var(--accent);color:var(--accent-ink);border-color:var(--accent)" : ""}
        onClick={() => update(x => { x.learning.goals = l.goals.includes(g.id) ? l.goals.filter(y => y !== g.id) : [...l.goals, g.id]; })}>{g.label}</button>)}</div>
      <label class="field" style="max-width:280px">Time you can give each week
        <select value={l.hours} onChange={e => update(x => { x.learning.hours = Number((e.target as HTMLSelectElement).value); })}>{[1, 2, 4, 6, 10].map(n => <option key={n} value={n}>{n} hour{n > 1 ? "s" : ""}</option>)}</select></label>
    </div>
    {plan.length > 0 && <section class="stack" aria-labelledby="plan-h">
      <h2 id="plan-h">Your plan</h2>
      <p class="muted">With {l.hours} hour{l.hours > 1 ? "s" : ""} a week, start with “{plan[0].label}”. {plan[0].why} The guide doesn't decide for you: change your goals and the plan changes, and every suggestion says why it's there.</p>
      {plan.map(g => <div class="stack" key={g.id} style="gap:10px"><h3>{g.label}</h3>
        {g.lessons.map(id => { const les = LESSONS.find(x => x.id === id)!; return <a class="card" href={`#/learn/lesson/${id}`} key={id}><div class="row between"><strong>{les.title}</strong>{l.done[id] ? <span class="pill pill-ok">Done</span> : <span class="pill">{les.minutes} min{les.credits ? ` · +${les.credits} credits` : ""}</span>}</div><span class="muted small">Built-in lesson, works offline. Why: it's the quickest first step for this goal.</span></a>; })}
        <div class="grid2">{g.sources.slice(0, l.hours >= 6 ? 4 : 2).map(id => <SourceCard key={id} s={SOURCES.find(s => s.id === id)!} why={g.why} />)}</div>
      </div>)}
    </section>}
    {due > 0 && <a class="card" href="#/learn/review"><strong>{due} question{due > 1 ? "s" : ""} ready to review</strong><span class="muted small">Questions you missed come back at growing intervals, the way memory works best.</span></a>}

    <h2>Lessons on this device</h2>
    <div class="grid2">{LESSONS.map(les => <a class="card" href={`#/learn/lesson/${les.id}`} key={les.id}><span class="eyebrow">{les.stage}</span><strong>{les.title}</strong>
      <span class="muted small">{les.minutes} minutes{les.credits ? ` · +${les.credits} credits` : ""}{l.done[les.id] ? " · Done ✓" : ""}</span></a>)}</div>

    <h2>The learning map</h2>
    <div class="seg" role="group" aria-label="Stage">{STAGES.map(s => <button key={s.id} aria-pressed={stage === s.id} onClick={() => setStage(s.id)}>{s.title}</button>)}</div>
    <p class="muted">{STAGES.find(s => s.id === stage)!.blurb}</p>
    <div class="grid2">{SOURCES.filter(s => s.stages.includes(stage)).map(s => <SourceCard key={s.id} s={s} />)}</div>
    <p class="small muted">Checked October 2026. Coursera's free audit ended in August 2025, and edX audit access is now time-limited, so they are marked as they are.</p>
    <BookSearch />
    <Tutor />
  </Page>;
}

// Live search of free books (Open Library) when online. If the service can't be reached, it says so and offers the website.
function BookSearch() {
  const [q, setQ] = useState(""), [rows, setRows] = useState<{ key: string; title: string; author: string; year?: number; read: boolean }[] | null>(null), [err, setErr] = useState("");
  const run = async (e: Event) => {
    e.preventDefault(); if (!q.trim()) return; setErr(""); setRows(null);
    try {
      const r = await fetch(`https://openlibrary.org/search.json?q=${encodeURIComponent(q)}&fields=key,title,author_name,first_publish_year,ebook_access&limit=8`);
      const j = await r.json();
      setRows((j.docs || []).map((d: { key: string; title: string; author_name?: string[]; first_publish_year?: number; ebook_access?: string }) => ({ key: d.key, title: d.title, author: (d.author_name || []).slice(0, 2).join(", "), year: d.first_publish_year, read: d.ebook_access === "public" })));
    } catch { setErr("Open Library can't be reached from here right now."); }
  };
  return <details class="card"><summary>Find a free book</summary>
    <form class="row" style="margin-top:10px" onSubmit={run}><input class="input" style="flex:1;min-width:180px" value={q} onInput={e => setQ((e.target as HTMLInputElement).value)} placeholder="A subject, title or author" aria-label="Search for a book" /><button class="btn">Search</button></form>
    {err && <Notice kind="warn">{err} <a href={`https://openlibrary.org/search?q=${encodeURIComponent(q)}`} target="_blank" rel="noopener">Search on openlibrary.org ↗</a></Notice>}
    {rows && (rows.length ? <ul class="list">{rows.map(b => <li key={b.key}><div class="grow"><a href={`https://openlibrary.org${b.key}`} target="_blank" rel="noopener"><strong>{b.title}</strong></a><div class="muted small">{b.author}{b.year ? ` · ${b.year}` : ""}</div></div>{b.read ? <span class="pill pill-ok">Free to read</span> : <span class="pill">Borrow or catalogue</span>}</li>)}</ul> : <p class="muted">No books found.</p>)}
    <p class="small muted">Searches go straight from your device to Open Library (Internet Archive). LifeLink doesn't see or keep them.</p>
  </details>;
}

// On-device AI, only where the browser provides it (currently some desktop Chrome). Nothing leaves the device.
type LM = { create: (o?: object) => Promise<{ prompt: (s: string) => Promise<string> }>; availability?: () => Promise<string> };
function Tutor() {
  const lm = (globalThis as unknown as { LanguageModel?: LM }).LanguageModel;
  const [state, setState] = useState<"checking" | "yes" | "no">("checking"), [q, setQ] = useState(""), [a, setA] = useState(""), [busy, setBusy] = useState(false);
  const session = useRef<{ prompt: (s: string) => Promise<string> } | null>(null);
  useEffect(() => { (async () => { try { setState(lm && (!lm.availability || (await lm.availability()) !== "unavailable") ? "yes" : "no"); } catch { setState("no"); } })(); }, []);
  const ask = async (e: Event) => {
    e.preventDefault(); if (!q.trim() || !lm) return; setBusy(true); setA("");
    try {
      session.current ||= await lm.create({ initialPrompts: [{ role: "system", content: "You are the LifeLink learning guide. Explain simply and kindly, in short paragraphs, for a learner who may have had little schooling. If you are not sure, say so. Never give medical, legal or financial advice: point to a professional." }] });
      setA(await session.current.prompt(q));
    } catch { setA("The on-device model couldn't answer. It may still be downloading."); }
    setBusy(false);
  };
  return <div class="card soft"><h2 style="font-size:1.15rem;display:flex;gap:8px;align-items:center"><Icon n="spark" />Ask the tutor</h2>
    {state === "yes" ? <form class="stack" onSubmit={ask}><input class="input" value={q} onInput={e => setQ((e.target as HTMLInputElement).value)} placeholder="Explain photosynthesis simply" aria-label="Your question" />
      <button class="btn btn-primary" disabled={busy} style="align-self:flex-start">{busy ? "Thinking on your device…" : "Ask"}</button>{a && <p style="white-space:pre-wrap">{a}</p>}
      <p class="small muted">Answered by an AI model running on this computer. Your question never leaves it. AI can be wrong: check important facts.</p></form>
      : <p class="muted">An AI tutor that runs entirely on your device, so your questions stay private. Today's browsers offer this only on some desktop computers (recent Chrome with a powerful graphics card), and not on this one. The pilot app will bring an open, on-device tutor to phones and to the LifeLink Tablet.</p>}
  </div>;
}

// ---------------------------------------------------------------- one lesson: cards, then a short quiz, then a certificate
export function Lesson({ id }: { id: string }) {
  const les = LESSONS.find(x => x.id === id);
  const [i, setI] = useState(0), [answers, setAnswers] = useState<number[]>([]), [finished, setFinished] = useState(false);
  if (!les) return <Page title="Lesson not found" back="/learn"><p>That lesson isn't here.</p></Page>;
  const total = les.cards.length + les.quiz.length;
  const qi = i - les.cards.length, q = qi >= 0 ? les.quiz[qi] : null, picked = q ? answers[qi] : undefined;
  const finish = async () => {
    setFinished(true);
    const right = les.quiz.filter((x, k) => x.answer < 0 || answers[k] === x.answer).length;
    const v = vault.value!; const first = !v.learning.done[les.id];
    const k = await holderKey(mode.value === "own");
    const cert = await issue("certificate", les.title, "https://peopleoftheworld.net/lifelink/vct/certificate", { course: les.title, provider: "LifeLink Learn", completed: new Date().toISOString().slice(0, 10), score: `${right} of ${les.quiz.length}` }, await publicJwk(k));
    const ledger = first && les.credits ? await append(v.ledger, { kind: "earn", amount: les.credits, memo: `Lesson completed: ${les.title}`, party: "LifeLink Learn" }) : v.ledger;
    update(x => {
      x.learning.done[les.id] = new Date().toISOString(); x.ledger = ledger;
      if (first) x.certificates.push(cert);
      les.quiz.forEach((qq, k2) => { if (qq.answer >= 0 && answers[k2] !== qq.answer) x.learning.review[`${les.id}-${k2}`] = { due: new Date(Date.now() + 864e5).toISOString(), interval: 1, ease: 2.3 }; });
    });
    logAccess("LifeLink Learn", "Issued a certificate", les.title);
  };
  return <Page eyebrow={les.stage} title={les.title} back="/learn">
    <div class="bar" role="progressbar" aria-valuemin={0} aria-valuemax={total} aria-valuenow={Math.min(i + 1, total)} aria-label="Lesson progress"><span style={`width:${(Math.min(i + 1, total) / total) * 100}%`} /></div>
    {finished ? <FinishedCard les={les} answers={answers} /> : q ? <div class="card lesson-card" aria-live="polite">
      <span class="eyebrow">Question {qi + 1} of {les.quiz.length}</span><h2>{q.q}</h2>
      <div class="stack" style="gap:8px">{q.options.map((o, k) => <button key={k} class={`btn opt ${picked !== undefined && q.answer >= 0 ? (k === q.answer ? "right" : k === picked ? "wrong" : "") : picked === k ? "right" : ""}`} disabled={picked !== undefined}
        onClick={() => setAnswers(a => { const n = [...a]; n[qi] = k; return n; })}>{o}</button>)}</div>
      {picked !== undefined && <Notice kind={q.answer < 0 || picked === q.answer ? "ok" : "warn"}>{q.answer < 0 ? q.why : picked === q.answer ? `Right. ${q.why}` : `Not quite. ${q.why}`}</Notice>}
    </div> : <div class="card lesson-card" aria-live="polite"><span class="eyebrow">{i + 1} of {les.cards.length}</span><h2>{les.cards[i].h}</h2><p style="font-size:1.1rem">{les.cards[i].p}</p></div>}
    {!finished && <div class="row between">
      <button class="btn" disabled={i === 0} onClick={() => setI(i - 1)}>Back</button>
      {i < total - 1 ? <button class="btn btn-primary" disabled={!!q && picked === undefined} onClick={() => setI(i + 1)}>Next</button>
        : <button class="btn btn-primary" disabled={picked === undefined} onClick={finish}>Finish</button>}
    </div>}
  </Page>;
}
function FinishedCard({ les, answers }: { les: L; answers: number[] }) {
  const right = les.quiz.filter((x, k) => x.answer < 0 || answers[k] === x.answer).length;
  return <div class="card accent lesson-card">
    <span class="eyebrow">Lesson complete</span><h2>{right} of {les.quiz.length}{les.quiz.length && right === les.quiz.length ? ". Well done." : "."}</h2>
    <p>{les.credits ? `+${les.credits} Civic Credits (first time only), and ` : ""}a signed certificate has been added to your Identity.{right < les.quiz.length && les.quiz[0].answer >= 0 ? " The questions you missed will come back for review." : ""}</p>
    {les.more && <a class="btn" style="align-self:flex-start" href={les.more.url} target={les.more.url.startsWith("#") ? undefined : "_blank"} rel="noopener">Go further: {les.more.label}</a>}
    <div class="row"><button class="btn btn-primary" onClick={() => go("/learn")}>Back to Learn</button><a class="btn btn-ghost" href="#/id">See my certificates</a></div>
  </div>;
}

// ---------------------------------------------------------------- spaced review
export function Review() {
  const v = vault.value!;
  const [dueKeys] = useState(() => Object.entries(v.learning.review).filter(([, r]) => new Date(r.due) <= new Date()).map(([k]) => k));   // fixed for this session
  const [idx, setIdx] = useState(0), [picked, setPicked] = useState<number | null>(null);
  if (!dueKeys.length || idx >= dueKeys.length) return <Page title="All caught up" back="/learn"><p class="muted">No questions to review right now. They come back at growing intervals: a day, then three, then a week or more.</p></Page>;
  const key = dueKeys[idx], [lid, qn] = [key.slice(0, key.lastIndexOf("-")), Number(key.slice(key.lastIndexOf("-") + 1))];
  const q = LESSONS.find(x => x.id === lid)?.quiz[qn];
  if (!q) return null;
  const answer = (k: number) => {
    setPicked(k); const ok = k === q.answer;
    update(x => { const r = x.learning.review[key]; if (ok) { r.interval = Math.max(1, Math.round(r.interval * r.ease)); r.ease = Math.min(3, r.ease + 0.1); } else { r.interval = 1; r.ease = Math.max(1.3, r.ease - 0.2); } r.due = new Date(Date.now() + r.interval * 864e5).toISOString(); });
  };
  return <Page eyebrow={`Review ${idx + 1} of ${dueKeys.length}`} title={q.q} back="/learn">
    <div class="stack" style="gap:8px">{q.options.map((o, k) => <button key={k} class={`btn opt ${picked !== null ? (k === q.answer ? "right" : k === picked ? "wrong" : "") : ""}`} disabled={picked !== null} onClick={() => answer(k)}>{o}</button>)}</div>
    {picked !== null && <><Notice kind={picked === q.answer ? "ok" : "warn"}>{q.why}</Notice><button class="btn btn-primary" onClick={() => { setPicked(null); setIdx(idx + 1); }}>Next</button></>}
  </Page>;
}
