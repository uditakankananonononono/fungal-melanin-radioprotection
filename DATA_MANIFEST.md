# DATA MANIFEST

All attenuation data: NIST XCOM: Photon Cross Sections Database (Berger, Hubbell, Seltzer, Chang, Coursey, Sukumar, Zucker, Olsen).
Landing: https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html
Retrieval endpoint: https://physics.nist.gov/cgi-bin/Xcom/xcom3_3 (POST per material; raw HTML preserved under data/raw/).

Literature sources (numbers quoted in RESULTS.md):
- Shunk, Gomez & Averesch 2022, Front. Microbiol. 13:877625: https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2022.877625/full
- Dadachova et al. 2007, PLoS ONE 2(5):e457: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0000457
- Schweitzer et al. 2009, PLoS ONE 4(9):e7229: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0007229
- Chatterjee 2013, Nutrients 5(2):525-542: https://www.mdpi.com/2072-6643/5/2/525

| material | formulae (weight fractions) | rows | retrieved UTC | sha256 (tsv, first 16) |
|---|---|---|---|---|
| water | `H2O 1` | 80 | 2026-11-13T07:51:24+00:00 | 2070fad318fa99c5... |
| polyethylene | `CH2 1` | 80 | 2026-11-13T07:51:27+00:00 | 7c7a97928eafd5fb... |
| aluminum | `Al 1` | 81 | 2026-11-13T07:51:29+00:00 | 8daab6ab3d86578c... |
| eumelanin_C18H10N2O4 | `C18H10N2O4 1` | 80 | 2026-11-13T07:51:31+00:00 | 853c54f919743d3b... |
| dhn_melanin_C8H4O2 | `C8H4O2 1` | 80 | 2026-11-13T07:51:33+00:00 | f1ff09799dd444fc... |
| wet_biomass_5pct_eumelanin | `H2O 0.60
C18H10N2O4 0.05
C10H18O5N 0.35` | 80 | 2026-11-13T07:51:35+00:00 | 1aec9d4d370ca5b0... |
| wet_biomass_30pct_eumelanin | `H2O 0.60
C18H10N2O4 0.30
C10H18O5N 0.10` | 80 | 2026-11-13T07:51:38+00:00 | f73e081c164d7025... |
| dry_biomass_5pct_eumelanin | `C18H10N2O4 0.05
C10H18O5N 0.95` | 80 | 2026-11-13T07:51:40+00:00 | 475900498d545697... |
| tissue_icru44_approx | `H 0.101
C 0.111
N 0.026
O 0.761` | 80 | 2026-11-13T07:51:42+00:00 | 5f903096b262da87... |

Verification: `python3 analyze.py` re-checks nothing about provenance; to verify hashes, re-run `REFETCH=1 python3 fetch_xcom.py` on a clean checkout and diff data/manifest.json, or sha256sum data/*.tsv against the values above (full values in data/manifest.json).
