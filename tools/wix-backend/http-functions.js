// backend/http-functions.js  (Wix site: shop.peopleoftheworld.net)
//
// Online scores for the Decision Game on peopleoftheworld.net.
// Keeps EVERY run, plus each player's best run per mode.
//
// Collections used (create both in the Wix CMS; fields are added automatically on first save):
//   DecisionGameRuns    every finished run
//   DecisionGameScores  one row per player per mode: that player's best run
//
// Endpoints (all under https://shop.peopleoftheworld.net/_functions/decisionGame/...):
//   POST saveScore                     save a run (body: JSON text)
//   GET  leaderboard?mode=short        best run per player, ranked (top 100)
//   GET  runs?mode=short&limit=100     latest runs, newest first (all scores)
//   GET  player?id=PLAYER_ID           one player's bests per mode and run history
//   GET  ping                          health check
import { ok, badRequest, notFound, serverError } from 'wix-http-functions';
import wixData from 'wix-data';

const RUNS = 'DecisionGameRuns';
const BESTS = 'DecisionGameScores';
const MODES = { short: 10, long: 20, infinite: null };
const OPTS = { suppressAuth: true };
const HEADERS = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};
const reply = (fn, body) => fn({ headers: HEADERS, body: JSON.stringify(body) });

// ranking: short/long = fewest mistakes, then total time, then average reaction
//          infinite   = most correct, then average reaction, then total time
function compare(a, b) {
  if (a.mode === 'infinite') {
    if (a.correct !== b.correct) return b.correct - a.correct;
    if (a.avgReaction !== b.avgReaction) return a.avgReaction - b.avgReaction;
    return a.totalTime - b.totalTime;
  }
  const am = a.questions - a.correct, bm = b.questions - b.correct;
  if (am !== bm) return am - bm;
  if (a.totalTime !== b.totalTime) return a.totalTime - b.totalTime;
  return a.avgReaction - b.avgReaction;
}

