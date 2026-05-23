# purpose: drift monitor for the preference-trained-router methodology
# consumes: current window route distribution + reference window
# produces: KL divergence + structured alert on threshold breach
# depends-on: r5-drift-monitor
# token-budget-impact: ~200 tokens
"""Daily drift check for a preference-trained router.

Compares the current-window routing distribution to a stable reference
window via KL divergence; emits a structured alert when the divergence
crosses the configured threshold.

Input  → JSONL log with one record per request: {"route": "weak"|"strong"}
Output → exit 0 (OK) or exit 1 (alert) plus a one-line JSON summary on stdout.
"""

import json
import math
import sys
from collections import Counter
from pathlib import Path

KL_THRESHOLD = 0.10  # tune per workload


def distribution(path: Path) -> dict[str, float]:
    counts: Counter[str] = Counter()
    with path.open() as fh:
        for line in fh:
            counts[json.loads(line)["route"]] += 1
    total = sum(counts.values()) or 1
    return {k: v / total for k, v in counts.items()}


def kl(p: dict[str, float], q: dict[str, float]) -> float:
    keys = set(p) | set(q)
    out = 0.0
    for k in keys:
        pk = max(p.get(k, 1e-9), 1e-9)
        qk = max(q.get(k, 1e-9), 1e-9)
        out += pk * math.log(pk / qk)
    return out


def main(reference: str, current: str) -> int:
    p = distribution(Path(reference))
    q = distribution(Path(current))
    d = kl(p, q)
    summary = {"kl": round(d, 4), "ref": p, "cur": q}
    sys.stdout.write(json.dumps(summary) + "\n")
    return 0 if d < KL_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
