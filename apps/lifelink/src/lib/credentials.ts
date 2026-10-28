// Digital identity and certificates as selectively disclosable credentials, in the IETF SD-JWT format (RFC 9901).
//   - The issuer signs digests of each claim, not the claims themselves.
//   - The holder reveals only the claims they choose (for example "over 18", without a birth date).
//   - A key-binding signature from the holder's own device key proves the presentation came from the holder's phone.
//   - Any device can verify the whole thing offline, with only the issuer's public key.
// Credentials also carry a second, post-quantum signature (ML-DSA-44, NIST FIPS 204) kept in the wallet.
import { ml_dsa44 } from "@noble/post-quantum/ml-dsa.js";
import { b64u, unb64u, utf8, fromUtf8, rand, sha256, hex } from "./crypto";
import { DEMO_ISSUER } from "../data/demo-issuer";
import { db } from "./db";

const ES256 = { name: "ECDSA", namedCurve: "P-256" } as const;
const SIG = { name: "ECDSA", hash: "SHA-256" } as const;

export type Jwk = { kty: string; crv: string; x: string; y: string };
export type Credential = {
  kind: "id" | "certificate";
  title: string;
  issued: string;
  sdjwt: string;                 // issuer-signed JWT ~ every disclosure ~
  claims: Record<string, unknown>;
  pq?: { alg: "ML-DSA-44"; sig: string };
};

// ---------------------------------------------------------------- the holder's device key
// Generated on the device and marked non-extractable: it can sign, but it can never be copied out of the browser.
let holder: CryptoKeyPair | null = null;
export async function holderKey(persist: boolean): Promise<CryptoKeyPair> {
  if (holder) return holder;
  if (persist) { const k = await db.get<CryptoKeyPair>("holder-key"); if (k) return (holder = k); }
  holder = await crypto.subtle.generateKey(ES256, false, ["sign", "verify"]) as CryptoKeyPair;
  if (persist) await db.set("holder-key", holder);
  return holder;
}
export const forgetHolderKey = () => { holder = null; };
export async function publicJwk(k: CryptoKeyPair): Promise<Jwk> {
  const j = await crypto.subtle.exportKey("jwk", k.publicKey) as JsonWebKey;
  return { kty: "EC", crv: "P-256", x: j.x!, y: j.y! };
}
// RFC 7638 thumbprint, shown as a short LifeLink number
export async function thumbprint(j: Jwk): Promise<string> {
  return b64u(await sha256(JSON.stringify({ crv: j.crv, kty: j.kty, x: j.x, y: j.y })));
}
export async function lifelinkNumber(j: Jwk): Promise<string> {
  const h = hex((await sha256(JSON.stringify({ crv: j.crv, kty: j.kty, x: j.x, y: j.y }))).slice(0, 6)).toUpperCase();
  return `LL-${h.slice(0, 4)}-${h.slice(4, 8)}-${h.slice(8, 12)}`;
}

// ---------------------------------------------------------------- JWS helpers
async function signJws(header: object, payload: object, key: CryptoKey): Promise<string> {
  const input = `${b64u(utf8(JSON.stringify(header)))}.${b64u(utf8(JSON.stringify(payload)))}`;
  const sig = await crypto.subtle.sign(SIG, key, utf8(input) as BufferSource);   // Web Crypto gives r||s, exactly the JWS format
  return `${input}.${b64u(sig)}`;
}
async function verifyJws(jws: string, jwk: Jwk): Promise<{ header: any; payload: any } | null> {
  const [h, p, s] = jws.split("."); if (!h || !p || !s) return null;
  try {
    const key = await crypto.subtle.importKey("jwk", { ...jwk, ext: true } as JsonWebKey, ES256, false, ["verify"]);
    const ok = await crypto.subtle.verify(SIG, key, unb64u(s) as BufferSource, utf8(`${h}.${p}`) as BufferSource);
    return ok ? { header: JSON.parse(fromUtf8(unb64u(h))), payload: JSON.parse(fromUtf8(unb64u(p))) } : null;
  } catch { return null; }
}
const issuerKey = () => crypto.subtle.importKey("jwk", { ...DEMO_ISSUER.privateJwk, ext: true } as JsonWebKey, ES256, false, ["sign"]);
let pqKeys: { publicKey: Uint8Array; secretKey: Uint8Array } | null = null;
const pq = () => (pqKeys ||= ml_dsa44.keygen(Uint8Array.from(DEMO_ISSUER.pqSeedHex.match(/../g)!.map(x => parseInt(x, 16)))));

// ---------------------------------------------------------------- issuing (by the demonstration issuer)
const digestOf = async (disclosure: string) => b64u(await sha256(disclosure));
export async function issue(kind: Credential["kind"], title: string, vct: string, claims: Record<string, unknown>, holderJwk: Jwk, days = 365 * 5): Promise<Credential> {
  const disclosures: string[] = [];
  for (const [k, v] of Object.entries(claims)) disclosures.push(b64u(utf8(JSON.stringify([b64u(rand(16)), k, v]))));
  const digests = (await Promise.all(disclosures.map(digestOf))).sort();      // sorted so their order reveals nothing
  const now = Math.floor(Date.now() / 1000);
  const payload = { iss: DEMO_ISSUER.iss, iat: now, exp: now + days * 86400, vct, _sd: digests, _sd_alg: "sha-256", cnf: { jwk: holderJwk } };
  const jwt = await signJws({ alg: "ES256", typ: "dc+sd-jwt", kid: DEMO_ISSUER.kid }, payload, await issuerKey());
  const pqSig = ml_dsa44.sign(utf8(jwt.split(".").slice(0, 2).join(".")), pq().secretKey);
  return { kind, title, issued: new Date().toISOString(), sdjwt: `${jwt}~${disclosures.join("~")}~`, claims, pq: { alg: "ML-DSA-44", sig: b64u(pqSig) } };
}
export function verifyPq(c: Credential): boolean {
  if (!c.pq) return false;
  const jwt = c.sdjwt.split("~")[0];
  try { return ml_dsa44.verify(unb64u(c.pq.sig), utf8(jwt.split(".").slice(0, 2).join(".")), pq().publicKey); } catch { return false; }
}

