// What a person keeps in LifeLink, and how it is kept.
// "Own" mode: saved on this device in the encrypted vault. "Demo" mode: a sample person, held in memory, never saved.
import { signal, computed } from "@preact/signals";
import type { Credential } from "./credentials";
import type { Entry } from "./ledger";
import type { Reading } from "./ble";
import { saveVault } from "./crypto";

export type Item = { name: string; since?: string; dose?: string; severe?: boolean; date?: string };
export type Health = {
  medicalId: { bloodType: string; notes: string; organDonor: string; showOnLock: boolean };
  conditions: Item[]; medications: Item[]; allergies: Item[]; immunizations: Item[];
  vitals: Reading[];
  checkins: { at: string; mood: number; sleep: number; energy: number; note: string }[];
};
export type Contact = { name: string; phone: string; relation: string };
export type Access = { at: string; who: string; what: string; why: string };
export type Settings = { textSize: number; theme: "auto" | "light" | "dark"; contrast: boolean; reduceMotion: boolean; country: string; autoLockMin: number };
export type Vault = {
  v: 1;
  person: { name: string; birthDate: string; region: string; joined: string };
  idNumber: string;
  idCredential?: Credential;
  certificates: Credential[];
  ledger: Entry[];
  tasks: Record<string, "claimed" | "verified">;
  learning: { goals: string[]; level: string; hours: number; done: Record<string, string>; review: Record<string, { due: string; interval: number; ease: number }>; saved: string[] };
  health: Health;
  safety: { contacts: Contact[]; reports: { at: string; kind: string; text: string; anonymous: boolean }[]; sos: { at: string; outcome: string }[] };
  voice: { votes: Record<string, { choice: string; receipt: string; at: string }>; surveys: Record<string, string> };
  access: Access[];
  consents: Record<string, boolean>;
  settings: Settings;
  location?: { lat: number; lon: number; label: string };
};

export const DEFAULT_SETTINGS: Settings = { textSize: 100, theme: "auto", contrast: false, reduceMotion: false, country: "AU", autoLockMin: 5 };
export function emptyVault(name: string, birthDate: string, region: string, idNumber: string): Vault {
  return {
    v: 1, person: { name, birthDate, region, joined: new Date().toISOString() }, idNumber, certificates: [], ledger: [], tasks: {},
    learning: { goals: [], level: "", hours: 3, done: {}, review: {}, saved: [] },
    health: { medicalId: { bloodType: "", notes: "", organDonor: "", showOnLock: false }, conditions: [], medications: [], allergies: [], immunizations: [], vitals: [], checkins: [] },
    safety: { contacts: [], reports: [], sos: [] }, voice: { votes: {}, surveys: {} }, access: [],
    consents: { "health-in-sos": false, "share-learning-with-pec": false, "research-totals": false }, settings: { ...DEFAULT_SETTINGS }
  };
}

// ---------------------------------------------------------------- the live state
export const mode = signal<"none" | "own" | "demo">("none");
export const vault = signal<Vault | null>(null);
export const unlocked = computed(() => !!vault.value);
export const settings = computed(() => vault.value?.settings ?? DEFAULT_SETTINGS);

let saveTimer: number | undefined;
export const saveState = signal<"saved" | "saving" | "error" | "memory">("saved");
export function update(fn: (v: Vault) => void) {
  const cur = vault.value; if (!cur) return;
  const next: Vault = structuredClone(cur); fn(next); vault.value = next;
  if (mode.value !== "own") { saveState.value = "memory"; return; }
  saveState.value = "saving"; clearTimeout(saveTimer);
  saveTimer = window.setTimeout(() => saveVault(vault.value).then(() => (saveState.value = "saved")).catch(() => (saveState.value = "error")), 250);
}
export async function flush() { clearTimeout(saveTimer); if (mode.value === "own" && vault.value) await saveVault(vault.value); }

// Every time a record is opened, shared or changed by anyone, it is written here, and the person can read it.
export function logAccess(who: string, what: string, why: string) {
  update(v => { v.access.unshift({ at: new Date().toISOString(), who, what, why }); v.access = v.access.slice(0, 300); });
}

// ---------------------------------------------------------------- age helpers
export function age(birthDate: string, on = new Date()): number {
  const b = new Date(birthDate + "T00:00:00"); let a = on.getFullYear() - b.getFullYear();
  if (on.getMonth() < b.getMonth() || (on.getMonth() === b.getMonth() && on.getDate() < b.getDate())) a--;
  return a;
}
