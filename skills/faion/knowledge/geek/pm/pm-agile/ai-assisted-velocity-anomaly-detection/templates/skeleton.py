#!/usr/bin/env python3
# purpose: Python skeleton: pull velocity + PR metrics, compute z-scores against baseline, emit anomaly JSON.
# consumes: methodology inputs listed in AGENTS.md `## Prerequisites`
# produces: a filled artefact matching the JSON Schema in content/02-output-contract.xml
# depends-on: templates/header.yaml for frontmatter contract; AGENTS.md for body sections
# token-budget-impact: ~500-900 tokens to fill end-to-end; ~200 to validate
"""Methodology scaffold — fill the gaps in `produce()` and pipe to scripts/validate-<slug>.py."""
from __future__ import annotations

import json
from datetime import date


def produce() -> dict:
    return {
        "header": {
            "version": "0.1.0",
            "owner": "<role>:<person>",
            "last_reviewed": date.today().isoformat(),
        },
        "body": {},
        "evidence": [],
        "decisions": {"next_actions": [], "next_review": "YYYY-MM-DD"},
    }


if __name__ == "__main__":
    print(json.dumps(produce(), indent=2))  # noqa: T201
