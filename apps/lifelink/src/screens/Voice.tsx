// Your say: local proposals in plain language, votes with a receipt, and needs surveys that count without tracking.
import { useState } from "preact/hooks";
import { vault, update, logAccess } from "../lib/model";
import { b64u, rand, sha256 } from "../lib/crypto";
import { randomise, simulate, estimate } from "../lib/privacy";
import { PROPOSALS, SURVEYS, type Proposal } from "../data/community";
import { DemoNote, Notice, Page, fmtDate } from "../ui/ui";

export function Voice() {
  return <Page eyebrow="Your say" title="Decisions near you" sub="Read what's proposed, in plain words, and have your say.">
    <DemoNote>Proposals and results are for the demonstration district. Votes stay on this device.</DemoNote>
    {PROPOSALS.map(p => <ProposalCard key={p.id} p={p} />)}
    <h2>Help plan what your area needs</h2>
    <p class="muted">Planners need to know how many people need housing, food or training, but not who. These surveys use randomised response: your phone sometimes answers at random, so no single answer can be traced to you, yet across everyone the true total can be worked out.</p>
    {SURVEYS.map(s => <SurveyCard key={s.id} id={s.id} />)}
  </Page>;
}

function ProposalCard({ p }: { p: Proposal }) {
  const mine = vault.value!.voice.votes[p.id];
  const results = { ...p.results }; if (mine) results[mine.choice] = (results[mine.choice] || 0) + 1;
  const total = Object.values(results).reduce((a, b) => a + b, 0);
  const vote = async (choice: string) => {
    const salt = b64u(rand(12)), digest = b64u(await sha256(`${p.id}|${choice}|${salt}`));
    const receipt = `${digest.slice(0, 4)}-${digest.slice(4, 8)}-${digest.slice(8, 12)}`;
    update(x => { x.voice.votes[p.id] = { choice, receipt, at: new Date().toISOString() }; });
    logAccess("You", "Voted", p.title);
  };
  return <article class="card"><span class="eyebrow">Closes {fmtDate(p.closes)}</span><h3>{p.title}</h3><p>{p.summary}</p><p class="small"><strong>Cost:</strong> {p.cost}</p>
    <div class="grid2"><div><strong class="small">For</strong><ul class="small" style="margin:4px 0;padding-left:18px">{p.forArgs.map(a => <li key={a}>{a}</li>)}</ul></div>
      <div><strong class="small">Against</strong><ul class="small" style="margin:4px 0;padding-left:18px">{p.against.map(a => <li key={a}>{a}</li>)}</ul></div></div>
    {mine ? <><Notice kind="ok">You voted <strong>{mine.choice}</strong>. Receipt <span class="mono">{mine.receipt}</span>. In a pilot, the receipt lets you check your vote was counted, while no one else can tell how you voted.</Notice>
      {(["yes", "no", "abstain"] as const).map(k => <div key={k} class="stack" style="gap:2px"><div class="row between small"><span style="text-transform:capitalize">{k}</span><span>{Math.round((results[k] / total) * 100)}% · {results[k].toLocaleString()}</span></div><div class="bar"><span style={`width:${(results[k] / total) * 100}%`} /></div></div>)}</>
      : <div class="row">{["yes", "no", "abstain"].map(k => <button key={k} class={`btn ${k === "yes" ? "btn-primary" : ""}`} onClick={() => vote(k)} style="text-transform:capitalize">{k}</button>)}</div>}
  </article>;
}

function SurveyCard({ id }: { id: string }) {
  const s = SURVEYS.find(x => x.id === id)!; const answered = vault.value!.voice.surveys[id];
  const [sent, setSent] = useState<{ sent: boolean; honest: boolean } | null>(null), [sim, setSim] = useState<ReturnType<typeof simulate> | null>(null);
  const answer = (truth: boolean) => { const r = randomise(truth); setSent(r); update(x => { x.voice.surveys[id] = r.sent ? "yes" : "no"; }); logAccess("You", "Answered a needs survey", "Randomised: your true answer wasn't kept"); };
  return <div class="card"><strong>{s.question}</strong>
    {answered ? <Notice kind="ok">Answered. {sent ? (sent.honest ? "This time your phone sent your true answer" : "This time your phone sent a random answer") : "Your phone may have sent your answer or a random one"}, and it didn't keep your real answer. Planners will use the totals to work out {s.planners}.</Notice>
      : <div class="row"><button class="btn" onClick={() => answer(true)}>Yes</button><button class="btn" onClick={() => answer(false)}>No</button></div>}
    <button class="link small" style="align-self:flex-start" onClick={() => setSim(simulate(1000, s.trueRate))}>See how planners still get the right total</button>
    {sim && <p class="small">Simulated 1,000 neighbours. Truly yes: <strong>{sim.actual}</strong>. "Yes" received, including random answers: {sim.yes}. Planners' estimate (2 × {(sim.yes / 1000).toFixed(3)} − 0.5 = {estimate(sim.yes, 1000).toFixed(3)}): <strong>{sim.estimate}</strong>. Close to the truth, and no single answer can be trusted to be real.</p>}
  </div>;
}
