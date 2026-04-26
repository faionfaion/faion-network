#!/usr/bin/env bash
# market-risk-lint.sh — enforce citations from market-research files on every register row.
# Usage: market-risk-lint.sh .aidocs/product_docs/market-risk-register.md
# Exit code: 0 = OK, 1 = FAIL (prints violations to stdout)
set -euo pipefail
file="${1:?usage: market-risk-lint.sh REGISTER.md}"
docs_dir="$(dirname "$file")"
python3 - "$file" "$docs_dir" <<'PY'
import re, sys, pathlib
reg = pathlib.Path(sys.argv[1]).read_text()
docs = sys.argv[2]
allowed = {
    "market-research.md", "competitive-analysis.md",
    "pricing-research.md", "trend-analysis.md", "niche-evaluation.md"
}
sub_cats = {"demand", "competition", "pricing", "trend", "channel"}
errs = []

# Match rows like: | demand-001 | Risk text | demand | H | H | 9 | citation | ...
row_re = re.compile(
    r"^\|\s*([\w-]+)\s*\|[^|]+\|\s*([\w-]+)\s*\|\s*[HML]\s*\|\s*[HML]\s*\|\s*\d+\s*\|([^|]+)\|",
    re.MULTILINE,
)
for m in row_re.finditer(reg):
    rid = m.group(1).strip()
    cat = m.group(2).strip().lower()
    citation = m.group(3).strip()
    if not any(c in cat for c in sub_cats):
        errs.append(f"{rid}: sub-category '{cat}' not in {sorted(sub_cats)}")
    cited_files = [d for d in allowed if d in citation]
    if not cited_files:
        errs.append(f"{rid}: citation '{citation}' does not reference any of {sorted(allowed)}")
    else:
        for d in cited_files:
            if not (pathlib.Path(docs) / d).exists():
                errs.append(f"{rid}: cites missing file '{d}' in {docs}")

if errs:
    print("FAIL")
    for e in errs:
        print(" -", e)
    sys.exit(1)

print(f"OK: {sum(1 for _ in row_re.finditer(reg))} rows, all cite an existing market research doc")
PY
