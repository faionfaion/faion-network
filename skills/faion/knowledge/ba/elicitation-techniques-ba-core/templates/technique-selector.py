# purpose: CLI selector mapping (info_type, stakeholder_count) → technique.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env python3
"""technique-selector.py — map (info_type, stakeholder_count) to elicitation technique."""
from __future__ import annotations
import sys

MATRIX = {
    ('sme-deep', 1): 'interview', ('sme-deep', 2): 'interview', ('sme-deep', 3): 'interview',
    ('consensus-needs', 4): 'workshop', ('consensus-needs', 8): 'workshop',
    ('broad-preference', 15): 'survey', ('broad-preference', 100): 'survey',
    ('process-observe', 1): 'observation',
    ('artefact-analysis', 0): 'document-analysis',
}

def pick(info_type: str, count: int) -> str:
    for (it, n), tech in MATRIX.items():
        if it == info_type and count >= n: return tech
    return 'interview'

if __name__ == '__main__':
    print(pick(sys.argv[1], int(sys.argv[2])))
