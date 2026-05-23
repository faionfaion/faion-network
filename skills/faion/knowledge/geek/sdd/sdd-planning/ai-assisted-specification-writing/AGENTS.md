---
slug: ai-assisted-specification-writing
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Drafts an implementation-plan.md from an approved spec.md using an LLM, with human gates at task breakdown and dependency graph.
content_id: "68cea9a3a24356c5"
complexity: medium
produces: spec
est_tokens: 3800
tags: ["specification", "sdd-planning", "ai-assisted", "implementation-plan", "requirements"]
---
# AI-Assisted Specification Writing (Planning Layer)

## Summary

**One-sentence:** Drafts an implementation-plan.md from an approved spec.md using an LLM, with human gates at task breakdown and dependency graph.

**One-paragraph:** AI-Assisted Specification Writing (Planning Layer) produces a spec that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Швидкий чорновий implementation-plan.md після того, як spec.md затверджений.
- Task decomposition: LLM пропонує задачі, human reviewer фіксує залежності.
- Token-budget estimation: LLM зразу заповнює est_tokens на task.
- Critical-path detection: LLM ідентифікує блокери.
- Onboarding: junior бачить як spec → plan flow виглядає.

## Applies If (ALL must hold)

- spec.md is approved and stable (no open AC).
- Team uses SDD implementation-plan.md template.
- Human reviewer can gate task graph + dependencies.

## Skip If (ANY kills it)

- spec.md has open AC or unresolved blocking questions.
- Project has < 5 tasks — plan is overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved spec.md | Markdown | PM + tech lead |
| Team roster | YAML | PM |
| Token-budget rules | JSON | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-assisted-specification-writing (sdd)]] | spec-layer counterpart whose output we consume |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/05-examples.xml` | supplemental | One worked example end-to-end | 400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-assisted-specification-writing` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/implementation-plan.md` | Implementation-plan skeleton with task table + DAG section |
| `templates/plan-prompt.md` | LLM prompt template for task decomposition |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-specification-writing.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[ai-assisted-specification-writing]]
- [[sprint-capacity-from-complexity-tags]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
