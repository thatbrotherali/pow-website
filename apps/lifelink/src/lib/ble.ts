// Live readings from Bluetooth health devices, using the standard Bluetooth SIG health profiles.
// Any chest strap, watch, cuff, thermometer, scale or oximeter that speaks these profiles works; no vendor account needed.
// Web Bluetooth runs in Chrome, Edge and Android browsers. Safari on iPhone does not support it (the Phase 2 native app will).

export type Reading = { kind: "hr" | "bp" | "temp" | "weight" | "spo2"; at: string; value: number; value2?: number; pulse?: number; unit: string; source: string };
type Profile = { kind: Reading["kind"]; label: string; service: BluetoothServiceUUID; char: BluetoothCharacteristicUUID; parse: (v: DataView) => Omit<Reading, "kind" | "at" | "source"> | null };

// IEEE-11073 16-bit SFLOAT and 32-bit FLOAT, used by medical device profiles
function sfloat(raw: number): number {
  if ([0x07ff, 0x0800, 0x07fe, 0x0802, 0x0801].includes(raw)) return NaN;
  let m = raw & 0x0fff; if (m >= 0x0800) m -= 0x1000;
  let e = raw >> 12; if (e >= 0x8) e -= 0x10;
  return m * Math.pow(10, e);
}
function float32(v: DataView, o: number): number {
  let m = v.getUint8(o) | (v.getUint8(o + 1) << 8) | (v.getUint8(o + 2) << 16); if (m >= 0x800000) m -= 0x1000000;
  return m * Math.pow(10, v.getInt8(o + 3));
}
const round = (x: number, d = 1) => Math.round(x * 10 ** d) / 10 ** d;

export const PROFILES: Profile[] = [
  { kind: "hr", label: "Heart rate (strap, watch or band)", service: "heart_rate", char: "heart_rate_measurement",
    parse: v => { const f = v.getUint8(0); const hr = f & 1 ? v.getUint16(1, true) : v.getUint8(1); return hr ? { value: hr, unit: "bpm" } : null; } },
  { kind: "bp", label: "Blood pressure cuff", service: "blood_pressure", char: "blood_pressure_measurement",
    parse: v => { const f = v.getUint8(0); const kpa = f & 1; let o = 7; const sys = sfloat(v.getUint16(1, true)), dia = sfloat(v.getUint16(3, true));
      if (f & 2) o += 7; const pulse = f & 4 ? sfloat(v.getUint16(o, true)) : undefined;
      const k = kpa ? 7.50062 : 1; return { value: round(sys * k, 0), value2: round(dia * k, 0), pulse: pulse && !isNaN(pulse) ? round(pulse, 0) : undefined, unit: "mmHg" }; } },
  { kind: "temp", label: "Thermometer", service: "health_thermometer", char: "temperature_measurement",
    parse: v => { const f = v.getUint8(0); let t = float32(v, 1); if (f & 1) t = (t - 32) * 5 / 9; return { value: round(t), unit: "°C" }; } },
  { kind: "weight", label: "Weight scale", service: "weight_scale", char: "weight_measurement",
    parse: v => { const f = v.getUint8(0); const w = v.getUint16(1, true) * (f & 1 ? 0.01 * 0.453592 : 0.005); return w ? { value: round(w), unit: "kg" } : null; } },
  { kind: "spo2", label: "Pulse oximeter", service: 0x1822, char: 0x2a5f,
    parse: v => { const s = sfloat(v.getUint16(1, true)), pr = sfloat(v.getUint16(3, true)); return isNaN(s) ? null : { value: round(s, 0), pulse: isNaN(pr) ? undefined : round(pr, 0), unit: "%" }; } }
];

export const bluetoothAvailable = () => typeof navigator !== "undefined" && "bluetooth" in navigator;

export async function connect(p: Profile, onReading: (r: Reading) => void): Promise<{ name: string; stop: () => void }> {
  const bt = (navigator as Navigator & { bluetooth: Bluetooth }).bluetooth;
  const device = await bt.requestDevice({ filters: [{ services: [p.service] }] });
  const server = await device.gatt!.connect();
  const svc = await server.getPrimaryService(p.service);
  let ch: BluetoothRemoteGATTCharacteristic;
  try { ch = await svc.getCharacteristic(p.char); }
  catch { if (p.kind === "spo2") ch = await svc.getCharacteristic(0x2a5e); else throw new Error("This device doesn't send that reading."); }
  const name = device.name || p.label;
  const handler = (e: Event) => {
    const v = (e.target as BluetoothRemoteGATTCharacteristic).value; if (!v) return;
    try { const r = p.parse(v); if (r) onReading({ ...r, kind: p.kind, at: new Date().toISOString(), source: name }); } catch { /* ignore malformed packets */ }
  };
  ch.addEventListener("characteristicvaluechanged", handler);
  await ch.startNotifications();
  return { name, stop: () => { ch.removeEventListener("characteristicvaluechanged", handler); ch.stopNotifications().catch(() => {}); device.gatt?.disconnect(); } };
}
