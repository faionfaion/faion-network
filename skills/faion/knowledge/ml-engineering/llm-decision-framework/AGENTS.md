# LLM Decision Framework

## Summary

**One-sentence:** Produces an LLM-strategy ADR choosing prompt-engineering / RAG / fine-tuning / RAFT-hybrid against scored constraints (data freshness, accuracy, budget, latency, team).

**One-paragraph:** Produces an LLM-strategy ADR. Systematic framework for choosing the right LLM enhancement strategy — prompt engineering, RAG, fine-tuning, or RAFT (hybrid) — based on data freshness, accuracy requirements, budget, latency, and team constraints. Always score prompting first before investing in retrieval or training infrastructure; capture the score sheet in the ADR for auditable reversal later.

**Ефективно для:** ML лід на старті проекту — fixed ADR з оцінкою prompt/RAG/FT/RAFT, не давати рішенню затягтись хайпом.

## Applies If (ALL must hold)

- Starting a new LLM-powered feature OR re-evaluating an existing one.
- Choice between prompt-only, RAG, fine-tune, RAFT (RAG + fine-tune) is genuinely open.
- Stakeholders disagree on path — need an evidence-anchored decision.
- Org wants an auditable decision record for compliance / hiring / audit.
- Budget envelope known (one-off $ + recurring $/month).

## Skip If (ANY kills it)

- Decision already made and committed — skip; redo on material change.
- Single trivial feature with no recurring cost — over-engineering.
- Pre-revenue prototype phase — score lightly, revisit at growth.
- Constraints unstable (target moves weekly) — not enough signal to commit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case description | markdown | product |
| Constraints sheet (accuracy/freshness/latency/budget) | yaml | ML lead |
| Team skill inventory | markdown | engineering manager |
| Sample queries | jsonl | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/finetuning` | Downstream for fine-tune branch. |
| `geek/ai/ml-engineer/llamaindex` | Downstream for RAG branch. |
| `geek/ai/ml-engineer/cost-optimization` | Cost-scoring inputs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: gather-constraints → score-prompting → score-rag → score-ft → pick-and-write-adr. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by accuracy / freshness / budget / latency. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-prompting` | sonnet | Run prompting baseline on sample queries; record metric. |
| `score-rag` | sonnet | Stand up cheap RAG; score same queries. |
| `write-adr` | opus | Cross-cutting synthesis; surface real trade-offs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr.md` | ADR skeleton with score sheet + alternatives + consequences. |
| `templates/decision-matrix.py` | Score → recommendation calculator. |
| `templates/prompt-requirements.txt` | Constraint-elicitation prompt. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-decision-framework.py` | Validate the ADR (scores per option, chosen, rationale, alternatives). | Pre-merge of every LLM ADR PR. |

## Related

- [[finetuning]] — downstream when FT chosen.
- [[llamaindex]] — downstream when RAG chosen.
- [[cost-optimization]] — input to budget scoring.

## Decision tree

Decision tree at `content/06-decision-tree.xml` walks (accuracy gap, data freshness, budget, latency, team skill) and lands on prompt / RAG / FT / RAFT.
