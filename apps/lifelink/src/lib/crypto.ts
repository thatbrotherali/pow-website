// The vault: everything a person keeps in LifeLink is encrypted on their device.
//   Data key (DEK): a random AES-256-GCM key that encrypts the vault.
//   The DEK is stored only "wrapped" (encrypted) by keys derived from the person's unlock methods:
//     - their PIN, stretched with Argon2id (the OWASP-recommended password hash), and/or
//     - a passkey (fingerprint / face) using the WebAuthn PRF extension, where the browser offers it.
//   The biometric itself never leaves the phone's secure hardware; the app only receives a secret derived by it.
import { argon2id } from "hash-wasm";
import { db } from "./db";

const enc = new TextEncoder(), dec = new TextDecoder();
export const utf8 = (s: string) => enc.encode(s);
export const fromUtf8 = (b: ArrayBuffer | Uint8Array) => dec.decode(b);

export function b64u(bytes: ArrayBuffer | Uint8Array): string {
  const b = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes);
  let s = ""; for (let i = 0; i < b.length; i += 0x8000) s += String.fromCharCode(...b.subarray(i, i + 0x8000));
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
export function unb64u(s: string): Uint8Array {
  const t = s.replace(/-/g, "+").replace(/_/g, "/"); const p = t + "===".slice((t.length + 3) % 4);
  const bin = atob(p); const out = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i); return out;
}
export const rand = (n: number) => crypto.getRandomValues(new Uint8Array(n));
export async function sha256(data: Uint8Array | string): Promise<Uint8Array> {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", typeof data === "string" ? utf8(data) : (data as BufferSource)));
}
export const hex = (b: Uint8Array) => Array.from(b, x => x.toString(16).padStart(2, "0")).join("");

// ---------------------------------------------------------------- AES-GCM helpers
type Box = { iv: string; ct: string };
async function seal(key: CryptoKey, plain: Uint8Array): Promise<Box> {
  const iv = rand(12);
  const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, plain as BufferSource);
  return { iv: b64u(iv), ct: b64u(ct) };
}
async function open(key: CryptoKey, box: Box): Promise<Uint8Array> {
  return new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: unb64u(box.iv) as BufferSource }, key, unb64u(box.ct) as BufferSource));
}
const aesKey = (raw: Uint8Array, usages: KeyUsage[]) => crypto.subtle.importKey("raw", raw as BufferSource, "AES-GCM", false, usages);

