---
slug: sdd-promotion-gate-checklist
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a binary-pass checklist that gates feature promotion from `backlog/` → `todo/` in the SDD lifecycle, replacing gut-feel approval.
content_id: "c5ab052722ee3fe2"
complexity: medium
produces: checklist
est_tokens: 3400
tags: ["sdd", "promotion", "gate", "checklist", "backlog"]
---
# SDD Promotion Gate Checklist

## Summary

**One-sentence:** Produces a binary-pass checklist that gates feature promotion from `backlog/` → `todo/` in the SDD lifecycle, replacing gut-feel approval.

**One-paragraph:** SDD Promotion Gate Checklist produces a checklist that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Gate backlog→todo: тільки після binary-pass checklist.
- Reviewer onboarding: чіткий критерій, не gut-feel.
- Async approvals: reviewer заповнює галочки без зустрічі.
- Audit/compliance: evidence коли і чому фіча промотована.
- Velocity hygiene: блокувати недопромочені фічі від todo/.

## Applies If (ALL must hold)

- Team uses SDD lifecycle with backlog/todo/in-progress/done dirs.
- Promotion decisions are currently made informally.
- Reviewer role exists with authority to block.

## Skip If (ANY kills it)

- Team does not use SDD lifecycle.
- Project has < 10 features in backlog — overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature directory | .aidocs/backlog/<feature>/ | feature author |
| Reviewer roster | YAML | PM |
| Promotion policy | Markdown | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[definition-of-done-multi-role]] | promotion gate enforces per-role DoD readiness |

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
| `draft-sdd-promotion-gate-checklist` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/promotion-gate-checklist.md` | Markdown checklist with binary criteria + evidence column |
| `templates/promotion-gate.schema.json` | JSON Schema for the gate artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sdd-promotion-gate-checklist.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[definition-of-done-multi-role]]
- [[ai-assisted-specification-writing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
