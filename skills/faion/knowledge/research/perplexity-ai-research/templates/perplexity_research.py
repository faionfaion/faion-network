# purpose: Runnable Perplexity batch caller
# consumes: inputs declared in AGENTS.md Prerequisites table
# produces: artefact conforming to content/02-output-contract.xml (perplexity-ai-research)
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~150-400 tokens when loaded as context
"""perplexity_research.py — batch Pro Search caller.

Set PPLX_API_KEY before running.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

PPLX_URL = "https://api.perplexity.ai/chat/completions"


def query(q: str, recency: str = "year") -> dict:
    api_key = os.environ.get("PPLX_API_KEY", "")
    if not api_key:
        raise RuntimeError("PPLX_API_KEY missing")
    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": q}],
        "search_recency_filter": recency,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        PPLX_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    out = [query(line.strip()) for line in sys.stdin if line.strip()]
    sys.stdout.write(json.dumps(out, indent=2))
