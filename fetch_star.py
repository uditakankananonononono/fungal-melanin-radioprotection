#!/usr/bin/env python3
"""Fetch NIST PSTAR/ASTAR stopping-power tables for MEL-SHIELD-2 materials.

Saves raw HTML per material/particle to data/raw/star/<prog>_<matno>.html,
parsed TSVs to data/star/<prog>_<name>.tsv, and writes
data/manifest_star.json with sha256 + retrieval timestamps (UTC).
Read-only against NIST; standard grid only; one request per material/particle.
"""
import hashlib, json, re, time, pathlib, datetime, urllib.request

URL = "https://physics.nist.gov/cgi-bin/Star/ap_table.pl"
MAT = {"H": "001", "C": "006", "N": "007", "O": "008",
       "aluminum": "013", "polyethylene": "221", "water": "276"}
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}

rawdir = pathlib.Path("data/raw/star"); rawdir.mkdir(parents=True, exist_ok=True)
tsvdir = pathlib.Path("data/star"); tsvdir.mkdir(parents=True, exist_ok=True)
manifest = {}

ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
CELL = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
TAG = re.compile(r"<[^>]+>")

for prog in ("PSTAR", "ASTAR"):
    for name, matno in MAT.items():
        body = (f"prog={prog}&matno={matno}&ShowDefault=on&GraphType=None").encode()
        req = urllib.request.Request(URL, data=body, headers=UA)
        html = urllib.request.urlopen(req, timeout=60).read()
        p = rawdir / f"{prog}_{matno}.html"
        p.write_bytes(html)
        rows = []
        for r in ROW.findall(html.decode("utf-8", "replace")):
            cells = [TAG.sub("", c).strip() for c in CELL.findall(r)]
            if len(cells) >= 5 and re.match(r"^[\d.]", cells[0]):
                try:
                    e, se, sn, st = (float(cells[i]) for i in range(4))
                    rows.append((e, se, sn, st))
                except ValueError:
                    pass
        assert len(rows) >= 100, (prog, name, len(rows))
        txt = tsvdir / f"{prog}_{name}.tsv"
        txt.write_text("energy_MeV\telectronic\tnuclear\ttotal\n"
                       + "".join("\t".join(f"{v:.5E}" for v in r) + "\n" for r in rows))
        manifest[f"{prog}_{name}"] = {
            "matno": matno, "rows": len(rows),
            "sha256_html": hashlib.sha256(p.read_bytes()).hexdigest(),
            "sha256_tsv": hashlib.sha256(txt.read_bytes()).hexdigest(),
            "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "source": URL, "program": prog}
        print(f"{prog} {name}: {len(rows)} rows, E {rows[0][0]:.3g}..{rows[-1][0]:.3g} MeV")
        time.sleep(2)

pathlib.Path("data/manifest_star.json").write_text(json.dumps(manifest, indent=2))
print("star manifest written:", len(manifest), "tables")
