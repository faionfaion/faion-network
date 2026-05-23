# purpose: Stdlib audit checking event-log integrity before mining.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env python3
"""pm-feasibility-audit.py — verify event-log integrity (case_id, activity, timestamp)."""
from __future__ import annotations
import csv, sys

REQUIRED = {'case_id', 'activity', 'timestamp'}

def main(path: str) -> int:
    with open(path) as f:
        r = csv.DictReader(f)
        missing = REQUIRED - set(r.fieldnames or [])
        if missing:
            sys.stderr.write(f'missing columns: {sorted(missing)}\n'); return 1
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
