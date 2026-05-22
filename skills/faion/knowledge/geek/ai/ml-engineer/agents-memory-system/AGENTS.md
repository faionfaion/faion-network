---
slug: agents-memory-system
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Three-tier agent memory: short-term buffer, episodic store, long-term vector store; with summarisation, eviction, and recall scoring.
content_id: "e9325a1ffb112e0b"
complexity: deep
produces: code
est_tokens: 4200
tags: [agents, memory, vector-store, context-management, embeddings]
---
# Agents Memory System

## Summary

**One-sentence:** Three-tier agent memory: short-term buffer, episodic store, long-term vector store; with summarisation, eviction, and recall scoring.

**One-paragraph:** Long-running agents overflow their context window without explicit memory management. This methodology defines a three-tier memory system: short-term (recent N turns, raw), episodic (per-session summary, structured), long-term (cross-session embeddings). Includes summarisation strategy (rolling summary every N turns), eviction policy (LRU on episodic), and recall scoring (BM25 + vector hybrid).

**Ефективно для:** Команд, що тримають агента live > 1 години і вже бачили, як він «забуває» через 50 turns; пора додати дисциплінований memory-стек.

## Applies If (ALL must hold)

- agent sessions run > 50 turns or > 1 hour
- context window exceeded in production at least once
- session continuity matters (the user returns and expects «remembering»)
- vector store is available for long-term storage
- summariser model is configured

## Skip If (ANY kills it)

- single-shot or short (< 10 turn) sessions — no memory needed
- context window is never the bottleneck — pure context handling suffices
- no privacy budget for cross-session storage — opt for ephemeral only
- compliance forbids storing user content (HIPAA / GDPR without consent)

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=code + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=code`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-agents-memory-system.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/memory-tiers.py` | Three-tier memory class skeleton |
| `templates/summariser.py` | Rolling summariser implementation |
| `templates/hybrid-recall.py` | Hybrid BM25 + vector recall |
| `templates/eviction-policy.py` | LRU + TTL eviction helpers |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agents-memory-system.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-three-tiers`, `r2-bounded-short-term`, `r3-rolling-summary`, `r4-hybrid-recall`, `r5-eviction-policy` from `content/01-core-rules.xml`.
