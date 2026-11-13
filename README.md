# fungal-melanin-radioprotection (MEL-SHIELD)

Reproducible computational tests of what fungal melanin biology can and cannot support for radiation-protective human tissue. Preregistered gates, checksummed public data, nulls reported as nulls. No wet-lab, no clinical claims.

## Runs

- **Run 1 (photons)**: PREREG.md + Addendum 1 -> fetch_xcom.py -> analyze.py -> RESULTS.md (gates G1, G2, Q3, G4, Q5) with post-review qualifications. Data: NIST XCOM, 9 materials, `data/manifest.json`.
- **Run 2 (charged particles)**: PREREG2.md -> fetch_star.py -> analyze2.py -> RESULTS2.md (gate G6 + descriptives) with post-review qualification. Data: NIST PSTAR/ASTAR, 14 tables, `data/manifest_star.json`.

## Reproduce

Python 3, standard library only:

    python3 fetch_xcom.py     # run 1 data (REFETCH=1 to force re-download)
    python3 analyze.py        # run 1 gates -> results/gates.json
    python3 fetch_star.py     # run 2 data
    python3 analyze2.py       # run 2 gates -> results/gates2.json

Raw NIST responses are kept under data/raw/ and data/raw/star/; every parsed table is sha256-hashed in the manifests with retrieval timestamps (see DATA_MANIFEST.md for sources and exact URLs).

## Provenance

All commits pushed to this repository. Run 1 results at commit 4003a07; post-review qualifications 59f65f7; PREREG2 frozen at 4de573c before run-2 data; run 2 results at a6e31be.
