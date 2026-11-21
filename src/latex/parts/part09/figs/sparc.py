"""Read the SPARC tables (Lelli, McGaugh & Schombert 2016) and build the radial acceleration relation
as McGaugh, Lelli & Schombert (2016) did: disc M/L 0.5, bulge 0.7, quality 1-2, inclination >= 30 deg,
velocity errors under 10 per cent."""
import numpy as np
from pathlib import Path
D = Path(__file__).parent / "data"
KPC = 3.0857e19

def table1():
    gal = {}
    for line in (D / "SPARC_Lelli2016c.mrt").read_text().splitlines():
        f = line.split()
        if len(f) < 18: continue
        try:
            T = int(f[1]); vals = [float(x) for x in f[2:17]]; Q = int(f[17])
        except ValueError:
            continue
        Dm, eD, fD, inc, einc, L, eL, Reff, SBeff, Rdisk, SBdisk, MHI, RHI, Vf, eVf = vals
        gal[f[0]] = dict(T=T, D=Dm, inc=inc, L=L * 1e9, MHI=MHI * 1e9, Vflat=Vf, eVflat=eVf, Q=Q)
    return gal

def massmodels():
    rows = []
    for line in (D / "MassModels_Lelli2016c.mrt").read_text().splitlines():
        if len(line) < 59: continue
        try:
            r = (line[0:11].strip(),) + tuple(float(line[a:b]) for a, b in [(12, 18), (19, 25), (26, 32), (33, 38), (39, 45), (46, 52), (53, 59)])
        except ValueError:
            continue
        rows.append(r)
    return rows

def rar(yd=0.5, yb=0.7):
    gal = table1(); out = []
    for name, Dm, R, V, eV, Vg, Vd, Vb in massmodels():
        g = gal[name]
        if g["Q"] >= 3 or g["inc"] < 30 or V <= 0 or eV / V >= 0.1 or R <= 0: continue
        gobs = (V * 1e3) ** 2 / (R * KPC)
        vb2 = Vg * abs(Vg) + yd * Vd ** 2 + yb * Vb ** 2
        if vb2 <= 0: continue
        out.append((name, vb2 * 1e6 / (R * KPC), gobs))
    return out

def fit_a0(gb, go):
    best = None
    for a0 in np.linspace(0.6e-10, 2.0e-10, 1401):
        pred = gb / (1 - np.exp(-np.sqrt(gb / a0)))
        res = np.log10(go) - np.log10(pred); s = np.sum(res ** 2)
        if best is None or s < best[0]: best = (s, a0, res)
    return best[1], best[2]

if __name__ == "__main__":
    gal = table1(); mm = massmodels()
    print("galaxies in table 1:", len(gal), " rows in mass models:", len(mm), " galaxies:", len({r[0] for r in mm}))
    d = rar(); gb = np.array([x[1] for x in d]); go = np.array([x[2] for x in d])
    print("RAR points:", len(d), " galaxies:", len({x[0] for x in d}))
    a0, res = fit_a0(gb, go)
    print(f"best a0 = {a0:.3e} m/s^2; rms scatter = {res.std():.3f} dex; mean = {res.mean():+.3f}")
    for n in ("NGC3198", "M33", "UGC02885"):
        print(n, gal.get(n))
