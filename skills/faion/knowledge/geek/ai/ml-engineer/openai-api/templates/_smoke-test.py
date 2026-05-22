# purpose: smoke-test fixture for openai-api
# consumes: none
# produces: minimum-viable filled-in payload
# depends-on: content/02-output-contract.xml
# token-budget-impact: tiny

"""openai-api smoke-test fixture — minimum viable filled-in instance."""
from __future__ import annotations

SMOKE = {
    "slug": "openai-api",
    "version": "1.0.0",
    "date": "2026-05-22",
    "produces": "code",
    "payload": {
        "language": "python",
        "entry_point": "skeleton.py",
        "files": [{"path": "skeleton.py", "purpose": "main module"}],
    },
    "forbidden_seen": [],
}
