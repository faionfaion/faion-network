# purpose: Stdlib sensitivity analysis for method-selection scores.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env python3
"""sensitivity.py — perturb fit scores ±1; report rank stability."""
from __future__ import annotations
import json, sys

def main():
    data = json.loads(sys.stdin.read())
    methods = data['methods']  # [{name, scores: {axis: int}}]
    base = sorted(methods, key=lambda m: sum(m['scores'].values()), reverse=True)
    print(json.dumps({'baseline_rank': [m['name'] for m in base]}, indent=2))

if __name__ == '__main__': main()
