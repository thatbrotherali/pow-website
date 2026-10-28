// A sample person for exploring LifeLink. Held in memory only; nothing about her is saved.
import { emptyVault, type Vault } from "../lib/model";
import { append, type Entry } from "../lib/ledger";
import { holderKey, publicJwk, lifelinkNumber, issue } from "../lib/credentials";
import { DEMO_PLACE } from "./community";

const daysAgo = (d: number, h = 10) => { const t = new Date(); t.setDate(t.getDate() - d); t.setHours(h, 0, 0, 0); return t.toISOString(); };

export async function demoVault(): Promise<Vault> {
  const k = await holderKey(false), jwk = await publicJwk(k), num = await lifelinkNumber(jwk);
  const v = emptyVault("Amara Mensah", "1991-04-12", "Riverside District", num);
  v.location = { lat: DEMO_PLACE.lat, lon: DEMO_PLACE.lon, label: DEMO_PLACE.label };
  v.idCredential = await issue("id", "LifeLink ID", "https://peopleoftheworld.net/lifelink/vct/id", {
    given_name: "Amara", family_name: "Mensah", birthdate: "1991-04-12", age_over_18: true, age_over_65: false, region: "Riverside District", lifelink_number: num }, jwk);
  v.certificates.push(await issue("certificate", "Spot a scam", "https://peopleoftheworld.net/lifelink/vct/certificate", {
    course: "Spot a scam", provider: "LifeLink Learn", completed: daysAgo(9).slice(0, 10), score: "3 of 3" }, jwk));
  let L: Entry[] = [];
  const rows: [number, Entry["kind"], number, string, string][] = [
    [30, "grant", 50, "Welcome credits", "Riverside PEC"], [26, "earn", 30, "Neighbourhood clean-up", "Riverside PEC"], [24, "spend", 3, "Hot meal", "PEC kitchen"],
    [19, "earn", 40, "Community kitchen shift", "Riverside PEC kitchen"], [15, "spend", 12, "Weekly bus pass", "Riverside Transit"], [12, "earn", 20, "Reading partner", "Riverside Library"],
    [9, "earn", 5, "Lesson completed: Spot a scam", "LifeLink Learn"], [6, "spend", 25, "Fresh-food box", "Riverside Growers"], [3, "earn", 10, "Helped a neighbour join", "LifeLink Ambassadors"], [1, "spend", 3, "Hot meal", "PEC kitchen"]];
  for (const [d, kind, amount, memo, party] of rows) L = await append(L, { kind, amount, memo, party, at: daysAgo(d) });
  v.ledger = L;
  v.tasks = { cleanup: "verified", meals: "verified", tutor: "verified", mentor: "verified" };
  v.learning = { goals: ["job", "digital"], level: "school", hours: 4, done: { scam: daysAgo(9) }, saved: ["fcc", "openlearn"],
    review: { "scam-1": { due: daysAgo(-1), interval: 3, ease: 2.5 } } };
  v.health = {
    medicalId: { bloodType: "O+", notes: "Asthma: reliever inhaler in bag.", organDonor: "Yes", showOnLock: true },
    conditions: [{ name: "Asthma", since: "2004" }], medications: [{ name: "Salbutamol inhaler", dose: "2 puffs as needed" }],
    allergies: [{ name: "Penicillin", severe: true }], immunizations: [{ name: "Influenza", date: daysAgo(40).slice(0, 10) }, { name: "Tetanus booster", date: "2021-06-02" }],
    vitals: [{ kind: "hr", at: daysAgo(6, 8), value: 68, unit: "bpm", source: "Manual" }, { kind: "bp", at: daysAgo(6, 8), value: 118, value2: 76, unit: "mmHg", source: "Manual" },
             { kind: "hr", at: daysAgo(2, 8), value: 64, unit: "bpm", source: "Chest strap" }, { kind: "weight", at: daysAgo(2, 8), value: 67.4, unit: "kg", source: "Manual" }],
    checkins: [5, 4, 3, 4, 4, 5, 4].map((m, i) => ({ at: daysAgo(7 - i, 21), mood: m, sleep: [7, 6.5, 5, 7, 7.5, 8, 7][i], energy: [4, 3, 2, 4, 4, 5, 4][i], note: "" }))
  };
  v.safety.contacts = [{ name: "Kwame Mensah", phone: "0491 570 156", relation: "Brother" }, { name: "Grace Lee", phone: "0491 570 157", relation: "Neighbour" }];
  v.voice.votes = { solar: { choice: "yes", receipt: "8Hc2-k9Qw-T1mZ", at: daysAgo(4) } };
  v.access = [
    { at: daysAgo(1, 12), who: "Amara (you)", what: "Paid 3 credits", why: "Hot meal, PEC kitchen" },
    { at: daysAgo(6, 9), who: "Riverside Health Centre", what: "Viewed your Medical ID", why: "Yearly check-up, with your consent" },
    { at: daysAgo(9, 15), who: "LifeLink Learn", what: "Issued a certificate", why: "Completed: Spot a scam" },
    { at: daysAgo(30, 10), who: "Riverside PEC", what: "Issued your LifeLink ID", why: "Enrolment, in person" }];
  v.consents = { "health-in-sos": true, "share-learning-with-pec": true, "research-totals": true };
  return v;
}
