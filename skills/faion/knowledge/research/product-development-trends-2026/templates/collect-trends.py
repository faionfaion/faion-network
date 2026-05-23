# purpose: Pull 2026 source signals with freshness gate
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
#!/usr/bin/env python3
"""
collect-trends.py — collect 2025-2026 trend evidence per axis using Exa.ai.

Usage: EXA_API_KEY=<key> python collect-trends.py [output.jsonl]

Output: JSONL where each line is:
  {"axis": str, "title": str, "url": str, "published": str, "score": float}

Requires: EXA_API_KEY environment variable.
Install: pip install requests (stdlib urllib used to avoid extra deps)
"""
import json
import os
import sys
import urllib.request

AXES = [
    "ai-augmented-ideation product development",
    "continuous-discovery product team cadence",
    "rapid-pivot product strategy quarterly",
    "cross-functional product team structure",
]

EXA_URL = "https://api.exa.ai/search"
KEY = os.environ.get("EXA_API_KEY", "")


def fetch_axis(axis: str) -> list[dict]:
    if not KEY:
        raise RuntimeError("EXA_API_KEY environment variable not set")
    body = json.dumps({
        "query": f"{axis} 2025 OR 2026",
        "num_results": 8,
        "start_published_date": "2025-01-01",
        "use_autoprompt": True,
    }).encode()
    req = urllib.request.Request(
        EXA_URL,
        data=body,
        headers={"x-api-key": KEY, "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    return [
        {
            "axis": axis,
            "title": x.get("title", ""),
            "url": x.get("url", ""),
            "published": x.get("publishedDate", ""),
            "score": float(x.get("score", 0)),
        }
        for x in data.get("results", [])
    ]


def main() -> int:
    out_path = sys.argv[1] if len(sys.argv) > 1 else "trends.jsonl"
    total = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for axis in AXES:
            try:
                results = fetch_axis(axis)
                for row in results:
                    f.write(json.dumps(row) + "\n")
                    total += 1
                print(f"axis '{axis}': {len(results)} results", file=sys.stderr)
            except Exception as exc:
                print(f"ERROR axis '{axis}': {exc}", file=sys.stderr)
    print(f"Wrote {total} signals to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
