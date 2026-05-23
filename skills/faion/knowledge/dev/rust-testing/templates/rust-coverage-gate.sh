# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

#!/usr/bin/env bash
# rust-coverage-gate.sh — enforce line + branch coverage thresholds.
# Usage: rust-coverage-gate.sh LINE_PCT BRANCH_PCT
# Example: rust-coverage-gate.sh 70 60
set -euo pipefail
LINE="${1:-70}"
BRANCH="${2:-60}"

cargo llvm-cov --workspace --lcov --output-path lcov.info >/dev/null

python3 - "$LINE" "$BRANCH" <<'PY'
import re, sys
line_t, branch_t = float(sys.argv[1]), float(sys.argv[2])
with open("lcov.info") as f:
    data = f.read()
lf = sum(int(x) for x in re.findall(r"^LF:(\d+)", data, re.M))
lh = sum(int(x) for x in re.findall(r"^LH:(\d+)", data, re.M))
bf = sum(int(x) for x in re.findall(r"^BRF:(\d+)", data, re.M))
bh = sum(int(x) for x in re.findall(r"^BRH:(\d+)", data, re.M))
line = (lh / lf * 100) if lf else 100.0
branch = (bh / bf * 100) if bf else 100.0
print(f"line={line:.1f}% branch={branch:.1f}%")
fails = []
if line < line_t:   fails.append(f"line {line:.1f}% < {line_t}%")
if branch < branch_t: fails.append(f"branch {branch:.1f}% < {branch_t}%")
if fails:
    print("FAIL:", "; ".join(fails))
    sys.exit(1)
print("OK")
PY
