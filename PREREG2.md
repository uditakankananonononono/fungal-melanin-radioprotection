# MEL-SHIELD-2 preregistration (frozen before any data pull or result-producing code)

Frozen 2026-11-13, after run 1 (commit 59f65f7), before any PSTAR/ASTAR data is fetched or analysis code written. This file is never edited in place; later changes are labelled addenda.

## Motivation

Run 1 tested photons only (XCOM). The dominant dose component in deep space is charged particles, mostly protons and alpha particles (E1 context: ~80% of ISS dose from GCR/SEP particles). The same per-mass-special question must therefore be asked for charged-particle stopping, or run 1's G1 verdict covers only the photon channel.

## Question, computation and frozen gate

### Q6 - Is melanin's charged-particle mass stopping power special per unit mass?

Compute proton mass stopping power (S/rho, MeV cm2/g) from NIST PSTAR for: liquid water (matno 276), polyethylene (221), aluminum (013), and the elemental tables H (001), C amorphous (006), N (007), O (008). Melanin compositions (eumelanin unit C18H10N2O4; fungal DHN-melanin unit C8H4O2) are computed by Bragg additivity, S/rho = sum(w_i * S_i/rho_i) with w_i elemental mass fractions (eumelanin: C 0.6793, H 0.03167, N 0.08798, O 0.20106; DHN: C 0.7273, H 0.03052, O 0.24220).

- Frozen assumptions, labelled: (a) Bragg-Kleeman additivity neglects chemical-binding corrections to the mean excitation energy; PSTAR's own methodology documents these as small for the materials compared here, and the same approximation is applied uniformly so no comparison is skewed toward melanin. (b) Carbon uses the amorphous-carbon table (density 2.0), the standard Bragg input. (c) Alpha-particle stopping from ASTAR for the same materials is reported descriptively with identical additivity.
- Energy range: full PSTAR grid (1 keV - 10 GeV). Gate bins (GCR-relevant): 1-10, 10-100, 100-1000, 1000-10000 MeV.
- G6 PASS (melanin special per unit mass): melanin's S/rho exceeds BOTH water's and polyethylene's by >2x in every gate bin, for BOTH compositions.
- G6 FAIL: otherwise.
- Prediction: FAIL. Mass stopping power scales roughly with Z/A in the Bethe regime; eumelanin Z/A ~ 0.515 vs water 0.555, so melanin is expected slightly BELOW water per unit mass, with the same direction expected for DHN.

### Descriptive checks (no gate)

- Alpha-particle (ASTAR) analogue of the Q6 comparison, same materials and bins.
- Ratio of melanin to water and to polyethylene at 1 GeV protons (a representative GCR energy), both compositions.
- Hydrated-biomass context: wet biomass (60% water, 5% eumelanin) S/rho vs water at 1 GeV, from the same additivity applied to the run-1 biomass recipe.

## Honesty and scope rules (carried from PREREG.md and Addendum 1)

- Nulls are reported as nulls; a completed run is not scientific success.
- Verdicts are bounded to the stated compositions, the Bragg-additivity model, and the tested energy grid. No global claims.
- All data files checksummed (sha256) with retrieval timestamps in the manifest; NIST PSTAR/ASTAR cited with exact URLs.
