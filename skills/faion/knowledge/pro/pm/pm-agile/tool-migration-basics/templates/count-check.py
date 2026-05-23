# purpose: Pre/post count-check script to verify no rows lost
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env python3
"""count-check.py — compare source vs target issue counts after migration.

Exit 0 if drift is within threshold (default 1%), exit 1 otherwise.

Usage:
    JIRA_URL=https://myorg.atlassian.net JIRA_TOKEN=<token> \\
    LINEAR_TOKEN=<token> \\
        python3 count-check.py [--threshold 0.01]

Customize SOURCE_COUNT and TARGET_COUNT functions for your tool pair.
"""
from __future__ import annotations

import argparse
import os
import sys

import requests


def source_count() -> int:
    """Count all issues in the Jira source project."""
    base = os.environ["JIRA_URL"].rstrip("/")
    token = os.environ["JIRA_TOKEN"]
    r = requests.get(
        f"{base}/rest/api/3/search",
        params={"jql": "project = PROJ", "maxResults": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    r.raise_for_status()
    return r.json()["total"]


def target_count() -> int:
    """Count all issues in the Linear target team."""
    token = os.environ["LINEAR_TOKEN"]
    query = '{ issues(filter:{team:{key:{eq:"ABC"}}}) { totalCount } }'
    r = requests.post(
        "https://api.linear.app/graphql",
        json={"query": query},
        headers={"Authorization": token},
    )
    r.raise_for_status()
    return r.json()["data"]["issues"]["totalCount"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.01, help="Max allowed drift (default 1%%)")
    args = ap.parse_args()

    src = source_count()
    tgt = target_count()
    drift = abs(src - tgt) / max(src, 1)

    print(f"source={src}  target={tgt}  drift={drift:.2%}  threshold={args.threshold:.2%}")

    if drift > args.threshold:
        print(f"FAIL: drift {drift:.2%} exceeds threshold {args.threshold:.2%}")
        return 1

    print("PASS: counts within threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
