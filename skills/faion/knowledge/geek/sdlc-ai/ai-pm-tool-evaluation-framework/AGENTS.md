---
slug: ai-pm-tool-evaluation-framework
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Scoring framework for evaluating AI-assisted PM tools (Linear/Jira/Notion AI add-ons) on 8 dimensions: data residency, hallucination rate, tracker fidelity, cost, vendor lock, etc.
content_id: "e7f749a1dac93b6c"
complexity: medium
produces: rubric
est_tokens: 4400
tags: [pm-tools, evaluation, ai-procurement, rubric, sdlc-ai]
---
# AI PM Tool Evaluation Framework

## Summary

**One-sentence:** Scoring framework for evaluating AI-assisted PM tools (Linear/Jira/Notion AI add-ons) on 8 dimensions: data residency, hallucination rate, tracker fidelity, cost, vendor lock, etc.

**One-paragraph:** PM tool vendors are racing to bolt AI features onto Linear, Jira, Notion, Asana, ClickUp. Buying decisions need a deterministic rubric — not vendor demos. This methodology defines an 8-axis scorecard (data residency, hallucination rate measured on a fixture set, tracker fidelity, cost per user-month, vendor lock-in / export, prompt-injection surface, audit-log completeness, integration depth) with weighted scoring and a pass/fail threshold per axis. Output is a JSON scorecard per vendor, comparable side-by-side, that a buyer can defend in procurement review.

**Ефективно для:**

- The team is evaluating one or more AI-augmented PM SaaS tools for procurement.
- Procurement requires a written justification (not a single-vendor pilot).
- The decision impacts ≥5 users and binds the team for ≥6 months.

## Applies If (ALL must hold)

- The team is evaluating one or more AI-augmented PM SaaS tools for procurement.
- Procurement requires a written justification (not a single-vendor pilot).
- The decision impacts ≥5 users and binds the team for ≥6 months.

## Skip If (ANY kills it)

- Single-developer trial with no procurement gate.
- Vendor is already mandated by enterprise IT (no choice to evaluate).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Vendor shortlist | yaml | RFP intake |
| Fixture issue corpus | json | Internal — anonymised real-issue sample, ≥50 items |
| Cost model | yaml | Finance — seat counts, growth |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-pm-tool-evaluation-framework` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scorecard.json` | Per-vendor scorecard skeleton |
| `templates/comparison.md` | Side-by-side vendor comparison narrative |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pm-tool-evaluation-framework.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
