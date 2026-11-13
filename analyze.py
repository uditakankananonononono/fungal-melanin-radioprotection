#!/usr/bin/env python3
"""MEL-SHIELD gate computations Q1-Q5.

Implements exactly the frozen gates in PREREG.md against the checksummed
NIST XCOM tables in data/*.tsv (see data/manifest.json for sha256 + retrieval
timestamps). No fitted parameters; every threshold is from PREREG.md.

Output: results/gates.json (machine-readable) and a printed table.
"""
import json, math, pathlib

DATA = pathlib.Path("data")
OUT = pathlib.Path("results"); OUT.mkdir(exist_ok=True)

def load(name):
    rows = []
    for line in (DATA / f"{name}.tsv").read_text().splitlines()[1:]:
        e, coh, incoh, pe, pn, pel, twc, twoc = (float(v) for v in line.split("\t"))
        rows.append((e, twoc))  # energy_MeV, mass attenuation total without coherent (cm^2/g)
    return rows

MAT = {m: load(m) for m in [
    "water", "polyethylene", "aluminum",
    "eumelanin_C18H10N2O4", "dhn_melanin_C8H4O2",
    "wet_biomass_5pct_eumelanin", "wet_biomass_30pct_eumelanin",
    "dry_biomass_5pct_eumelanin", "tissue_icru44_approx"]}

def mu_at(mat, e_mev):
    """Interpolated mu/rho (log-log) at energy e_mev."""
    rows = MAT[mat]
    if e_mev <= rows[0][0]: return rows[0][1]
    if e_mev >= rows[-1][0]: return rows[-1][1]
    import bisect
    i = bisect.bisect_left([r[0] for r in rows], e_mev)
    e0, m0 = rows[i-1]; e1, m1 = rows[i]
    t = math.log(e_mev/e0) / math.log(e1/e0)
    return math.exp(math.log(m0) + t*(math.log(m1)-math.log(m0)))

gates = {}

# ---------- Q1 ----------
# G1 PASS iff, in EVERY decade bin of 10 keV-1 MeV, melanin mu/rho exceeds BOTH
# water's and polyethylene's by >2x; must hold for BOTH melanin compositions.
bins = [(0.01, 0.1), (0.1, 1.0)]
q1 = {}
for mel in ["eumelanin_C18H10N2O4", "dhn_melanin_C8H4O2"]:
    per_bin = {}
    for lo, hi in bins:
        grid = [lo * 10**(i/10) for i in range(11)]
        rw = min(mu_at(mel, e)/mu_at("water", e) for e in grid)          # worst case vs water
        rp = min(mu_at(mel, e)/mu_at("polyethylene", e) for e in grid)   # worst case vs PE
        per_bin[f"{lo}-{hi} MeV"] = {"min_ratio_vs_water": round(rw, 3),
                                     "min_ratio_vs_polyethylene": round(rp, 3)}
    q1[mel] = per_bin
q1_pass = all(b["min_ratio_vs_water"] > 2 and b["min_ratio_vs_polyethylene"] > 2
              for mel in q1.values() for b in mel.values())
# context: hydrated biomass vs water (what the ISS layer actually is)
ctx = {}
for name in ["wet_biomass_5pct_eumelanin", "wet_biomass_30pct_eumelanin", "dry_biomass_5pct_eumelanin"]:
    ctx[name] = {f"{lo}-{hi} MeV": round(min(mu_at(name, e)/mu_at("water", e) for e in [lo*10**(i/10) for i in range(11)]), 3)
                 for lo, hi in bins}
gates["Q1"] = {"gate": "G1: melanin mu/rho > 2x water AND polyethylene in every decade bin 10 keV-1 MeV, both melanin compositions",
               "ratios": q1, "biomass_min_ratio_vs_water": ctx,
               "PASS": q1_pass, "predicted": False}

# ---------- Q2 ----------
# ISS layer: <=1.67 mm hydrated biomass, density 1.0-1.1 g/cm3 -> 0.167-0.184 g/cm2.
# Required effective mu/rho for the observed 2.6% reduction: -ln(0.974)/x.
ATT = 0.026
x_lo, x_hi = 0.167, 0.184
mu_eff = [-math.log(1-ATT)/x for x in (x_hi, x_lo)]  # low..high
band = [0.02 * 10**(i/10) for i in range(21)]  # 20 keV - 2 MeV
wrange = (min(mu_at("water", e) for e in band), max(mu_at("water", e) for e in band))
mrange = (min(mu_at("eumelanin_C18H10N2O4", e) for e in band), max(mu_at("eumelanin_C18H10N2O4", e) for e in band))
inside_water = wrange[0] <= mu_eff[0] and mu_eff[1] <= wrange[1]
gates["Q2"] = {"gate": "G2 PASS only if required mu_eff outside water's 20 keV-2 MeV band for whole band AND inside melanin's",
               "required_mu_eff_cm2_g": [round(v, 4) for v in mu_eff],
               "water_band_range": [round(v, 4) for v in wrange],
               "eumelanin_band_range": [round(v, 4) for v in mrange],
               "required_within_water_band": inside_water,
               "PASS": (not inside_water) and mrange[0] <= mu_eff[0] and mu_eff[1] <= mrange[1],
               "predicted": False}

