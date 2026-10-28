// A tamper-evident ledger: each entry carries the hash of the one before it, so changing any past entry
// breaks every link after it. This is the core idea behind a blockchain, without the energy cost.
import { sha256, b64u } from "./crypto";

export type Entry = { n: number; at: string; kind: "earn" | "spend" | "receive" | "pay" | "grant"; amount: number; memo: string; party: string; prev: string; hash: string; proof?: string };

const body = (e: Omit<Entry, "hash">) => JSON.stringify([e.n, e.at, e.kind, e.amount, e.memo, e.party, e.prev, e.proof || ""]);
export async function append(chain: Entry[], e: Omit<Entry, "n" | "prev" | "hash" | "at"> & { at?: string }): Promise<Entry[]> {
  const prev = chain.length ? chain[chain.length - 1].hash : "genesis";
  const draft = { n: chain.length + 1, at: e.at || new Date().toISOString(), kind: e.kind, amount: e.amount, memo: e.memo, party: e.party, prev, proof: e.proof };
  const hash = b64u(await sha256(body(draft))).slice(0, 22);
  return [...chain, { ...draft, hash }];
}
export async function verifyChain(chain: Entry[]): Promise<{ ok: boolean; brokenAt?: number }> {
  let prev = "genesis";
  for (const e of chain) {
    if (e.prev !== prev) return { ok: false, brokenAt: e.n };
    const { hash, ...rest } = e;
    if (b64u(await sha256(body(rest))).slice(0, 22) !== hash) return { ok: false, brokenAt: e.n };
    prev = hash;
  }
  return { ok: true };
}
export const balance = (chain: Entry[]) => chain.reduce((s, e) => s + (e.kind === "spend" || e.kind === "pay" ? -e.amount : e.amount), 0);
