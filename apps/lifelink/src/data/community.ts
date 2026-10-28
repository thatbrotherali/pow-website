// The demonstration community: "Riverside District", a made-up place used to show how LifeLink works locally.
// Every proposal, alert, task and price here is illustrative.
import type { Pt } from "../lib/privacy";

export const DEMO_PLACE = { label: "Riverside District (demonstration)", lat: -27.4705, lon: 153.0260 };

export type Task = { id: string; title: string; hours: number; credits: number; who: string; verify: string };
export const TASKS: Task[] = [
  { id: "cleanup", title: "Neighbourhood clean-up, Saturday morning", hours: 3, credits: 30, who: "Riverside PEC", verify: "A PEC coordinator scans your LifeLink code at the end." },
  { id: "tutor", title: "Reading partner for a younger learner", hours: 2, credits: 20, who: "Riverside Library", verify: "The library confirms each session." },
  { id: "meals", title: "Cook and serve at the community kitchen", hours: 4, credits: 40, who: "Riverside PEC kitchen", verify: "The kitchen lead confirms your shift." },
  { id: "checkup", title: "Yearly health check-up", hours: 1, credits: 10, who: "Riverside Health Centre", verify: "The clinic confirms the visit, not what was found." },
  { id: "mentor", title: "Help a neighbour set up LifeLink", hours: 1, credits: 10, who: "LifeLink Ambassadors", verify: "Your neighbour confirms from their own LifeLink." }
];

export type Service = { id: string; title: string; credits: number; note: string };
export const SERVICES: Service[] = [
  { id: "meal", title: "Hot meal, PEC kitchen", credits: 3, note: "True cost plus a fair margin; no profit on necessities." },
  { id: "groceries", title: "Weekly fresh-food box", credits: 25, note: "Grown and packed locally." },
  { id: "bus", title: "Weekly bus pass", credits: 12, note: "Accepted on all Riverside routes." },
  { id: "course", title: "Forklift licence course", credits: 0, note: "Free: training is paid by the PEC, and finishing earns credits." },
  { id: "rent", title: "Rent contribution, community housing", credits: 90, note: "Weekly; the rest is covered by the housing programme." }
];

export type Proposal = { id: string; title: string; summary: string; cost: string; forArgs: string[]; against: string[]; closes: string; results: Record<string, number> };
export const PROPOSALS: Proposal[] = [
  { id: "depot", title: "Turn the empty bus depot into a Poverty Elimination Center",
    summary: "The council owns an empty depot on River Road. This proposal converts it into a centre with a community kitchen, training rooms, a health clinic and 40 short-stay rooms.",
    cost: "About 4.2 million, paid from the sale of a council-owned car park; running costs paid in Civic Credits.",
    forArgs: ["Puts housing, food, training and care under one roof.", "Uses a building that is costing money while empty.", "Creates about 35 local jobs."],
    against: ["Some neighbours worry about traffic on River Road.", "The car park would be sold for good."],
    closes: "2026-11-30", results: { yes: 1284, no: 412, abstain: 97 } },
  { id: "solar", title: "Solar panels and batteries for the community hall",
    summary: "Fit solar panels and a battery to the hall so it can stay open as a cool room in heatwaves and a charging point in blackouts.",
    cost: "About 180,000, repaid by lower power bills in about eight years.",
    forArgs: ["A safe place in heatwaves and power cuts.", "Cuts the hall's power bill and emissions."],
    against: ["The money could fix footpaths sooner."],
    closes: "2026-11-15", results: { yes: 902, no: 233, abstain: 61 } },
  { id: "bus", title: "A night bus to the hospital",
    summary: "Run a bus every hour from 10 pm to 5 am between Riverside and the hospital, for shift workers, patients and visitors.",
    cost: "About 310,000 a year, from the state transport budget.",
    forArgs: ["Night-shift nurses and cleaners have no way home.", "Fewer people driving tired."],
    against: ["Few riders after 1 am in a three-month trial elsewhere."],
    closes: "2026-12-10", results: { yes: 640, no: 388, abstain: 120 } }
];

export type Alert = { id: string; kind: string; title: string; detail: string; issued: string; by: string; area: Pt[] };
export const ALERTS: Alert[] = [
  { id: "water", kind: "Health", title: "Boil water notice", detail: "A water main is being repaired. Boil drinking water for one minute until Friday.", issued: "Riverside Water", by: "Riverside Water",
    area: [[-27.462, 153.015], [-27.462, 153.036], [-27.479, 153.036], [-27.479, 153.015]] },
  { id: "flood", kind: "Weather", title: "Minor flood warning: river flats", detail: "Low-lying parks and the riverside path may flood at high tide tonight.", issued: "Bureau of Meteorology (demo)", by: "Weather service",
    area: [[-27.474, 153.028], [-27.474, 153.045], [-27.490, 153.045], [-27.490, 153.028]] },
  { id: "fire", kind: "Fire", title: "Bushfire watch: North Ridge", detail: "A grass fire is under control. Keep windows closed if you smell smoke.", issued: "Fire service (demo)", by: "Fire service",
    area: [[-27.400, 152.990], [-27.400, 153.020], [-27.420, 153.020], [-27.420, 152.990]] }
];

export type Survey = { id: string; question: string; planners: string; trueRate: number };
export const SURVEYS: Survey[] = [
  { id: "housing", question: "Are you worried about keeping a roof over your head in the next six months?", planners: "how many homes and rent contributions the PEC should plan for", trueRate: 0.18 },
  { id: "food", question: "In the past month, did you skip meals because there wasn't enough money for food?", planners: "how many meals the community kitchen should prepare", trueRate: 0.12 },
  { id: "training", question: "Would you start a training course if it were free and earned Civic Credits?", planners: "how many training places to open", trueRate: 0.41 }
];