// ---------------------------------------------------------------- presenting (by the holder)
export function disclosuresOf(c: Credential): { name: string; value: unknown; raw: string }[] {
  return c.sdjwt.split("~").slice(1).filter(Boolean).map(raw => { const [, name, value] = JSON.parse(fromUtf8(unb64u(raw))); return { name, value, raw }; });
}
export async function present(c: Credential, reveal: string[], k: CryptoKeyPair, aud = "in-person"): Promise<string> {
  const jwt = c.sdjwt.split("~")[0];
  const chosen = disclosuresOf(c).filter(d => reveal.includes(d.name)).map(d => d.raw);
  const body = `${jwt}~${chosen.join("~")}${chosen.length ? "~" : ""}`;
  const kb = await signJws({ alg: "ES256", typ: "kb+jwt" }, { iat: Math.floor(Date.now() / 1000), aud, nonce: b64u(rand(12)), sd_hash: b64u(await sha256(body)) }, k.privateKey);
  return body + kb;
}

// ---------------------------------------------------------------- verifying (by anyone, offline)
export type Verified = { ok: boolean; problems: string[]; issuerKnown: boolean; claims: Record<string, unknown>; vct?: string; holderNumber?: string; ageSeconds?: number; expires?: number };
export async function verifyPresentation(text: string, maxAgeSeconds = 300): Promise<Verified> {
  const out: Verified = { ok: false, problems: [], issuerKnown: false, claims: {} };
  const parts = text.split("~");
  if (parts.length < 2) { out.problems.push("This isn't a LifeLink credential."); return out; }
  const jwt = parts[0], kb = parts[parts.length - 1], discl = parts.slice(1, -1).filter(Boolean);
  const issued = await verifyJws(jwt, DEMO_ISSUER.publicJwk);
  if (!issued) { out.problems.push("The issuer's signature doesn't match a known issuer."); return out; }
  out.issuerKnown = true; out.vct = issued.payload.vct; out.expires = issued.payload.exp;
  const now = Math.floor(Date.now() / 1000);
  if (issued.payload.exp && issued.payload.exp < now) out.problems.push("The credential has expired.");
  const sd: string[] = issued.payload._sd || [];
  for (const d of discl) {
    if (!sd.includes(await digestOf(d))) { out.problems.push("A shown detail was not signed by the issuer."); continue; }
    const [, name, value] = JSON.parse(fromUtf8(unb64u(d))); out.claims[name] = value;
  }
  const holderJwk = issued.payload.cnf?.jwk as Jwk | undefined;
  if (!holderJwk) out.problems.push("The credential isn't bound to a device.");
  else {
    out.holderNumber = await lifelinkNumber(holderJwk);
    const proof = kb ? await verifyJws(kb, holderJwk) : null;
    if (!proof) out.problems.push("It wasn't presented from the holder's own device.");
    else {
      const body = parts.slice(0, -1).join("~") + "~";
      if (proof.payload.sd_hash !== b64u(await sha256(body))) out.problems.push("The presentation was altered.");
      out.ageSeconds = now - proof.payload.iat;
      if (out.ageSeconds > maxAgeSeconds) out.problems.push(`The code is ${Math.round(out.ageSeconds / 60)} minutes old: ask for a fresh one.`);
      if (out.ageSeconds < -60) out.problems.push("The code's time is in the future: check both devices' clocks.");
    }
  }
  out.ok = out.problems.length === 0;
  return out;
}

// ---------------------------------------------------------------- signed payments (Civic Credits, demonstration)
export type Payment = { v: 1; from: string; fromName: string; to: string; amount: number; memo: string; nonce: string; iat: number };
export async function signPayment(p: Omit<Payment, "v" | "nonce" | "iat">, k: CryptoKeyPair): Promise<string> {
  const jwk = await publicJwk(k);
  return signJws({ alg: "ES256", typ: "ll-pay", jwk }, { v: 1, nonce: b64u(rand(9)), iat: Math.floor(Date.now() / 1000), ...p }, k.privateKey);
}
export async function verifyPayment(jws: string): Promise<{ ok: boolean; payment?: Payment; problem?: string }> {
  try {
    const header = JSON.parse(fromUtf8(unb64u(jws.split(".")[0])));
    if (header.typ !== "ll-pay" || !header.jwk) return { ok: false, problem: "This isn't a LifeLink payment." };
    const r = await verifyJws(jws, header.jwk); if (!r) return { ok: false, problem: "The payment's signature is not valid." };
    if (r.payload.from !== await lifelinkNumber(header.jwk)) return { ok: false, problem: "The payment was signed by a different device than it claims." };
    return { ok: true, payment: r.payload as Payment };
  } catch { return { ok: false, problem: "This isn't a LifeLink payment." }; }
}
