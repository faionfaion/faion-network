# purpose: Reference runbook parser
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-500 tokens when loaded as context

#!/usr/bin/env python3
# purpose: parse tagged-step runbook markdown into JSON step list
# consumes: runbook markdown
# produces: JSON step list
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~250 tokens
"""Parse markdown runbook into structured steps."""
from __future__ import annotations
import re
import json
import sys
from pathlib import Path

STEP_RE = re.compile(r"^### `\[(?P<tag>read|write|approval-required|verify|wait)\]` id=(?P<id>[a-z0-9-]+)\s*$")


def parse(md_path: Path) -> list[dict]:
    steps: list[dict] = []
    current: dict | None = None
    in_code = False
    for line in md_path.read_text().splitlines():
        m = STEP_RE.match(line)
        if m:
            if current:
                steps.append(current)
            current = {"id": m["id"], "tag": m["tag"], "command": ""}
            continue
        if current is None:
            continue
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            current["command"] += line + "\n"
        elif line.startswith("assertion:"):
            current["assertion"] = line.split(":", 1)[1].strip(" `")
    if current:
        steps.append(current)
    return steps


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("usage: parser.py <runbook.md>\n")
        sys.exit(2)
    print(json.dumps(parse(Path(sys.argv[1])), indent=2))
