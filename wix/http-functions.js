// backend/http-functions.js  (Wix site: shop.peopleoftheworld.net)
//
// Online scores for the brain-training games on peopleoftheworld.net:
// the Decision Game, the Memory Game and the Focus Game, including each game's Daily Challenge.
// Keeps EVERY run, plus each player's best run per board (and, for a Daily Challenge, the first run each day).
//
// Version 3. Existing Decision Game scores are untouched: rows saved before version 3 have no "game"
// field and are read as Decision Game rows, and the boards short / long / infinite work exactly as before.
//
// Collections used (both already exist; the new fields "game" and "day" are added automatically on first save):
//   DecisionGameRuns    every finished run
//   DecisionGameScores  one row per player per board: that player's best run
//                       (for a Daily Challenge: one row per player per board per day, the first run that day)
//
// Endpoints (all under https://shop.peopleoftheworld.net/_functions/decisionGame/...):
//   POST saveScore                                  save a run (body: JSON text)
//   GET  leaderboard?mode=short                     best run per player, ranked (top 100)
//   GET  leaderboard?mode=memory-daily&day=2026-10-29   a Daily Challenge board for one day
//   GET  runs?mode=short&limit=100[&day=...]        latest runs, newest first (all scores)
//   GET  player?id=PLAYER_ID[&game=decision]        one player's bests per board and run history for one game
//   GET  ping                                       health check
//
// Boards ("mode"):
//   Decision Game: short (10), long (20), infinite, daily (10, one a day)
//   Memory Game:   memory-daily (10, one a day), memory-endless (three lives)
//   Focus Game:    focus-daily (30, one a day), focus-endless (three mistakes)
import { ok, badRequest, notFound, serverError } from 'wix-http-functions';
import wixData from 'wix-data';

const RUNS = 'DecisionGameRuns';
const BESTS = 'DecisionGameScores';
const OPTS = { suppressAuth: true };

// questions: a fixed run length (null = open-ended)   maxMistakes: open-ended runs end after this many
// rank: 'fewest' = fewest mistakes, then total time, then average answer
//       'most'   = most correct, then average answer, then total time
const BOARDS = {
  'short':          { game: 'decision', questions: 10, rank: 'fewest' },
  'long':           { game: 'decision', questions: 20, rank: 'fewest' },
  'infinite':       { game: 'decision', questions: null, maxMistakes: 1, rank: 'most' },
  'daily':          { game: 'decision', questions: 10, rank: 'fewest', daily: true },
  'memory-daily':   { game: 'memory', questions: 10, rank: 'most', daily: true },
  'memory-endless': { game: 'memory', questions: null, maxMistakes: 3, rank: 'most' },
  'focus-daily':    { game: 'focus', questions: 30, rank: 'most', daily: true },
  'focus-endless':  { game: 'focus', questions: null, maxMistakes: 3, rank: 'most' }
};

const HEADERS = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};
const VERSION = 3;
const reply = (fn, body) => fn({ headers: HEADERS, body: JSON.stringify(body) });
const gameOf = item => item.game || 'decision';           // rows saved before version 3 are Decision Game rows

