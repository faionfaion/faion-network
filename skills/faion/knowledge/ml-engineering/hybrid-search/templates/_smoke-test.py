"""_smoke-test.py.
purpose: bench harness skeleton
consumes: held-out queries JSONL + labels
produces: hybrid-search-config.json metrics
depends-on: qdrant-client; stdlib
token-budget-impact: +100t.
"""
from __future__ import annotations

import json
import time
from pathlib import Path


def main() -> None:
    queries = [json.loads(l) for l in Path("queries.jsonl").read_text().splitlines() if l.strip()]
    hits = 0
    latencies: list[float] = []
    for q in queries:
        t0 = time.perf_counter()
        # results = hybrid_search(client, ...)
        results: list[dict] = []
        latencies.append((time.perf_counter() - t0) * 1000)
        if any(r["id"] in q["relevant_ids"] for r in results[:10]):
            hits += 1
    p_at_10 = hits / max(1, len(queries))
    latencies.sort()
    p99 = latencies[int(0.99 * (len(latencies) - 1))] if latencies else 0.0
    print(json.dumps({"precision_at_10": p_at_10, "p99_latency_ms": p99}, indent=2))


if __name__ == "__main__":
    main()
