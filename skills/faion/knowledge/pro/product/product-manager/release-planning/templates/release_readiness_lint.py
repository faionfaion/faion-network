#!/usr/bin/env python3
"""
purpose: Lint script for readiness matrix completeness.
consumes: input from methodology
produces: artefact for downstream agent
depends-on: content/02-output-contract.xml
token-budget-impact: 0 (executes locally)
"""

#!/usr/bin/env python3
"""
release_readiness_lint.py — fail CI if any "green" row lacks an evidence link.

Input:  release-readiness.md (table with columns: function, artifact, owner, status, evidence_link)
Usage:  python release_readiness_lint.py release-readiness.md
Exit:   0 = clean, 1 = at least one violation (suitable for pre-merge hook).
"""
import re, sys, pathlib

p = pathlib.Path(sys.argv[1])
lines = p.read_text(encoding="utf-8").splitlines()
rows = [ln for ln in lines if ln.startswith("|") and "---" not in ln]
if len(rows) < 2:
    sys.exit("readiness matrix has no rows")

hdr = [c.strip().lower() for c in rows[0].strip("|").split("|")]
need = {"function", "artifact", "owner", "status", "evidence_link"}
missing = need - set(hdr)
if missing:
    sys.exit(f"missing required columns: {missing}")

idx = {c: hdr.index(c) for c in need}
url_re = re.compile(r"https?://\S+")
violations = []

for ln in rows[1:]:
    cells = [c.strip() for c in ln.strip("|").split("|")]
    if len(cells) < len(hdr):
        continue
    status = cells[idx["status"]].lower()
    evidence = cells[idx["evidence_link"]]
    fn = cells[idx["function"]]
    art = cells[idx["artifact"]]
    if status == "green" and not url_re.search(evidence):
        violations.append(f"GREEN without evidence URL: {fn} / {art}")
    if status in ("yellow", "red") and not cells[idx["owner"]]:
        violations.append(f"{status.upper()} without named owner: {fn} / {art}")

if violations:
    print("\n".join(violations))
    sys.exit(1)
print(f"OK: {len(rows) - 1} rows, all green cells have evidence")
