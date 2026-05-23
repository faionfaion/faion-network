---
slug: tailwind-patterns
tier: solo
group: dev
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Tailwind variant-composition spec: cva() (class-variance-authority) for type-safe variants and cn() (clsx + tailwind-merge) for conflict-safe class merging.
content_id: "92464705d94e813e"
complexity: medium
produces: spec
est_tokens: 4900
tags: [tailwind, cva, variants, components, design-patterns]
---
# Tailwind Patterns with CVA

## Summary

**One-sentence:** Tailwind variant-composition spec: cva() (class-variance-authority) for type-safe variants and cn() (clsx + tailwind-merge) for conflict-safe class merging.

**One-paragraph:** Tailwind variant-composition spec: cva() (class-variance-authority) for type-safe variants and cn() (clsx + tailwind-merge) for conflict-safe class merging. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script `scripts/validate-tailwind-patterns.py` enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- Tailwind Patterns with CVA — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `tailwind-patterns` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Repeated component variants (button sizes, intents, states) need a type-safe definition.
- Conflicting Tailwind class merging is causing visual drift in component overrides.
- Existing components mix Tailwind classes with conditional logic in JSX.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Project has < 5 reusable components — cva overhead exceeds payoff.
- Team prefers a CSS-in-JS variant API (styled-components, vanilla-extract) and is unwilling to switch.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tailwind]] | Workflow context: related methodology in the same family |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-tailwind-patterns-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-tailwind-patterns.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tailwind-patterns.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[tailwind]]
- [[tailwind-architecture]]
- [[shadcn-ui]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (variant volume, conflict frequency, type-safety need) to cva-only / cva+tv / leave-as-is. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
