# Consistency and Standards

## Summary

**One-sentence:** Audit and enforce internal and external consistency — terminology, components, gestures, and platform conventions — so users do not have to relearn the same idea twice.

**One-paragraph:** Audit and enforce internal and external consistency — terminology, components, gestures, and platform conventions — so users do not have to relearn the same idea twice.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Design system exists but is partially adopted across the product.
- Same action is exposed with different labels or controls in different flows.
- Onboarding or support reports highlight terminology mismatches.
- Cross-platform product needs to honour OS conventions without diverging too far.
- New page is being added that should obey existing patterns.

## Skip If (ANY kills it)

- Early prototype where divergence is intentional and explorative.
- Brand pivot in progress — wait for the new system to stabilise.
- Single-page utility with no recurring patterns.
- Standards already enforced by automated linting in CI.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Design system reference | url / storybook | Design system team |
| Glossary of approved terms | markdown | Content team |
| UI inventory | figma | Design ops |
| Platform style guide links | url list | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/heuristic-evaluation` | Heuristic-4 violations highlight inconsistencies. |
| `solo/ux/ux-ui-designer/aesthetic-minimalist` | Minimalist passes intersect with standards enforcement. |

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
| `templates/consistency-standards.json` | JSON skeleton conforming to the output contract schema. |
| `templates/consistency-standards.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-consistency-standards.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[heuristic-evaluation]]
- [[aesthetic-minimalist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
