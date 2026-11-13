# MEL-SHIELD preregistration (frozen before any result-producing code)

Frozen 2026-11-13, before any analysis code. Any later change is a labelled addendum; this file is never edited in place.

## Objective (owner's words, Nov 13 WhatsApp)

"Develop and evaluate a reproducible computational project testing what fungal melanin biology can—and cannot—support for radiation-protective human tissue."

## Scope rules

- Computational only. No wet-lab, no human-tissue engineering, no treatment instructions.
- Simulations and literature arithmetic are never clinical proof. Every "can/cannot" verdict is scoped to what the cited public data and stated physics support.
- Negative and null results are preserved and reported as plainly as positive ones.
- Named baselines throughout: liquid water (tissue proxy), polyethylene (standard spacecraft shielding), aluminum (spacecraft structure).
- All external data files are checksummed (sha256) with retrieval dates in DATA_MANIFEST.md.

## Verified starting evidence (already read, cited here with source)

E1. Shunk, Gomez & Averesch, Front. Microbiol. 13:877625 (2022) — the actual ISS experiment:
    - C. sphaerospermum on the ISS grew at k = 0.299 h^-1 vs ground controls k = 0.241/0.231/0.196 h^-1 (flight 1.21 +/- 0.37x ground), single flight replicate, microgravity confound acknowledged by the authors.
    - Radiation counts beneath the fully grown fungal layer: 147 vs 151 counts-per-minute (experiment vs control), i.e. ~2.6% fewer counts, difference concentrated in the late phase (200-622 h) at full growth. Biomass layer at most ~1.67 mm thick. Authors state the reduction is "potentially attributable to the fungal biomass" and do not claim melanin-specific attenuation.
    - Authors state passive shielding against GCR is "ultimately limited by mass density."
E2. Dadachova et al., PLoS ONE 2(5):e457 (2007) — melanized fungi showed enhanced growth under 500x-background gamma; "radiosynthesis" remains a hypothesis (as the ISS authors restate).
E3. ISS dose context from E1's citations: ~144 mSv/year ISS vs ~6.2 mSv/year Earth background; ~80% of ISS dose from GCR/SEP particles.

## Questions, computations and frozen gates

### Q1 — Is melanin's photon mass-attenuation special per unit mass?

Compute mass attenuation coefficients (mu/rho) from NIST XCOM for: eumelanin (C18H10N2O4 unit), fungal DHN-melanin (C8H4O2 unit), hydrated fungal biomass (60% water by mass, melanin fraction varied 0-30%), liquid water, polyethylene (CH2), aluminum. Energies: 1 keV to 10 MeV, log-spaced.

- G1 PASS (melanin special): melanin's mu/rho exceeds BOTH water's and polyethylene's by >2x in every decade bin of 10 keV-1 MeV.
- G1 FAIL (not special per mass): otherwise.
- Prediction: FAIL. Composition sensitivity (eumelanin vs DHN) reported; the verdict must hold for BOTH melanin compositions to count.

### Q2 — Does the ISS attenuation observation require melanin-specific physics?

From E1: ~2.6% count reduction behind <=1.67 mm of hydrated biomass (density assumed 1.0-1.1 g/cm3, areal density 0.167-0.184 g/cm2). Compute the effective mu/rho a Beer-Lambert layer needs to produce 2.6% attenuation: mu_eff = -ln(0.974)/x. Compare against the XCOM mu/rho ranges of water and melanin over 20 keV-2 MeV (detector-sensitive band assumption, labelled as an assumption).

- G2 PASS (melanin-specific physics required): required mu_eff falls outside the water range for the whole band AND inside melanin's.
- G2 FAIL (data explained by mass alone): required mu_eff lies within water's band range.
- Prediction: FAIL (plain hydrated mass suffices). Caveat frozen: the ISS detector count spectrum is not published per-energy; this gate tests necessity of melanin physics, not the exact detector response.

### Q3 — How fast can biology accrue shielding mass?

From E1: full-coverage layer (~0.18 g/cm2) in ~48 h. Generous accrual model: 0.09 g/cm2/day, assuming repeated full-harvest cycles at the observed per-cycle density (assumption labelled; logistic saturation means this is an upper bound). Compute days to reach 1, 5, 10, 20 g/cm2.

- Descriptive, no pass/fail. Frozen computation and assumption list.

### Q4 — What can a biologically grown layer do for human-tissue dose?

Optimistic Beer-Lambert bound: dose transmission T = exp(-x/lambda) with lambda = 100 g/cm2 (order-of-magnitude attenuation length for GeV protons, cited from standard references; labelled as an optimistic bound because secondary build-up is ignored and heavy-ion dose equivalent is worse).

- G4 PASS (meaningful tissue protection feasible): a layer accrual-feasible within 30 days at the Q3 rate cuts transmitted dose by >20% under this optimistic bound.
- G4 FAIL: otherwise.
- Prediction: FAIL (0.18-5 g/cm2 transmits 95%+).

### Q5 — Can melanin's radical scavenging protect human tissue chemically?

Compare, per gram of tissue: published melanin radical-scavenging capacity (one-time, non-regenerating) vs endogenous glutathione (1-10 umol/g tissue, enzyme-regenerated). Sources cited in DATA_MANIFEST. Descriptive; frozen computation. Claim tested: added melanin at plausible loading (<1 g/kg tissue) does not exceed endogenous regenerable capacity. Prediction: claim holds (cannot support therapeutic chemical protection).

## Verdict matrix to be populated (predictions, not outcomes)

CAN (predicted): UV shielding (literature, cited); the fungus's OWN radioresistance (E1/E2); self-replicating in-situ bulk mass equivalent to water for habitat shielding (ISRU framing from E1); a few-percent count reduction at ~0.18 g/cm2 (E1, verified arithmetic).
CANNOT (predicted): per-mass ionizing-radiation superiority over water/polyethylene; melanin-specific explanation of the ISS attenuation; meaningful GCR dose reduction for human tissue at biologically accrual-feasible mass; clinical/therapeutic radioprotection of human tissue; "radiosynthesis" as established fact.

## Success criterion for the project itself

The project succeeds if every gate runs reproducibly from checksummed public data, predictions are scored honestly (including prediction failures), and the can/cannot matrix is populated with numbers. It does not require any particular claim to win.
