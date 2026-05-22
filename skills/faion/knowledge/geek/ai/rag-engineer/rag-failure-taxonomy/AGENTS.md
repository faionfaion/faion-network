---
slug: rag-failure-taxonomy
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a per-incident failure label from a closed RAG taxonomy: retrieval-fail / generation-fail / chunk-boundary / stale-doc / wrong-doc-ranked / prompt-leak.
content_id: "eba9e3039a371ddf"
complexity: light
produces: checklist
est_tokens: 2500
tags: [rag, failure-taxonomy, retrieval-quality, triage, weekly-review]
---
# RAG Failure Taxonomy

## Summary

**One-sentence:** Produces a per-incident failure label from a closed RAG taxonomy: retrieval-fail / generation-fail / chunk-boundary / stale-doc / wrong-doc-ranked / prompt-leak.

**One-paragraph:** A shared vocabulary for clustering RAG failure cases — retrieval-fail / generation-fail / chunk-boundary / stale-doc / wrong-doc-ranked / prompt-instruction-leak — so weekly retrieval-quality reviews and customer-feedback triage produce consistent diagnoses across reviewers. The output is a per-incident JSON record carrying the label, evidence, and a pointer to the failing query.

**Ефективно для:** тімам підтримки, які кластеризують RAG-провали у спільному словнику, щоб weekly review був стабільним між рев'юверами.

## Applies If (ALL must hold)

- Weekly retrieval-quality review meetings.
- Triage of customer feedback flagged as 'wrong answer'.
- Building dashboards that count failures by class.
- Building post-mortems for production quality incidents.

## Skip If (ANY kills it)

- Single-reviewer team where consistency is irrelevant.
- No production traffic to triage.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Failing query + answer + retrieved context | JSON | production logs |
| Ground-truth or human judgement | annotation | review |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/rag-engineer/rag-eval-production-monitoring` | Source of incident candidates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Apply taxonomy to incident | sonnet | Judgement + evidence. |
| Aggregate dashboard counts | haiku | Pure counting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/incident-form.md` | Per-incident triage form. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-failure-taxonomy.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[rag-eval-production-monitoring]]
- [[rag-eval-pipeline]]
- [[rag]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes each failing case to its primary label using observable evidence. Each leaf references a rule id from `01-core-rules.xml`.
