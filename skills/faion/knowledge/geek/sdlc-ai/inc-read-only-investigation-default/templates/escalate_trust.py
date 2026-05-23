# purpose: Trust ratchet manager
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-500 tokens when loaded as context

#!/usr/bin/env python3
# purpose: trust ratchet manager — records first authorised write per action class
# consumes: audit log + signed approval
# produces: ratchet entry
# depends-on: scripts/validate-inc-read-only-investigation-default.py
# token-budget-impact: ~250 tokens
"""Record agent write authorisations to trust ratchet."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def record(action_class: str, agent_id: str, approver: str, evidence_url: str, log_path: Path) -> None:
    entry = {"action_class": action_class, "agent_id": agent_id, "approver": approver, "evidence_url": evidence_url, "ts": "auto"}
    existing = []
    if log_path.exists():
        existing = json.loads(log_path.read_text())
    existing.append(entry)
    log_path.write_text(json.dumps(existing, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.stderr.write("usage: escalate_trust.py <action_class> <agent_id> <approver> <evidence_url> <log_path>\n")
        sys.exit(2)
    record(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], Path(sys.argv[5]))
