---
slug: error-prevention
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design constraints, confirmations, defaults, and forgiving formats so dangerous actions never occur or surface as a question before they commit.
content_id: "63a5c419599d76c8"
complexity: medium
produces: checklist
est_tokens: 3200
tags: ["heuristic", "error-prevention", "forms", "validation", "nielsen"]
---
# Error Prevention

## Summary

**One-sentence:** Design constraints, confirmations, defaults, and forgiving formats so dangerous actions never occur or surface as a question before they commit.

**One-paragraph:** Design constraints, confirmations, defaults, and forgiving formats so dangerous actions never occur or surface as a question before they commit.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Workflow exposes destructive or irreversible actions to users.
- Bug tickets cite accidental clicks, double submissions, or misformatted input.
- Forms accept ambiguous free text that downstream systems must parse.
- Recovery from the action would be costly in time, money, or trust.
- Engineering can add validation, confirmation, or undo at acceptable cost.

## Skip If (ANY kills it)

- Action is genuinely reversible at zero cost — prevention adds friction.
- Power-user tool where confirmations would slow daily work.
- Throwaway prototype with no real impact.
- Compliance already provides the safety net (e.g., signed transactions).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inventory of destructive actions | markdown | Design audit |
| Bug-ticket sample on mis-clicks | csv | Support tool |
| Form-validation rules | yaml / json | Backend team |
| Confirmation pattern catalogue | url | Design system |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/error-recovery` | Recovery closes the loop when prevention fails. |
| `solo/ux/ux-ui-designer/user-control-freedom` | Undo is the safety net behind prevention. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + run/skip rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-artefact` | sonnet | Section-by-section judgement against the rubric. |
| `lint-and-validate` | haiku | Deterministic schema validation + forbidden-pattern check. |
| `final-review` | opus | Cross-section coherence and stakeholder readiness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-prevention.json` | JSON skeleton conforming to the output contract schema. |
| `templates/error-prevention.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-prevention.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[error-recovery]]
- [[user-control-freedom]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
