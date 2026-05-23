# purpose: Stdlib RTM generator that scans repo for req-ID mentions.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env python3
"""rtm_min.py — scan repo for requirement-ID mentions, emit RTM JSON."""
from __future__ import annotations
import json, pathlib, re, sys

REQ_RE = re.compile(r'\bREQ-[A-Z0-9-]+\b')

def main(root: str) -> int:
    rtm: dict[str, list[str]] = {}
    for p in pathlib.Path(root).rglob('*'):
        if not p.is_file() or p.suffix not in {'.md', '.ts', '.py', '.js'}: continue
        try: txt = p.read_text(errors='ignore')
        except Exception: continue
        for m in REQ_RE.finditer(txt):
            rtm.setdefault(m.group(0), []).append(str(p))
    print(json.dumps(rtm, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
