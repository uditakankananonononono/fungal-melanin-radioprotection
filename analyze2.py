#!/usr/bin/env python3
"""MEL-SHIELD-2 gate computation Q6 (proton stopping power) + descriptives.

Implements PREREG2.md exactly against data/star/*.tsv (sha256 in
data/manifest_star.json). Bragg additivity: compound S/rho = sum(w_i S_i),
with w_i elemental mass fractions. No fitted parameters.
"""
import json, math, bisect, pathlib

D = pathlib.Path("data/star")
OUT = pathlib.Path("results"); OUT.mkdir(exist_ok=True)

def load(prog, name):
    rows = []
    for line in (D / f"{prog}_{name}.tsv").read_text().splitlines()[1:]:
        e, se, sn, st = (float(v) for v in line.split("\t"))
        rows.append((e, st))  # total mass stopping power MeV cm2/g
    return rows

def interp(rows, e):
    es = [r[0] for r in rows]
    if e <= es[0]: return rows[0][1]
    if e >= es[-1]: return rows[-1][1]
    i = bisect.bisect_left(es, e)
    e0, m0 = rows[i-1]; e1, m1 = rows[i]
    t = math.log(e/e0) / math.log(e1/e0)
    return math.exp(math.log(m0) + t*(math.log(m1)-math.log(m0)))

# elemental mass fractions (from PREREG2, checked against atomic weights below)
AW = {"H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999}
def fractions(formula):
    M = sum(AW[e]*n for e, n in formula.items())
    return {e: AW[e]*n/M for e, n in formula.items()}

EUM = fractions({"C": 18, "H": 10, "N": 2, "O": 4})
DHN = fractions({"C": 8, "H": 4, "O": 2})
BIOMASS_C10H18O5N = fractions({"C": 10, "H": 18, "O": 5, "N": 1})
WET5 = {}  # 0.60 H2O + 0.05 eumelanin + 0.35 C10H18O5N (run-1 recipe)
H2O_FRAC = fractions({"H": 2, "O": 1})
for e in ("H", "C", "N", "O"):
    WET5[e] = (0.60 * H2O_FRAC.get(e, 0) + 0.05 * EUM.get(e, 0) + 0.35 * BIOMASS_C10H18O5N.get(e, 0))
for nm, fr in (("EUM", EUM), ("DHN", DHN), ("WET5", WET5)):
    assert abs(sum(fr.values()) - 1) < 1e-9, nm

def compound_S(prog, frac, e):
    return sum(w * interp(load(prog, el), e) for el, w in frac.items())

TABLES = {(p, m): load(p, m) for p in ("PSTAR", "ASTAR") for m in ("water", "polyethylene", "aluminum", "H", "C", "N", "O")}
def S(prog, mat, e):
    if mat in ("eumelanin", "dhn", "wet5"):
        fr = {"eumelanin": EUM, "dhn": DHN, "wet5": WET5}[mat]
        return sum(w * interp(TABLES[(prog, el)], e) for el, w in fr.items())
    return interp(TABLES[(prog, mat)], e)

bins = [(1, 10), (10, 100), (100, 1000), (1000, 10000)]
res = {"assumptions": "Bragg additivity; total mass stopping power; bins 1-10/10-100/100-1000/1000-10000 MeV"}

# ---- G6 (PSTAR, protons) ----
q6 = {}
for mel in ("eumelanin", "dhn"):
    per = {}
    for lo, hi in bins:
        grid = [lo * 10**(i/10) for i in range(11)]
        per[f"{lo}-{hi} MeV"] = {
            "min_ratio_vs_water": round(min(S("PSTAR", mel, e)/S("PSTAR", "water", e) for e in grid), 4),
            "min_ratio_vs_polyethylene": round(min(S("PSTAR", mel, e)/S("PSTAR", "polyethylene", e) for e in grid), 4)}
    q6[mel] = per
g6_pass = all(b["min_ratio_vs_water"] > 2 and b["min_ratio_vs_polyethylene"] > 2
              for mel in q6.values() for b in mel.values())
res["G6"] = {"gate": "melanin proton S/rho > 2x water AND polyethylene in every bin 1 MeV-10 GeV, both compositions",
             "ratios": q6, "PASS": g6_pass, "predicted": False}

# ---- descriptives ----
desc = {}
for mel in ("eumelanin", "dhn"):
    desc[f"{mel}_at_1GeV_protons"] = {"vs_water": round(S("PSTAR", mel, 1000)/S("PSTAR", "water", 1000), 4),
                                       "vs_polyethylene": round(S("PSTAR", mel, 1000)/S("PSTAR", "polyethylene", 1000), 4)}
desc["wet_biomass_5pct_at_1GeV_protons_vs_water"] = round(S("PSTAR", "wet5", 1000)/S("PSTAR", "water", 1000), 4)
astar = {}
for mel in ("eumelanin", "dhn"):
    astar[mel] = {f"{lo}-{hi} MeV": round(min(S("ASTAR", mel, min(e, 1000))/S("ASTAR", "water", min(e, 1000)) for e in [lo*10**(i/10) for i in range(11) if lo*10**(i/10) <= 1000]), 4)
                  for lo, hi in bins[:3]}
desc["ASTAR_min_ratio_vs_water"] = astar
res["descriptives"] = desc

(OUT / "gates2.json").write_text(json.dumps(res, indent=2))
print("G6", "PASS" if g6_pass else "FAIL", "(predicted FAIL)")
for mel in ("eumelanin", "dhn"):
    print(" ", mel, {k: v["min_ratio_vs_water"] for k, v in q6[mel].items()})
print("1 GeV protons:", json.dumps(desc["eumelanin_at_1GeV_protons"]), "wet5 vs water:", desc["wet_biomass_5pct_at_1GeV_protons_vs_water"])
print("ASTAR eumelanin min ratios vs water:", astar["eumelanin"])
