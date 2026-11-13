#!/usr/bin/env python3
"""Fetch NIST XCOM mass attenuation tables for MEL-SHIELD materials.

Saves raw HTML per material to data/raw/<name>.html and writes
data/manifest.json with sha256 + retrieval timestamp (UTC).
Read-only against NIST; standard grid only; one request per material.
"""
import hashlib, json, re, time, urllib.parse, urllib.request, pathlib, datetime

# local name -> (xcom-safe display name, formulae). XCOM 'Name' rejects long/digit-heavy strings.
MATERIALS = {
    "water": ("water", "H2O 1"),
    "polyethylene": ("polyeth", "CH2 1"),
    "aluminum": ("aluminum", "Al 1"),
    "eumelanin_C18H10N2O4": ("eumelanin", "C18H10N2O4 1"),
    "dhn_melanin_C8H4O2": ("dhnmel", "C8H4O2 1"),
    "wet_biomass_5pct_eumelanin": ("wetbiofive", "H2O 0.60\nC18H10N2O4 0.05\nC10H18O5N 0.35"),
    "wet_biomass_30pct_eumelanin": ("wetbiothirty", "H2O 0.60\nC18H10N2O4 0.30\nC10H18O5N 0.10"),
    "dry_biomass_5pct_eumelanin": ("drybiofive", "C18H10N2O4 0.05\nC10H18O5N 0.95"),
    "tissue_icru44_approx": ("tissueicru", "H 0.101\nC 0.111\nN 0.026\nO 0.761"),
}
URL = "https://physics.nist.gov/cgi-bin/Xcom/xcom3_3"
outdir = pathlib.Path("data/raw"); outdir.mkdir(parents=True, exist_ok=True)
manifest = {}

ROW = re.compile(r"<tr BGColor=\"#FFFFCC\">\s*<td>([^<]*)</td>(.*?)</tr>", re.S)
CELL = re.compile(r"<td[^>]*>([^<]*)</td>")

for name, (xname, formulae) in MATERIALS.items():
    import os
    if not os.environ.get("REFETCH") and pathlib.Path(f"data/{name}.tsv").exists():
        print(name, "already fetched; skipping"); continue
    body = urllib.parse.urlencode({
        "Formulae": formulae, "NumAdd": "2", "Output": "on", "Name": xname,
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"})
    html = urllib.request.urlopen(req, timeout=60).read()
    p = outdir / f"{name}.html"
    p.write_bytes(html)
    rows = []
    for m in ROW.finditer(html.decode("utf-8", "replace")):
        cells = CELL.findall(m.group(2))
        if len(cells) == 8:
            try:
                rows.append(tuple(float(c) for c in cells))
            except ValueError:
                pass
    assert len(rows) >= 50, (name, len(rows))
    txt = pathlib.Path(f"data/{name}.tsv")
    txt.write_text("energy_MeV\tcoherent\tincoherent\tphotoelectric\tpair_nuclear\tpair_electron\ttotal_with_coh\ttotal_without_coh\n"
                   + "".join("\t".join(f"{v:.4E}" for v in r) + "\n" for r in rows))
    assert b"XCOM: Error" not in html, (name, "XCOM error page")
    manifest[name] = {
        "formulae": formulae, "rows": len(rows),
        "sha256_html": hashlib.sha256(p.read_bytes()).hexdigest(),
        "sha256_tsv": hashlib.sha256(txt.read_bytes()).hexdigest(),
        "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "source": URL,
    }
    print(f"{name}: {len(rows)} rows, E {rows[0][0]:.3g}..{rows[-1][0]:.3g} MeV")
    time.sleep(2)  # be polite to NIST

pathlib.Path("data/manifest.json").write_text(json.dumps(manifest, indent=2))
print("manifest written")
