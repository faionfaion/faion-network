#!/usr/bin/env bash
# riskreg.sh — sort risk register by score, lint missing fields and mitigations.
# Usage: riskreg.sh path/to/risk-register.md
# Output: sorted risk table + lint errors (exits 1 if errors found)
set -euo pipefail
file="${1:?usage: riskreg.sh REGISTER.md}"
python3 - "$file" <<'PY'
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
score = {"H": 3, "M": 2, "L": 1}
rows, errs = [], []
row_re = re.compile(
    r"^\|\s*(R\d+)\s*\|([^|]+)\|([^|]+)\|\s*([HML])\s*\|\s*([HML])\s*\|\s*\d*\s*\|([^|]*)\|",
    re.M,
)
for m in row_re.finditer(src):
    rid, risk, cat, p, i, status = (s.strip() for s in m.groups())
    s = score[p] * score[i]
    rows.append((s, rid, risk, cat, p, i, status))
    if not status:
        errs.append(f"{rid}: missing status")
    if s >= 6 and "mitigat" not in src.lower().split(rid, 1)[-1][:600]:
        errs.append(f"{rid}: high score {s} without 'mitigation' nearby")
rows.sort(reverse=True)
print(f"# Risk Register — sorted ({len(rows)} risks)\n")
print("| Score | ID | Risk | Cat | P | I | Status |")
print("|------:|----|------|-----|---|---|--------|")
for s, rid, risk, cat, p, i, st in rows:
    print(f"| {s} | {rid} | {risk} | {cat} | {p} | {i} | {st} |")
if errs:
    print("\n## Lint errors")
    for e in errs:
        print("-", e)
    sys.exit(1)
PY