// ---------------------------------------------------------------- key derivation
export const ARGON = { memorySize: 19456, iterations: 2, parallelism: 1 };   // OWASP minimum for Argon2id: 19 MiB, 2 passes
async function pinKey(pin: string, salt: Uint8Array): Promise<CryptoKey> {
  const raw = await argon2id({ password: pin, salt, hashLength: 32, outputType: "binary", ...ARGON });
  return aesKey(raw, ["encrypt", "decrypt"]);
}
async function prfKey(secret: ArrayBuffer): Promise<CryptoKey> {
  const base = await crypto.subtle.importKey("raw", secret, "HKDF", false, ["deriveKey"]);
  return crypto.subtle.deriveKey({ name: "HKDF", hash: "SHA-256", salt: utf8("LifeLink vault") as BufferSource, info: utf8("passkey unlock") as BufferSource },
    base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
}

// ---------------------------------------------------------------- the vault
export type VaultMeta = {
  v: 1; created: string; salt: string; argon: typeof ARGON; pin: Box;
  passkey?: { id: string; prfSalt: string; wrap: Box };
};
let dataKey: CryptoKey | null = null;
let rawDek: Uint8Array | null = null;          // kept only while unlocked, to add or remove unlock methods

export const isUnlocked = () => !!dataKey;
export const hasVault = async () => !!(await db.get<VaultMeta>("vault-meta"));
export const vaultMeta = () => db.get<VaultMeta>("vault-meta");

export async function createVault(pin: string): Promise<void> {
  const dek = rand(32), salt = rand(16);
  const meta: VaultMeta = { v: 1, created: new Date().toISOString(), salt: b64u(salt), argon: ARGON, pin: await seal(await pinKey(pin, salt), dek) };
  await db.set("vault-meta", meta);
  rawDek = dek; dataKey = await aesKey(dek, ["encrypt", "decrypt"]);
}
export async function unlockWithPin(pin: string): Promise<boolean> {
  const meta = await vaultMeta(); if (!meta) return false;
  try { const dek = await open(await pinKey(pin, unb64u(meta.salt)), meta.pin); rawDek = dek; dataKey = await aesKey(dek, ["encrypt", "decrypt"]); return true; }
  catch { return false; }
}
export async function changePin(pin: string) {
  const meta = await vaultMeta(); if (!meta || !rawDek) throw new Error("Locked");
  const salt = rand(16); meta.salt = b64u(salt); meta.pin = await seal(await pinKey(pin, salt), rawDek);
  await db.set("vault-meta", meta);
}
export function lock() { dataKey = null; if (rawDek) rawDek.fill(0); rawDek = null; }

export async function saveVault(obj: unknown) {
  if (!dataKey) throw new Error("Locked");
  await db.set("vault-data", await seal(dataKey, utf8(JSON.stringify(obj))));
}
export async function loadVault<T>(): Promise<T | null> {
  if (!dataKey) throw new Error("Locked");
  const box = await db.get<Box>("vault-data"); if (!box) return null;
  return JSON.parse(fromUtf8(await open(dataKey, box))) as T;
}

// ---------------------------------------------------------------- passkeys (fingerprint / face) with the PRF extension
type PrfResults = { prf?: { enabled?: boolean; results?: { first?: ArrayBuffer } } };
export const passkeysPossible = () => typeof PublicKeyCredential !== "undefined" && !!navigator.credentials;
export async function platformAuthenticator(): Promise<boolean> {
  try { return passkeysPossible() && await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable(); } catch { return false; }
}
async function prfGet(id: Uint8Array, prfSalt: Uint8Array): Promise<ArrayBuffer | null> {
  const cred = await navigator.credentials.get({ publicKey: {
    challenge: rand(32) as BufferSource, allowCredentials: [{ type: "public-key", id: id as BufferSource }], userVerification: "required", timeout: 60000,
    extensions: { prf: { eval: { first: prfSalt as BufferSource } } } as AuthenticationExtensionsClientInputs } }) as PublicKeyCredential | null;
  const r = cred?.getClientExtensionResults() as PrfResults | undefined;
  return r?.prf?.results?.first ?? null;
}
// Returns a reason string on failure, so the app can say plainly why biometric unlock isn't available.
export async function addPasskey(displayName: string): Promise<string | null> {
  if (!rawDek) return "Unlock first.";
  if (!(await platformAuthenticator())) return "This device has no fingerprint or face sign-in the browser can use.";
  const prfSalt = rand(32);
  let cred: PublicKeyCredential | null;
  try {
    cred = await navigator.credentials.create({ publicKey: {
      rp: { name: "LifeLink prototype" }, user: { id: rand(16) as BufferSource, name: "lifelink", displayName: displayName || "LifeLink" },
      challenge: rand(32) as BufferSource, pubKeyCredParams: [{ type: "public-key", alg: -7 }, { type: "public-key", alg: -257 }],
      authenticatorSelection: { authenticatorAttachment: "platform", residentKey: "preferred", userVerification: "required" }, timeout: 60000,
      extensions: { prf: { eval: { first: prfSalt as BufferSource } } } as AuthenticationExtensionsClientInputs } }) as PublicKeyCredential | null;
  } catch (e) { return (e as Error).name === "NotAllowedError" ? "Cancelled." : "The passkey couldn't be created."; }
  if (!cred) return "Cancelled.";
  const r = cred.getClientExtensionResults() as PrfResults;
  if (r.prf && r.prf.enabled === false) return "This browser or password manager can't unlock encrypted data with a passkey (no PRF support). Your PIN still works.";
  let secret = r.prf?.results?.first ?? null;
  const id = new Uint8Array(cred.rawId);
  if (!secret) { try { secret = await prfGet(id, prfSalt); } catch { secret = null; } }
  if (!secret) return "This browser or password manager can't unlock encrypted data with a passkey (no PRF support). Your PIN still works.";
  const meta = await vaultMeta(); if (!meta) return "No vault.";
  meta.passkey = { id: b64u(id), prfSalt: b64u(prfSalt), wrap: await seal(await prfKey(secret), rawDek) };
  await db.set("vault-meta", meta);
  return null;
}
export async function unlockWithPasskey(): Promise<string | null> {
  const meta = await vaultMeta(); if (!meta?.passkey) return "No passkey set up.";
  try {
    const secret = await prfGet(unb64u(meta.passkey.id), unb64u(meta.passkey.prfSalt));
    if (!secret) return "The passkey didn't return its unlock secret. Use your PIN.";
    const dek = await open(await prfKey(secret), meta.passkey.wrap); rawDek = dek; dataKey = await aesKey(dek, ["encrypt", "decrypt"]); return null;
  } catch (e) { return (e as Error).name === "NotAllowedError" ? "Cancelled." : "That didn't work. Use your PIN."; }
}
export async function removePasskey() { const m = await vaultMeta(); if (m) { delete m.passkey; await db.set("vault-meta", m); } }
