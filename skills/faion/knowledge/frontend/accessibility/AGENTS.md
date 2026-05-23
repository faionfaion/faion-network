# Accessibility

## Summary

**One-sentence:** Specification of accessibility expectations for a frontend codebase: WCAG-AA conformance target, tooling baseline, per-role responsibilities, and regression-prevention contract; produces an a11y spec that the team agrees to and that subsequent audits assert against.

**One-paragraph:** Specification of accessibility expectations for a frontend codebase: WCAG-AA conformance target, tooling baseline, per-role responsibilities, and regression-prevention contract; produces an a11y spec that the team agrees to and that subsequent audits assert against. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Solo founders deciding the a11y target before the codebase exists.
- Teams adopting WCAG-AA for the first time after a customer complaint.
- Component-library publishers who must guarantee a11y to consumers.
- Pre-funding compliance prep (EU EAA, ADA Title III risk).

## Applies If (ALL must hold)

- Project ships a user-facing UI consumed outside the engineering team.
- Org commits (or must commit) to a named WCAG conformance level (A, AA, or AAA).
- Operator can enforce CI gates and PR checklists.
- Component library or design system exists where a11y baseline can be set once.

## Skip If (ANY kills it)

- Pure internal tool used by 1–2 named operators — overhead exceeds value.
- API-only product with no user-facing UI.
- Org explicitly disclaims a11y commitments (rare; usually a compliance risk in itself).

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
| [[a11y-audit-per-screen-checklist]] | upstream context this methodology builds on |
| [[accessibility-as-code]] | sibling discipline cited in decision tree |

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
| `fill-accessibility-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-accessibility.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-accessibility.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[a11y-audit-per-screen-checklist]]
- [[accessibility-as-code]]
- [[design-tokens-basics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
