# RAG A/B Testing Framework

## Summary

**One-sentence:** Runs an interleaved A/B test of two RAG configurations on a shared question set and reports per-config metrics with a promote/reject recommendation.

**One-paragraph:** A/B testing for RAG configurations runs the same question set through two pipeline variants and compares their results. The baseline framework measures latency and source count; a full quality comparison requires integrating the RAGAS evaluation loop per configuration. Use A/B testing to validate parameter changes (chunk size, embedding model, top-K, reranker) before promoting config B to production.

**Ефективно для:** команд, які хочуть перевірити config-зміну (chunk size, embedding model, reranker) до промоушн в production.

## Applies If (ALL must hold)

- Comparing different chunk sizes for the same corpus.
- Evaluating the impact of adding or swapping a reranker model.
- Comparing embedding models (e.g., text-embedding-3-large vs voyage-3).
- Validating any config parameter change before promoting it to production.

## Skip If (ANY kills it)

- Test set has &lt;20 questions — differences are within statistical noise.
- The two configurations are not isolated (share index state or caches).
- Only latency matters and quality is irrelevant — just benchmark directly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Config A | YAML | current prod |
| Config B | YAML | candidate |
| Shared test set | JSONL {query, ground_truth} | rag-eval-test-set-generation |
| RAGAS judge | LLM credentials | env |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-pipeline` | Provides the per-config eval runner. |
| `geek/ai/rag-engineer/rag-eval-strategy` | Defines numeric quality gates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: interleave A/B, isolate state, ≥20 questions, paired stats, quality &gt; latency | ~800 |
| `content/02-output-contract.xml` | essential | JSON schema for AB report | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: non-interleaved batches, latency-only signal, leak via shared cache | ~700 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Tree for promote/reject/run-more | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Run interleaved trials | haiku | Mechanical. |
| Compute paired metrics | haiku | Pure arithmetic. |
| Write promotion recommendation | sonnet | Trade-off framing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ab-runner.py.tmpl` | Interleaved runner that fires A and B per question. |
| `templates/ab-report.md.tmpl` | Report skeleton with per-config metrics and recommendation. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-eval-ab-testing.py` | Validates AB report JSON. | Pre-commit; CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-eval-pipeline]]
- [[rag-eval-strategy]]
- [[rag-eval-test-set-generation]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides promotion: root question — "Is the per-question paired difference between A and B statistically significant (p&lt;0.05)?". Branches lead to promote-B, keep-A, or "run more trials". Each leaf references a rule.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ab-runner.py.tmpl`

```python
from statistics import mean
from typing import Callable, List, Dict


def run_ab(
    pipeline_a: Callable[[str], Dict],
    pipeline_b: Callable[[str], Dict],
    judge: Callable[[str, Dict], float],
    questions: List[Dict],
) -> Dict:
    assert len(questions) >= 20, "need >=20 questions"
    per_q = []
    for q in questions:
        ra = pipeline_a(q["query"])
        rb = pipeline_b(q["query"])
        a_score = judge(q["query"], ra)
        b_score = judge(q["query"], rb)
        per_q.append({"query": q["query"], "a_score": a_score, "b_score": b_score, "delta": b_score - a_score,
                      "a_latency_ms": ra.get("latency_ms", 0.0), "b_latency_ms": rb.get("latency_ms", 0.0)})
    a_lat = sorted(p["a_latency_ms"] for p in per_q)
    b_lat = sorted(p["b_latency_ms"] for p in per_q)
    p95 = lambda xs: xs[int(0.95 * (len(xs) - 1))] if xs else 0.0
    p_value = _paired_p([p["a_score"] for p in per_q], [p["b_score"] for p in per_q])
    a_mean = mean(p["a_score"] for p in per_q)
    b_mean = mean(p["b_score"] for p in per_q)
    if p_value < 0.05 and b_mean > a_mean and p95(b_lat) <= p95(a_lat) * 1.2:
        rec = "promote-b"
    elif p_value < 0.05 and b_mean < a_mean:
        rec = "keep-a"
    elif p_value >= 0.05 and len(questions) < 100:
        rec = "run-more"
    else:
        rec = "keep-a"
    return {"n_questions": len(questions), "per_question": per_q,
            "aggregate": {"a_mean": a_mean, "b_mean": b_mean, "p_value": p_value,
                          "a_latency_p95_ms": p95(a_lat), "b_latency_p95_ms": p95(b_lat)},
            "recommendation": rec}


def _paired_p(a, b):
    diffs = [bi - ai for ai, bi in zip(a, b)]
    n = len(diffs)
    if n < 2:
        return 1.0
    mu = sum(diffs) / n
    var = sum((d - mu) ** 2 for d in diffs) / (n - 1)
    if var == 0:
        return 0.0 if mu != 0 else 1.0
    se = (var / n) ** 0.5
    z = mu / se
    # Rough two-sided normal approximation; for production use scipy.stats.ttest_rel
    from math import erf, sqrt
    return 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
```

### `templates/ab-report.md.tmpl`

```markdown
# RAG A/B Report — <config_a> vs <config_b>

Date: YYYY-MM-DD
Owner: <name>
N questions: <int>

## Aggregate
- Metric: <faithfulness | mrr | ndcg>
- A mean: <x>   B mean: <y>   p-value: <p>
- A p95 latency: <a_ms>   B p95 latency: <b_ms>

## Recommendation
- promote-b | keep-a | run-more

## Per-question deltas (top regressions / wins)
- worst: q="..." A=.. B=.. Δ=-..
- best:  q="..." A=.. B=.. Δ=+..
```