function compare(a, b) {
  const board = BOARDS[a.mode] || BOARDS.short;
  if (board.rank === 'most') {
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
const cleanId = s => String(s || '').replace(/[^a-zA-Z0-9-]/g, '').slice(0, 40);
const round3 = n => Math.round(n * 1000) / 1000;

// a Daily Challenge day is the player's local date, so allow from yesterday to tomorrow (UTC) to cover every time zone
function isoDay(offsetDays) {
  const d = new Date(Date.now() + offsetDays * 864e5);
  return d.toISOString().slice(0, 10);
}
function cleanDay(s) {
  const v = String(s || '');
  return /^\d{4}-\d{2}-\d{2}$/.test(v) ? v : '';
}
function dayIsCurrent(day) {
  return day === isoDay(-1) || day === isoDay(0) || day === isoDay(1);
}

function publicRun(item, rank) {
  const out = {
    playerId: item.playerId || '', name: item.name || item.initials || '???', initials: item.initials || '',
    game: gameOf(item), mode: item.mode, correct: item.correct, questions: item.questions,
    totalTime: item.totalTime, avgReaction: item.avgReaction,
    date: item.playedAt || item.bestDate || item.updatedAt || item._createdDate || null
  };
  if (item.day) out.day = item.day;
  if (rank) out.rank = rank;
  return out;
}

// reject impossible runs (a person cannot answer faster than about 0.12 s on average)
function validate(d) {
  const board = BOARDS[d.mode];
  if (!board) return 'Invalid mode';
  if (d.game && d.game !== board.game) return 'Invalid mode';
  for (const k of ['correct', 'questions', 'totalTime', 'avgReaction']) {
    if (typeof d[k] !== 'number' || !isFinite(d[k]) || d[k] < 0) return 'Score fields must be numbers';
  }
  if (!Number.isInteger(d.correct) || !Number.isInteger(d.questions)) return 'Counts must be whole numbers';
  if (d.questions < 1 || d.correct > d.questions) return 'Impossible score';
  if (board.questions && d.questions !== board.questions) return 'Incomplete run';
  if (board.maxMistakes != null && d.questions - d.correct > board.maxMistakes) return 'Impossible score';
  if (d.avgReaction < 0.12 || d.totalTime < d.questions * 0.12 || d.totalTime > 4 * 3600) return 'Implausible time';
  if (board.daily) {
    const day = cleanDay(d.day);
    if (!day) return 'A day is required for the Daily Challenge';
    if (!dayIsCurrent(day)) return 'That Daily Challenge has closed';
  }
  return '';
}

export function options_decisionGame() {
  return reply(ok, { ok: true });
}

export async function post_decisionGame(request) {
  if ((request.path || [])[0] !== 'saveScore') return reply(notFound, { error: 'Unknown endpoint' });
  try {
    const d = JSON.parse((await request.body.text()) || '{}');
    d.mode = String(d.mode || '').toLowerCase();
    const err = validate(d);
    if (err) return reply(badRequest, { error: err });
    const name = cleanName(d.name || d.initials);
    if (!name) return reply(badRequest, { error: 'A name is required' });
    const board = BOARDS[d.mode];
    const playerId = cleanId(d.playerId) || ('initials-' + name.toUpperCase());
    const now = new Date();
    const run = {
      playerId, name, initials: name.slice(0, 3).toUpperCase(), game: board.game, mode: d.mode,
      correct: d.correct, questions: d.questions, totalTime: round3(d.totalTime), avgReaction: round3(d.avgReaction),
      playedAt: now
    };
    if (board.daily) run.day = cleanDay(d.day);
    await wixData.insert(RUNS, run, OPTS);

    let q = wixData.query(BESTS).eq('playerId', playerId).eq('mode', d.mode);
    if (board.daily) q = q.eq('day', run.day);
    const found = await q.limit(1).find(OPTS);
    let best = false, counted = true;
    if (!found.items.length) {
      await wixData.insert(BESTS, { ...run, bestDate: now }, OPTS);
      best = true;
    } else if (board.daily) {
      counted = false;                                     // a Daily Challenge counts only the first run of the day
    } else {
      const cur = found.items[0];
      cur.name = name;                                     // keep the latest spelling of the name
      if (compare(run, cur) < 0) {
        Object.assign(cur, run, { bestDate: now });
        best = true;
      }
      await wixData.update(BESTS, cur, OPTS);
    }
    return reply(ok, { success: true, version: VERSION, best, counted });
  } catch (e) {
    console.error('decisionGame saveScore', e);
    return reply(serverError, { error: 'Internal error' });
  }
}

export async function get_decisionGame(request) {
  const what = (request.path || [])[0] || '';
  const q = request.query || {};
  try {
    if (what === 'ping') return reply(ok, { ok: true, version: VERSION, boards: Object.keys(BOARDS) });

    if (what === 'leaderboard' || what === 'runs') {
      const mode = String(q.mode || 'short').toLowerCase();
      const board = BOARDS[mode];
      if (!board) return reply(badRequest, { error: 'Invalid mode' });
      const day = cleanDay(q.day);
      if (board.daily && what === 'leaderboard' && !day) return reply(badRequest, { error: 'A day is required for the Daily Challenge' });

      if (what === 'leaderboard') {
        let query = wixData.query(BESTS).eq('mode', mode);
        if (board.daily) query = query.eq('day', day);
        const res = await query.limit(1000).find(OPTS);
        const items = res.items.filter(i => i.playerId).sort(compare).slice(0, 100);
        return reply(ok, { mode, day: board.daily ? day : undefined, version: VERSION, results: items.map((i, n) => publicRun(i, n + 1)) });
      }

      const limit = Math.min(Math.max(parseInt(q.limit, 10) || 100, 1), 500);
      let query = wixData.query(RUNS).eq('mode', mode);
      if (board.daily && day) query = query.eq('day', day);
      const res = await query.descending('playedAt').limit(limit).find(OPTS);
      return reply(ok, { mode, version: VERSION, results: res.items.map(i => publicRun(i)) });
    }

    if (what === 'player') {
      const id = cleanId(q.id);
      if (!id) return reply(badRequest, { error: 'Missing player id' });
      const game = String(q.game || 'decision').toLowerCase();
      const [bests, runs] = await Promise.all([
        wixData.query(BESTS).eq('playerId', id).limit(1000).find(OPTS),
        wixData.query(RUNS).eq('playerId', id).descending('playedAt').limit(1000).find(OPTS)
      ]);
      const myBests = bests.items.filter(b => gameOf(b) === game);
      const myRuns = runs.items.filter(r => gameOf(r) === game).slice(0, 500);
      const name = (myRuns[0] || myBests[0] || runs.items[0] || {}).name || '';
      const byMode = {}, dailies = [];
      for (const b of myBests) {
        if (BOARDS[b.mode] && BOARDS[b.mode].daily) dailies.push(publicRun(b));
        else byMode[b.mode] = publicRun(b);
      }
      // rank of each best within its board (Daily Challenges are ranked per day on their own boards)
      for (const mode of Object.keys(byMode)) {
        const all = await wixData.query(BESTS).eq('mode', mode).limit(1000).find(OPTS);
        const sorted = all.items.filter(i => i.playerId).sort(compare);
        byMode[mode].rank = sorted.findIndex(i => i.playerId === id) + 1;
        byMode[mode].players = sorted.length;
      }
      dailies.sort((a, b) => (a.day < b.day ? 1 : -1));
      return reply(ok, { version: VERSION, game, player: { playerId: id, name }, bests: byMode, dailies: dailies.slice(0, 100), runs: myRuns.map(i => publicRun(i)) });
    }

    return reply(notFound, { error: 'Unknown endpoint' });
  } catch (e) {
    console.error('decisionGame get', e);
    return reply(serverError, { error: 'Internal error' });
  }
}
