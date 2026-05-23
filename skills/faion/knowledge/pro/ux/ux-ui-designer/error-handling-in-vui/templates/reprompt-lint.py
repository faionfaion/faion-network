# purpose: Re-prompt ladder lint
# consumes: ladder JSON
# produces: lint report
# depends-on: stdlib only
# token-budget-impact: ~150
"""reprompt-lint.py — verify VUI re-prompt ladder discipline."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

def lint(ladder: list[str], require_examples_at: int | None) -> list[str]:
    errs: list[str] = []
    if len(set(ladder)) < len(ladder):
        errs.append("duplicate rung prompt — verbatim repeat is forbidden")
    if require_examples_at is not None and len(ladder) > require_examples_at:
        # rung 2 should mention "say" or examples
        if not re.search(r"\bsay\b|`[^`]+`", ladder[require_examples_at], re.I):
            errs.append("rung 2 missing example phrases")
    return errs

if __name__ == "__main__":
    spec = json.loads(Path(sys.argv[1]).read_text())
    errs = lint(spec.get("misrecognition_ladder", []), require_examples_at=1)
    errs += lint(spec.get("no_input_ladder", []), require_examples_at=None)
    for e in errs:
        sys.stderr.write(f"VIOLATION: {e}\n")
    sys.exit(0 if not errs else 1)