# ---------- Q3 ----------
RATE = 0.09  # g/cm2/day, generous upper bound (PREREG Q3)
gates["Q3"] = {"accrual_g_cm2_day": RATE,
               "days_to": {f"{t} g/cm2": round(t/RATE, 1) for t in (1, 5, 10, 20)},
               "descriptive": True}

# ---------- Q4 ----------
LAM = 100.0  # g/cm2 optimistic attenuation length (PREREG Q4)
x30 = RATE * 30
T = math.exp(-x30/LAM)
cut = 1 - T
x_for_20pct = -LAM * math.log(0.8)
gates["Q4"] = {"gate": "G4 PASS if 30-day-accrual layer cuts transmitted dose >20% under optimistic Beer-Lambert, lambda=100 g/cm2",
               "x_30d_g_cm2": round(x30, 2), "transmission": round(T, 4),
               "dose_cut_pct": round(100*cut, 2),
               "areal_needed_for_20pct_g_cm2": round(x_for_20pct, 1),
               "days_to_20pct": round(x_for_20pct/RATE, 1),
               "PASS": cut > 0.20, "predicted": False}

# ---------- Q5 ----------
# Numbers with sources (exact URLs in RESULTS.md / DATA_MANIFEST.md):
# - Melanin stable free radicals: 9.05e17 - 7.09e18 spins/g (Schweitzer 2009, Table 1, EPR).
#   One-time trapping capacity taken as <= ~10x the stable-radical count (labelled assumption).
# - GSH: millimolar intracellular (1-10 umol/g tissue), enzymatically regenerated (PMC3635210).
SPINS_MAX = 7.09e18          # per g melanin, best measured synthetic melanin
CAPACITY_MAX = 10 * SPINS_MAX  # generous one-time scavenging capacity per g (assumption)
LOAD = 1e-3                  # g melanin per g tissue (1 g/kg, plausible-loading ceiling, PREREG)
GSH_LO, GSH_HI = 1e-6 * 6.022e23, 1e-5 * 6.022e23  # molecules per g tissue
added = CAPACITY_MAX * LOAD
gates["Q5"] = {"melanin_stable_radicals_per_g_max": SPINS_MAX,
               "assumed_one_time_capacity_per_g": CAPACITY_MAX,
               "loading_g_per_g_tissue": LOAD,
               "added_one_time_capacity_per_g_tissue": added,
               "endogenous_GSH_per_g_tissue": [GSH_LO, GSH_HI],
               "GSH_regenerated": True,
               "added_exceeds_endogenous": added > GSH_HI,
               "claim_holds_melanin_cannot_beat_GSH": added <= GSH_HI,
               "descriptive": True}

(OUT / "gates.json").write_text(json.dumps(gates, indent=2))

# ---------- print ----------
def pf(q): return "PASS" if gates[q]["PASS"] else "FAIL"
print(f"Q1 {pf('Q1')} (predicted FAIL)  worst ratios vs water: " +
      ", ".join(f"{m.split('_')[0]}={min(b['min_ratio_vs_water'] for b in q1[m].values())}"
                for m in q1))
print(f"Q2 {pf('Q2')} (predicted FAIL)  mu_eff required {gates['Q2']['required_mu_eff_cm2_g']} vs water band {gates['Q2']['water_band_range']}")
print(f"Q3 (descriptive)  days to 1/5/10/20 g/cm2: {list(gates['Q3']['days_to'].values())}")
print(f"Q4 {pf('Q4')} (predicted FAIL)  30d layer: {gates['Q4']['dose_cut_pct']}% cut; needs {gates['Q4']['days_to_20pct']} d for 20%")
print(f"Q5 (descriptive)  added one-time {added:.2e}/g tissue vs endogenous GSH {GSH_LO:.1e}-{GSH_HI:.1e}/g regenerated; claim holds: {gates['Q5']['claim_holds_melanin_cannot_beat_GSH']}")
scored = [q for q in ("Q1", "Q2", "Q4")]
print("prediction score:", sum(gates[q]["PASS"] == gates[q]["predicted"] for q in scored), "/", len(scored))
