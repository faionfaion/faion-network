# purpose: Pareto sweep skeleton for HNSW M × ef_search × quantization
# consumes: query workload + corpus snapshot
# produces: code (drop-in bench tool emitting tuning-history.yaml row)
# depends-on: qdrant-client / pgvector psycopg + numpy + scipy
# token-budget-impact: ~200 tokens if loaded into LLM context
"""Pareto sweep skeleton for HNSW M × ef_search × quantization."""
from __future__ import annotations

import time
import statistics


def bench_one(client, collection, queries, ground_truth, k: int = 10) -> dict:
    """Run queries, return recall@k + latency stats."""
    latencies = []
    hits = 0
    for q, expected in zip(queries, ground_truth):
        t0 = time.perf_counter()
        results = client.search(collection_name=collection, query_vector=q, limit=k)
        latencies.append((time.perf_counter() - t0) * 1000)
        ids = {r.id for r in results}
        hits += len(ids & set(expected)) / len(expected)
    return {
        "recall_at_k": hits / len(queries),
        "latency_p50_ms": statistics.median(latencies),
        "latency_p95_ms": sorted(latencies)[int(0.95 * len(latencies))],
    }


def sweep(client, collection, queries, ground_truth,
          m_values=(16, 32, 64),
          ef_values=(32, 64, 128, 200)) -> list[dict]:
    rows = []
    for m in m_values:
        # NOTE: in real bench, rebuild index per M; this is the skeleton
        for ef in ef_values:
            client.update_collection(collection_name=collection, hnsw_config={"ef": ef})
            r = bench_one(client, collection, queries, ground_truth)
            rows.append({"m": m, "ef_search": ef, **r})
    return rows
