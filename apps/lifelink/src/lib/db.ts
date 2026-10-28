// A tiny key-value store on IndexedDB. Everything LifeLink keeps lives here, on this device only.
const NAME = "lifelink-prototype";
const STORE = "kv";

let dbp: Promise<IDBDatabase> | null = null;
function open(): Promise<IDBDatabase> {
  if (dbp) return dbp;
  dbp = new Promise((resolve, reject) => {
    const req = indexedDB.open(NAME, 1);
    req.onupgradeneeded = () => req.result.createObjectStore(STORE);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return dbp;
}

function tx<T>(mode: IDBTransactionMode, fn: (s: IDBObjectStore) => IDBRequest<T>): Promise<T> {
  return open().then(db => new Promise<T>((resolve, reject) => {
    const t = db.transaction(STORE, mode);
    const r = fn(t.objectStore(STORE));
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error);
  }));
}

export const db = {
  get: <T = unknown>(k: string) => tx<T | undefined>("readonly", s => s.get(k) as IDBRequest<T | undefined>),
  set: (k: string, v: unknown) => tx("readwrite", s => s.put(v, k)).then(() => undefined),
  del: (k: string) => tx("readwrite", s => s.delete(k)).then(() => undefined),
  keys: () => tx<IDBValidKey[]>("readonly", s => s.getAllKeys()),
  async wipe() {
    const d = await open(); d.close(); dbp = null;
    await new Promise<void>((res, rej) => { const r = indexedDB.deleteDatabase(NAME); r.onsuccess = () => res(); r.onerror = () => rej(r.error); r.onblocked = () => res(); });
  }
};
