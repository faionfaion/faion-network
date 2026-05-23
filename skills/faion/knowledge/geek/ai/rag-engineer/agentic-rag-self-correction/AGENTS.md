---
slug: agentic-rag-self-correction
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates an answer, runs a faithfulness verifier (different model) against retrieved chunks, regenerates with feedback up to a hard cap, escalates if ungrounded claims persist.
content_id: "69b136f8e2d0c44d"
complexity: deep
produces: code
est_tokens: 3700
tags: [rag, agentic, self-correction, faithfulness, hallucination]
---
# Agentic RAG — Self-Correction Loop

## Summary

**One-sentence:** Generates an answer, runs a faithfulness verifier (different model) against retrieved chunks, regenerates with feedback up to a hard cap, escalates if ungrounded claims persist.

**One-paragraph:** Generators hallucinate even on grounded RAG context. This methodology wraps any RAG agent with a self-correction loop: generate → verify faithfulness against the same retrieved chunks via a DIFFERENT model → if &gt;2 ungrounded claims, regenerate with feedback. Cap at `max_corrections` (default 2). On cap reached without verified answer, escalate to human review with full iteration trace.

**Ефективно для:**

- RAG features де hallucination > 3% — потрібен safety net.
- Mandatory verifier (different model than generator) — break confirmation bias.
- Trace всі iterations для post-mortem.
- Hard cap на корекції — uncapped loops drift.
- Bridge with `[[agentic-rag-iterative-retrieval]]` — verifier is the gate.

## Applies If (ALL must hold)

- Hallucination rate &gt;3% on baseline RAG eval.
- Verifier model available distinct from generator.
- Cost budget allows N × verifier calls per query.
- Audit-trace pipeline downstream.

## Skip If (ANY kills it)

- Hallucination rate &lt;1% (overhead exceeds gain).
- Only one model available (no distinct verifier).
- Strict latency &lt;2s SLA — self-correct adds 1–3s.
- No audit-trace consumer.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Generator model client | provider client | platform |
| Verifier model client (different from generator) | provider client | platform |
| Faithfulness prompt template | text | service repo |
| Audit log writer | python | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[agentic-rag-iterative-retrieval]]` | Companion methodology — verifier gates iterative loop. |
| `[[prompt-pr-review-checklist]]` | Per-prompt-PR review of the faithfulness prompt. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 2 rules + run/skip terminals | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for self-correction-config | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with detector + repair | ~700 |
| `content/04-procedure.xml` | essential | 5-step: pick verifier → generate → verify → regenerate → escalate | ~700 |
| `content/06-decision-tree.xml` | essential | Routes hallucination rate + verifier availability to self-correct vs vanilla | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `faithfulness-verifier` | sonnet | Different from generator (rule r1); reasoning fits sonnet. |
| `regenerate-with-feedback` | opus | Generator stays on opus. |

## Templates

| File | Purpose |
|------|---------|
| `templates/self_correction_loop.py` | SelfCorrectionLoop class. |
| `templates/self-correction-config.json` | Config skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-rag-self-correction.py` | Validate self-correction-config | Pre-commit + CI |

## Related

- [[agentic-rag-iterative-retrieval]]
- [[agentic-rag-query-decomposition]]
- [[rag-bench-harness-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on baseline hallucination rate + verifier availability + latency budget. Walk before wiring.