function cleanName(s) {
  return String(s || '').replace(/[<>"'`\\]/g, '').replace(/\s+/g, ' ').trim().slice(0, 16);
}
const round3 = n => Math.round(n * 1000) / 1000;

function publicRun(item, rank) {
  const out = {
    playerId: item.playerId || '', name: item.name || item.initials || '???', initials: item.initials || '',
    mode: item.mode, correct: item.correct, questions: item.questions,
    totalTime: item.totalTime, avgReaction: item.avgReaction,
    date: item.playedAt || item.bestDate || item.updatedAt || item._createdDate || null
  };
  if (rank) out.rank = rank;
  return out;
}

// reject impossible runs (a person cannot answer faster than about 0.12 s on average)
function validate(d) {
  if (!(d.mode in MODES)) return 'Invalid mode';
  for (const k of ['correct', 'questions', 'totalTime', 'avgReaction']) {
    if (typeof d[k] !== 'number' || !isFinite(d[k]) || d[k] < 0) return 'Score fields must be numbers';
  }
  if (!Number.isInteger(d.correct) || !Number.isInteger(d.questions)) return 'Counts must be whole numbers';
  if (d.questions < 1 || d.correct > d.questions) return 'Impossible score';
  const fixed = MODES[d.mode];
  if (fixed && d.questions !== fixed) return 'Incomplete run';
  if (d.mode === 'infinite' && d.questions - d.correct > 1) return 'Impossible score';
  if (d.avgReaction < 0.12 || d.totalTime < d.questions * 0.12 || d.totalTime > 4 * 3600) return 'Implausible time';
  return '';
}

export function options_decisionGame() {
  return reply(ok, { ok: true });
}

export async function post_decisionGame(request) {
  if ((request.path || [])[0] !== 'saveScore') return reply(notFound, { error: 'Unknown endpoint' });
  try {
    const d = JSON.parse((await request.body.text()) || '{}');
    const err = validate(d);
    if (err) return reply(badRequest, { error: err });
    const name = cleanName(d.name || d.initials);
    if (!name) return reply(badRequest, { error: 'A name is required' });
    const playerId = String(d.playerId || '').replace(/[^a-zA-Z0-9-]/g, '').slice(0, 40) || ('initials-' + name.toUpperCase());
    const now = new Date();
    const run = {
      playerId, name, initials: name.slice(0, 3).toUpperCase(), mode: d.mode,
      correct: d.correct, questions: d.questions, totalTime: round3(d.totalTime), avgReaction: round3(d.avgReaction),
      playedAt: now
    };
    await wixData.insert(RUNS, run, OPTS);

    const found = await wixData.query(BESTS).eq('playerId', playerId).eq('mode', d.mode).limit(1).find(OPTS);
    let best = false;
    if (!found.items.length) {
      await wixData.insert(BESTS, { ...run, bestDate: now }, OPTS);
      best = true;
    } else {
      const cur = found.items[0];
      cur.name = name; // keep the latest spelling of the name
      if (compare(run, cur) < 0) {
        Object.assign(cur, run, { bestDate: now });
        best = true;
      }
      await wixData.update(BESTS, cur, OPTS);
    }
    return reply(ok, { success: true, version: 2, best });
  } catch (e) {
    console.error('decisionGame saveScore', e);
    return reply(serverError, { error: 'Internal error' });
  }
}

export async function get_decisionGame(request) {
  const what = (request.path || [])[0] || '';
  const q = request.query || {};
  try {
    if (what === 'ping') return reply(ok, { ok: true, version: 2 });

    if (what === 'leaderboard') {
      const mode = String(q.mode || 'short').toLowerCase();
      if (!(mode in MODES)) return reply(badRequest, { error: 'Invalid mode' });
      const res = await wixData.query(BESTS).eq('mode', mode).limit(1000).find(OPTS);
      const items = res.items.filter(i => i.playerId).sort(compare).slice(0, 100);
      return reply(ok, { mode, version: 2, results: items.map((i, n) => publicRun(i, n + 1)) });
    }

    if (what === 'runs') {
      const mode = String(q.mode || 'short').toLowerCase();
      if (!(mode in MODES)) return reply(badRequest, { error: 'Invalid mode' });
      const limit = Math.min(Math.max(parseInt(q.limit, 10) || 100, 1), 500);
      const res = await wixData.query(RUNS).eq('mode', mode).descending('playedAt').limit(limit).find(OPTS);
      return reply(ok, { mode, version: 2, results: res.items.map(i => publicRun(i)) });
    }

    if (what === 'player') {
      const id = String(q.id || '').replace(/[^a-zA-Z0-9-]/g, '').slice(0, 40);
      if (!id) return reply(badRequest, { error: 'Missing player id' });
      const [bests, runs] = await Promise.all([
        wixData.query(BESTS).eq('playerId', id).limit(10).find(OPTS),
        wixData.query(RUNS).eq('playerId', id).descending('playedAt').limit(500).find(OPTS)
      ]);
      const name = (runs.items[0] || bests.items[0] || {}).name || '';
      const byMode = {};
      for (const b of bests.items) byMode[b.mode] = publicRun(b);
      // rank of each best within its mode
      for (const mode of Object.keys(byMode)) {
        const all = await wixData.query(BESTS).eq('mode', mode).limit(1000).find(OPTS);
        const sorted = all.items.filter(i => i.playerId).sort(compare);
        byMode[mode].rank = sorted.findIndex(i => i.playerId === id) + 1;
        byMode[mode].players = sorted.length;
      }
      return reply(ok, { version: 2, player: { playerId: id, name }, bests: byMode, runs: runs.items.map(i => publicRun(i)) });
    }

    return reply(notFound, { error: 'Unknown endpoint' });
  } catch (e) {
    console.error('decisionGame get', e);
    return reply(serverError, { error: 'Internal error' });
  }
}
