---
slug: adr-ai-drafted-with-review
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Drafts an ADR via LLM from a decision-context bundle, then routes through a mandatory human-review gate with named approver before commit.
content_id: "7d98ee81143e6cfd"
complexity: medium
produces: decision-record
est_tokens: 3400
tags: ["adr", "sdlc-ai", "ai-drafted", "human-review", "decision"]
---
# ADR AI-Drafted With Review

## Summary

**One-sentence:** Drafts an ADR via LLM from a decision-context bundle, then routes through a mandatory human-review gate with named approver before commit.

**One-paragraph:** ADR AI-Drafted With Review produces a decision-record that fixes a recurring decision in the sdlc-ai domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Швидкий чорновий ADR з context bundle.
- Named approver gate — LLM не комітить ADR сам.
- Audit trail: коли LLM драфтував, коли людина approve.
- Cost-control: tokenization budget per ADR.
- Onboarding: junior бачить шаблон ADR + workflow.

## Applies If (ALL must hold)

- Team accepts AI-drafted ADRs as input.
- Named approver workflow exists or can be established.
- Decision context bundle (related ADRs, code refs) can be assembled within token budget.

## Skip If (ANY kills it)

- Team rejects AI-drafted decision records.
- No named approver available within decision window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision context bundle | Markdown + code refs | architect |
| Approver roster | YAML | tech lead |
| ADR template | Markdown | faion-network |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[adr-consequence-evidence-binding]] | AI drafts using evidence-binding shape |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-adr-ai-drafted-with-review` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ADR-AI-template.md` | ADR skeleton with AI-attribution frontmatter + approver field |
| `templates/ai-adr-prompt.md` | LLM prompt template for ADR drafting |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-adr-ai-drafted-with-review.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[adr-consequence-evidence-binding]]
- [[adr-supersession-detection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
