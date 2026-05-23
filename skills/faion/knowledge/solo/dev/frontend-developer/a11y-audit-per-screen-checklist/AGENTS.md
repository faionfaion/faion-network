---
slug: a11y-audit-per-screen-checklist
tier: solo
group: dev
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Per-screen accessibility audit checklist running 9 critical WCAG-AA checks (semantic landmarks, focus order, contrast, alt text, ARIA correctness, keyboard nav, error messaging, motion-respect, screen-reader labels); produces a per-screen pass/fail row set with named fixes."
content_id: "6b3c94d224c19012"
complexity: medium
produces: checklist
est_tokens: 4900
tags: ["frontend", "solo", "a11y", "audit", "checklist"]
---
# A11y Audit per-Screen Checklist

## Summary

**One-sentence:** Per-screen accessibility audit checklist running 9 critical WCAG-AA checks (semantic landmarks, focus order, contrast, alt text, ARIA correctness, keyboard nav, error messaging, motion-respect, screen-reader labels); produces a per-screen pass/fail row set with named fixes.

**One-paragraph:** Per-screen accessibility audit checklist running 9 critical WCAG-AA checks (semantic landmarks, focus order, contrast, alt text, ARIA correctness, keyboard nav, error messaging, motion-respect, screen-reader labels); produces a per-screen pass/fail row set with named fixes. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- SaaS dashboards with ≥10 screens needing systematic AA coverage.
- Marketing pages where contrast and motion are visible compliance risks.
- Storybook component libraries pre-publish.
- Solo founders shipping under EU 'European Accessibility Act' obligations.

## Applies If (ALL must hold)

- Project has ≥1 user-facing screen targeting WCAG-AA conformance.
- Screens have a stable URL or storybook story id auditable in isolation.
- Operator has authority to ship fixes against findings.
- Browser-based audit tooling (axe-devtools, Lighthouse) is available.

## Skip If (ANY kills it)

- Internal-only tooling with one user — overhead exceeds value.
- Screen is still in design exploration — wait until DOM is stable.
- Org has a centralised a11y review process — duplicate effort.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[accessibility]] | upstream context this methodology builds on |
| [[accessibility-as-code]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-a11y-audit-per-screen-checklist-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-a11y-audit-per-screen-checklist.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-a11y-audit-per-screen-checklist.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[accessibility]]
- [[accessibility-as-code]]
- [[a11y-audit-per-screen-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
