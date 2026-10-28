// Two techniques that let a community be counted without anyone being tracked.

// 1. Area alerts: an alert is sent to everyone with the shape of the affected area.
//    Each device checks for itself whether it is inside. The person's location goes nowhere.
export type Pt = [number, number];   // [latitude, longitude]
export function inside(p: Pt, poly: Pt[]): boolean {
  let hit = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [yi, xi] = poly[i], [yj, xj] = poly[j];
    if ((yi > p[0]) !== (yj > p[0]) && p[1] < ((xj - xi) * (p[0] - yi)) / (yj - yi) + xi) hit = !hit;
  }
  return hit;
}
export function km(a: Pt, b: Pt): number {
  const R = 6371, r = Math.PI / 180, dLat = (b[0] - a[0]) * r, dLon = (b[1] - a[1]) * r;
  const s = Math.sin(dLat / 2) ** 2 + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}

// 2. Randomised response (local differential privacy).
//    The device flips a coin. Heads: it sends the true answer. Tails: it flips again and sends that instead.
//    Any single answer could be chance, so no one can know what one person said,
//    yet across many people the true total can be recovered: true rate = 2 × (yes rate) − ½.
export function randomise(truth: boolean, r = Math.random): { sent: boolean; honest: boolean } {
  if (r() < 0.5) return { sent: truth, honest: true };
  return { sent: r() < 0.5, honest: false };
}
export const estimate = (yes: number, total: number) => Math.min(1, Math.max(0, 2 * (yes / total) - 0.5));
export function simulate(people: number, trueRate: number, r = Math.random) {
  let yes = 0, actual = 0;
  for (let i = 0; i < people; i++) { const t = r() < trueRate; if (t) actual++; if (randomise(t, r).sent) yes++; }
  return { yes, actual, estimate: Math.round(estimate(yes, people) * people) };
}
