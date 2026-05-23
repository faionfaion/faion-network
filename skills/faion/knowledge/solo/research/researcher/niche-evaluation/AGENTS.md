---
slug: niche-evaluation
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Researcher-tier niche evaluation: definition + TAM/SAM/SOM + competitor matrix + audience + monetization + fit, biased to research-anchored inputs over sizing-by-feel."
content_id: "048488d030522580"
complexity: medium
produces: report
est_tokens: 4700
tags: [niche, evaluation, research, market-sizing, validation]
---
# Niche Evaluation (Researcher)

## Summary

**One-sentence:** Researcher-tier niche evaluation: definition + TAM/SAM/SOM + competitor matrix + audience + monetization + fit, biased to research-anchored inputs over sizing-by-feel.

**One-paragraph:** Mirror of the market-researcher tier but for researchers anchoring on interview / behavioural evidence. Pins the six-step report (niche formula → cited sizing → competitor matrix → accessibility → monetization → fit) but adds an evidence-link requirement per step: each row must cite an interview / behavioural signal / public report. Output: a niche-evaluation report with a single GO / PASS / PIVOT verdict.

**Ефективно для:**

- Researcher evaluating a niche identified from JTBD interviews.
- Solo operator who already runs niche-evaluation but lacks the research bias.
- PM cross-checking a market-researcher report with research evidence.
- Founder pre-MVP wanting research-anchored niche sizing.

## Applies If (ALL must hold)

- Candidate niche defined.
- ≥3 interviews in the niche cohort.
- ≥2 named industry sources reachable.
- Operator has ≥2 focused hours per niche.

## Skip If (ANY kills it)

- Niche undefined — run idea-generation first.
- <3 interviews — collect more before evaluation.
- Operator wants intuition-driven choice — methodology cannot help.
- Three previous evaluations failed and operator is fatigued — change methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Niche definition | [audience] who do [job] when [trigger] | ideation output |
| Interview corpus in niche | ≥3 interviews tagged | research repo |
| Industry sources | URLs to reports / public data | research |
| Competitor list with evidence | csv + screenshots | competitor scan |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/niche-evaluation` | shared six-step engine; this tier adds evidence-link discipline |
| `solo/research/researcher/jobs-to-be-done` | JTBD output feeds niche definition |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-niche-evaluation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/niche-evaluation.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/niche-evaluation.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-niche-evaluation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[jobs-to-be-done]]`
- `[[pain-point-research]]`
- `[[problem-validation]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
