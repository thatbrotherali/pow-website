// Starting, unlocking, locking and erasing.
import { effect } from "@preact/signals";
import { db } from "./db";
import { createVault, unlockWithPin, unlockWithPasskey, loadVault, lock, hasVault, saveVault } from "./crypto";
import { holderKey, publicJwk, lifelinkNumber, issue, forgetHolderKey } from "./credentials";
import { append } from "./ledger";
import { mode, vault, emptyVault, flush, type Vault } from "./model";
import { demoVault } from "../data/demo";

export const vaultExists = hasVault;

export async function startDemo() { vault.value = await demoVault(); mode.value = "demo"; }

export async function createOwn(name: string, birthDate: string, region: string, pin: string) {
  await createVault(pin);
  const k = await holderKey(true), jwk = await publicJwk(k), num = await lifelinkNumber(jwk);
  const v = emptyVault(name.trim(), birthDate, region.trim(), num);
  const [given, ...rest] = name.trim().split(/\s+/);
  const today = new Date(), b = new Date(birthDate + "T00:00:00");
  const ageNow = today.getFullYear() - b.getFullYear() - (today < new Date(today.getFullYear(), b.getMonth(), b.getDate()) ? 1 : 0);
  v.idCredential = await issue("id", "LifeLink ID", "https://peopleoftheworld.net/lifelink/vct/id",
    { given_name: given, family_name: rest.join(" "), birthdate: birthDate, age_over_18: ageNow >= 18, age_over_65: ageNow >= 65, region: region.trim(), lifelink_number: num }, jwk);
  v.ledger = await append([], { kind: "grant", amount: 50, memo: "Welcome credits (demonstration)", party: "LifeLink demonstration" });
  v.access.unshift({ at: new Date().toISOString(), who: "You", what: "Created your LifeLink", why: "Set up on this device" });
  await saveVault(v);
  vault.value = v; mode.value = "own";
}

export async function unlock(pin: string): Promise<boolean> {
  if (!(await unlockWithPin(pin))) return false;
  return open();
}
export async function unlockPasskey(): Promise<string | null> {
  const r = await unlockWithPasskey(); if (r) return r;
  await open(); return null;
}
async function open(): Promise<boolean> {
  const v = await loadVault<Vault>(); if (!v) return false;
  await holderKey(true);
  vault.value = v; mode.value = "own"; return true;
}

export async function lockNow() {
  if (mode.value === "own") await flush();
  lock(); forgetHolderKey(); vault.value = null; mode.value = "none";
}
export async function eraseEverything() {
  lock(); forgetHolderKey(); vault.value = null; mode.value = "none";
  await db.wipe();   // the app itself stays cached for offline use; every piece of personal data is gone
}

// The emergency Medical ID can be shown on the lock screen, if the person chooses. Only then is that small part kept unencrypted.
effect(() => {
  const v = vault.value;
  if (mode.value !== "own" || !v) return;
  const m = v.health.medicalId;
  if (m.showOnLock) db.set("lock-medical-id", { name: v.person.name, birthDate: v.person.birthDate, bloodType: m.bloodType, notes: m.notes, organDonor: m.organDonor,
    allergies: v.health.allergies, conditions: v.health.conditions, medications: v.health.medications, contacts: v.safety.contacts.slice(0, 3) });
  else db.del("lock-medical-id");
});

// Lock automatically after a few minutes without use.
let idle: number | undefined;
export function watchIdle() {
  const reset = () => {
    clearTimeout(idle);
    const v = vault.value; if (mode.value !== "own" || !v) return;
    idle = window.setTimeout(() => { lockNow(); }, Math.max(1, v.settings.autoLockMin) * 60000);
  };
  ["pointerdown", "keydown", "scroll", "visibilitychange"].forEach(e => addEventListener(e, reset, { passive: true }));
  effect(() => { void vault.value; reset(); });
}
