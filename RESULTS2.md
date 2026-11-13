# MEL-SHIELD-2 results (run 2026-11-13)

Gate G6 implemented in `analyze2.py` against checksummed NIST PSTAR/ASTAR tables (`data/star/*.tsv`, hashes in `data/manifest_star.json`). Gate and thresholds exactly as frozen in `PREREG2.md` (commit 4de573c, before any data pull). Reproduce: `python3 fetch_star.py && python3 analyze2.py` (stdlib only).

## Gate outcome

| Gate | Question | Predicted | Outcome | Key numbers |
|---|---|---|---|---|
| G6 | Is melanin's proton mass stopping power special per unit mass? | FAIL | **FAIL** | Under Bragg additivity, melanin S/rho is BELOW water's in every gate bin (min ratios vs water: eumelanin 0.915-0.925 across 1 MeV-10 GeV; DHN 0.911-0.923), and below polyethylene's (0.872 at 1 GeV). Nowhere near the >2x bar in any bin, for either composition. |

Prediction score: 1/1 (G6 predicted FAIL, observed FAIL).

## Descriptive results (no gate)

- At 1 GeV protons (representative GCR energy): eumelanin 0.915x water, 0.872x polyethylene; DHN similar (0.912x water).
- Hydrated fungal biomass (run-1 wet recipe, 60% water + 5% eumelanin): 0.990x water at 1 GeV, i.e. essentially water, as expected for a mostly-water layer.
- Alpha particles (ASTAR, same additivity): same direction, eumelanin min ratios vs water 0.898-0.924 over 1 MeV-1 GeV.

## Scope of these claims (bounded)

- Bounded to the two stated unit compositions (C18H10N2O4, C8H4O2), the Bragg-Kleeman additivity model (chemical-binding corrections to mean excitation energy neglected, applied uniformly to all compared materials), the total (electronic + nuclear) mass stopping power, and the 1 keV-10 GeV PSTAR / 1 keV-1 GeV ASTAR grids. No claim is made outside this scope.
- The direction of the result matches the frozen Z/A expectation (eumelanin Z/A ~ 0.515 vs water 0.555), which is corroboration, not a fitted outcome.
- Combined with run 1 (photons, XCOM): within the tested compositions, models, and energy grids, melanin is not per-unit-mass special for EITHER the photon channel or the charged-particle channel. This remains a bounded statement about those channels and models, not a universal property of all melanin chemistry.

## Sources (exact URLs)

- NIST PSTAR: Stopping-Power and Range Tables for Protons (Berger, Coursey, Zucker): https://physics.nist.gov/PhysRefData/Star/Text/PSTAR.html
- NIST ASTAR: Stopping-Power and Range Tables for Helium Ions: https://physics.nist.gov/PhysRefData/Star/Text/ASTAR.html
- Data pulled via https://physics.nist.gov/cgi-bin/Star/ap_table.pl on 2026-11-13; material numbers, sha256 and retrieval timestamps in `data/manifest_star.json`.
- Bragg-Kleeman additivity is the standard rule documented in the PSTAR/ASTAR methodology (same pages).
