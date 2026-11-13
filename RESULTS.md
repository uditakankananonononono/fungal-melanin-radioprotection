# MEL-SHIELD results (run 2026-11-13)

All gates implemented in `analyze.py` against checksummed NIST XCOM tables (`data/*.tsv`, hashes in `data/manifest.json`, human-readable `DATA_MANIFEST.md`). Gates and thresholds exactly as frozen in `PREREG.md`. Reproduce: `python3 fetch_xcom.py && python3 analyze.py` (stdlib only).

## Gate outcomes

| Gate | Question | Predicted | Outcome | Key numbers |
|---|---|---|---|---|
| G1 | Is melanin's photon mass-attenuation special per unit mass? | FAIL | **FAIL** | Melanin never exceeds water per unit mass anywhere on the 1 keV-100 MeV grid; max ratio 0.929 (eumelanin, 0.32 MeV), worst 0.585 (10 keV). Vs polyethylene it reaches only 1.53x (10 keV), below the 2x bar, and falls below PE above ~30 keV. Identical verdict for DHN-melanin (max 0.927 vs water). |
| G2 | Does the ISS 2.6% attenuation require melanin-specific physics? | FAIL | **FAIL** | Required mu_eff = 0.143-0.158 cm2/g (areal density 0.167-0.184 g/cm2, -ln(0.974)/x). Water's mu/rho spans 0.049-0.721 cm2/g over 20 keV-2 MeV, so the required value sits comfortably inside plain water's range (it equals water's at ~100 keV). No melanin-specific physics needed; mass alone suffices. |
| Q3 | How fast can biology accrue shielding mass? | (descriptive) | computed | At the generous 0.09 g/cm2/day upper bound: 11.1 d to 1 g/cm2, 55.6 d to 5, 111 d to 10, 222 d to 20. |
| G4 | Can a 30-day-grown layer cut tissue dose >20% (optimistic Beer-Lambert, lambda=100 g/cm2)? | FAIL | **FAIL** | 30-day accrual = 2.7 g/cm2 -> transmission exp(-0.027) = 0.973, a 2.66% cut. A 20% cut needs 22.1 g/cm2 = ~248 days of continuous optimal growth, even under the optimistic bound that ignores secondary build-up and heavy-ion quality factors. |
| Q5 | Can melanin's radical scavenging protect human tissue chemically? | claim holds | **claim holds** | Best measured melanin: 7.09e18 stable radicals/g (Schweitzer 2009, EPR, Table 1). Assuming one-time trapping capacity <= 10x that, at the prereg loading ceiling of 1 g/kg tissue the added one-time capacity is ~7.1e16 radicals/g tissue. Endogenous glutathione is 1-10 umol/g tissue = 6.0e17-6.0e18 molecules/g and is enzymatically regenerated. Added melanin is 10-100x below endogenous regenerable capacity, one-time vs regenerated, and only shown protective in cell culture at low photon energies (85 keV, 600 cGy, 20 ug/mL extracellular: 21-23% survival increase), not at MeV-GeV GCR energies. |

Prediction score on scored gates: 3/3. No prediction failures.

## Honest can / cannot matrix (populated)

CAN (supported by the cited data and this arithmetic):
- Shield UV (literature-established, not re-tested here).
- Protect the FUNGUS ITSELF: melanized fungi grow at least normally, possibly faster, under elevated radiation (E1 flight k=0.299 h^-1 vs ground 0.196-0.241 h^-1, 1.21 +/- 0.37x, single flight replicate with acknowledged microgravity confound; E2 enhanced growth at 500x background gamma).
- Provide a few-percent count reduction at ~0.18 g/cm2 hydrated biomass, indistinguishable from the same mass of water (E1's 147 vs 151 CPM; G2 arithmetic).
- Serve as self-replicating in-situ bulk mass for habitat shielding where mass is what matters and biology supplies it cheaply (ISRU framing from E1); per gram it is at best equal to water.

CANNOT (supported):
- Beat water or polyethylene per unit mass for ionizing photon shielding, in any energy decade, for either melanin composition (G1).
- Explain the ISS attenuation with melanin-specific physics; hydrated mass alone is sufficient (G2).
- Deliver meaningful (>20%) GCR dose reduction to human tissue within 30 days of growth; even an optimistic bound needs ~248 days (G4).
- Act as a chemical radioprotectant competitive with endogenous, enzyme-regenerated glutathione at any plausible tissue loading (Q5).
- Establish "radiosynthesis" as fact; both E1 and E2 present it as hypothesis.

## Sources (exact URLs)

- E1 (ISS experiment, all flight/ground growth rates, 147 vs 151 CPM, <=1.67 mm layer, "potentially attributable to fungal biomass", mass-density limit): Shunk, Gomez & Averesch, Front. Microbiol. 13:877625 (2022). https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2022.877625/full
- E2 (500x-background growth enhancement, radiosynthesis as hypothesis): Dadachova et al., PLoS ONE 2(5):e457 (2007). https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0000457
- Melanin stable-radical counts (9.05e17-7.09e18 spins/g), CHO-cell 21-23% survival increase at 600 cGy / 85 keV with 20 ug/mL melanin, Compton-recoil trapping mechanism, intracellular-delivery caveat: Schweitzer et al., PLoS ONE 4(9):e7229 (2009). https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0007229 (open copy: https://pmc.ncbi.nlm.nih.gov/articles/PMC2749938/)
- Glutathione "most abundant intracellular nonprotein thiol that reaches millimolar concentrations in most cell types" and its insufficiency for direct DNA-radical competition with oxygen: Chatterjee, Nutrients 5(2):525 (2013). https://www.mdpi.com/2072-6643/5/2/525 (open copy: https://pmc.ncbi.nlm.nih.gov/articles/PMC3635210/)
- Photon cross sections: NIST XCOM: Photon Cross Sections Database, Berger et al. https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html (data pulled via https://physics.nist.gov/cgi-bin/Xcom/xcom3_3 on 2026-11-13; formulae and sha256 per file in `data/manifest.json`).

## Scientific-success assessment (per Addendum 1)

Completed experiment: yes — every gate runs reproducibly from checksummed public data, and all predictions were scored honestly. Novel finding beating a named baseline: NO. Every "CAN" is a re-verification of published claims; every "CANNOT" is a null. The one independent, quantitative novelty is the explicit per-mass comparison showing melanin is uniformly WORSE than water across 1 keV-100 MeV (never reported this way in the cited promotion literature), which sharpens rather than overturns the authors' own "limited by mass density" statement.

## Post-review qualifications (2026-11-13, added after run 1; run 1 text above preserved verbatim)

Independent review of commit 4003a07 required these scoping qualifications. The gate arithmetic is unchanged; only claim wording is scoped.

1. **G1 is a bounded composition/energy result, not a global statement.** "Melanin never exceeds water per unit mass" holds only for the two tested compositions (C18H10N2O4 and C8H4O2 unit formulae), the photon total-attenuation-without-coherent coefficient, and the tested 1 keV-100 GeV NIST XCOM grid. Other melanin chemotypes, other interaction channels, and energies outside the grid were not tested. The frozen gate verdict (not special, by the >2x-both-decades criterion) stands.
2. **G2 establishes plausibility, not causation.** The required mu_eff falling inside water's 20 keV-2 MeV band shows the ISS count reduction is *consistent with* plain hydrated biomass and does not *require* melanin-specific physics. It does not establish that mass alone causally explains the observation; that would need the actual detector energy spectrum and geometry, which are not published (caveat already frozen in PREREG Q2). The gate tests necessity, and necessity is what failed.
3. **Q5 is bounded to its stated model.** The glutathione comparison shows melanin cannot compete *as a one-time, stoichiometric radical sink at <=1 g/kg tissue loading against enzyme-regenerated endogenous GSH*. It is not a general chemical or clinical impossibility claim: catalytic/regenerating melanin formulations, intracellular nanoparticle delivery (which Schweitzer 2009 explicitly raises), and low-photon-energy regimes (where 21-23% CHO-cell survival increases were measured) are outside its scope.
4. **No novelty claim is made from absence of statements in promotion literature.** The per-mass grid comparison is reported as this project's own computation from NIST data, nothing more.

## Post-review corrections 2 (2026-11-13, added after independent audit; earlier text preserved verbatim)

Independent audit reproduced both runs including NIST refetches and confirmed all gate computations. Three prose-level corrections (the gate arithmetic and all PASS/FAIL verdicts were and remain correct):

1. **G4 prose**: the areal density needed for a 20% cut is 22.3 g/cm2 (not 22.1 as the table prose said; gates.json had the correct 22.3). The derived ~248 days was computed from the correct value and stands.
2. **Q5 prose**: added melanin one-time capacity is 8.5-85x below endogenous GSH per gram of tissue (not "10-100x"; endpoints are 6.0e17/7.1e16 = 8.5 and 6.0e18/7.1e16 = 85).
3. **G1 peak location**: the eumelanin/water max-ratio energy is exactly 0.30 MeV, an actual XCOM grid node, with ratio 0.92881. The "0.32 MeV" in the table and the auditor's 0.282 MeV were both artifacts of coarse scan grids; the ratio value 0.929 is confirmed by all three computations. DHN-melanin's max is 0.92740 at 0.6 MeV (grid node). These peak-location differences do not touch any gate verdict: both melanins remain below water everywhere on the tested grid.
