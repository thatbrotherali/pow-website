// Today: the day at a glance, from "A day with LifeLink" in LifeLink Daily Implementation.
import { vault, update, mode } from "../lib/model";
import { balance } from "../lib/ledger";
import { inside } from "../lib/privacy";
import { ALERTS } from "../data/community";
import { LESSONS } from "../data/lessons";
import { DemoNote, Icon, Page } from "../ui/ui";

export function Today() {
  const v = vault.value!; const h = new Date().getHours();
  const first = v.person.name.split(" ")[0];
  const greet = h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening";
  const bal = balance(v.ledger);
  const next = LESSONS.find(l => !v.learning.done[l.id] && l.id !== "within") || LESSONS[0];
  const due = Object.values(v.learning.review).filter(r => new Date(r.due) <= new Date()).length;
  const todayKey = new Date().toDateString();
  const checkedIn = v.health.checkins.some(c => new Date(c.at).toDateString() === todayKey);
  const here = v.location ? ALERTS.filter(a => inside([v.location!.lat, v.location!.lon], a.area)) : [];
  const quick = (mood: number) => update(x => { x.health.checkins.push({ at: new Date().toISOString(), mood, sleep: 0, energy: 0, note: "" }); });

  return <Page eyebrow={new Date().toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" })} title={`${greet}, ${first}`}>
    {mode.value === "demo" && <DemoNote>You're exploring as Amara, a sample person. Try anything: nothing is saved, and nothing is sent anywhere.</DemoNote>}
    <div class="grid2">
      <a class="card accent" href="#/wallet"><span class="eyebrow">Civic Credits</span><span class="big">{bal}</span><span class="muted">credits available. <span style="color:var(--info)">Earn or spend →</span></span></a>
      <a class="card" href={due ? "#/learn/review" : `#/learn/lesson/${next.id}`}><span class="eyebrow">Learn</span>
        <h3>{due ? `${due} question${due > 1 ? "s" : ""} to review` : next.title}</h3>
        <span class="muted">{due ? "A quick review keeps what you've learned." : `${next.minutes} minutes · ${next.stage}`}</span></a>
      <div class="card"><span class="eyebrow">How are you today?</span>
        {checkedIn ? <span class="muted">Checked in today. <a href="#/health/checkin">See your week</a>.</span> :
          <div class="row" role="group" aria-label="How are you feeling?">{["😞", "🙁", "😐", "🙂", "😄"].map((e, i) =>
            <button class="btn btn-small" key={i} onClick={() => quick(i + 1)} aria-label={["Very low", "Low", "Okay", "Good", "Very good"][i]}><span aria-hidden="true" style="font-size:1.3rem">{e}</span></button>)}</div>}
      </div>
      <a class="card" href="#/safety"><span class="eyebrow">Your area</span>
        <h3>{here.length ? `${here.length} alert${here.length > 1 ? "s" : ""} where you are` : "No alerts where you are"}</h3>
        <span class="muted">{here[0] ? here[0].title + "." : "Checked on this device; your location went nowhere."}</span></a>
    </div>
    {h >= 18 || h < 4 ? <div class="card soft"><span class="eyebrow">Evening reflection</span>
      <p style="font-family:var(--display);font-size:1.25rem">What was the kindest thing you did today, and what would you do differently tomorrow?</p>
      <span class="muted small">A quiet minute with the voice within. <a href="#/learn/lesson/within">Why this matters</a></span></div> : null}
    <h2>Everything in one place</h2>
    <div class="grid3">
      {[["id", "Identity", "#/id", "Show or check an ID, offline"], ["learn", "Learn", "#/learn", "From first letters to university"], ["health", "Health", "#/health", "Medical ID, records, care"],
        ["safety", "Safety", "#/safety", "SOS, alerts, reporting"], ["voice", "Your say", "#/voice", "Proposals and votes"], ["data", "My data", "#/data", "See, export, erase"]].map(([i, t, href, d]) =>
        <a class="card" href={href} key={href}><Icon n={i} size={26} /><strong>{t}</strong><span class="muted small">{d}</span></a>)}
    </div>
  </Page>;
}
