---
slug: accessibility-as-code
tier: solo
group: dev
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pattern for asserting accessibility invariants in code: unit-level component contracts, integration-level axe assertions, and CI gates that block on critical violations; produces a code scaffold + CI config making a11y regressions impossible to merge silently."
content_id: "9c62f72ca2dbe343"
complexity: deep
produces: code
est_tokens: 4900
tags: ["frontend", "solo", "a11y", "automation", "ci"]
---
# Accessibility as Code

## Summary

**One-sentence:** Pattern for asserting accessibility invariants in code: unit-level component contracts, integration-level axe assertions, and CI gates that block on critical violations; produces a code scaffold + CI config making a11y regressions impossible to merge silently.

**One-paragraph:** Pattern for asserting accessibility invariants in code: unit-level component contracts, integration-level axe assertions, and CI gates that block on critical violations; produces a code scaffold + CI config making a11y regressions impossible to merge silently. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Component libraries where a11y is a publishable contract.
- SaaS apps that must catch regressions before customer-visible.
- Solo founders avoiding manual audits every release.
- Migrations from a manual audit cadence to a continuous one.

## Applies If (ALL must hold)

- Project has component-level testing infrastructure (Vitest, Jest, Storybook test-runner).
- Project has integration / e2e testing (Playwright, Cypress).
- CI is configured and can run a11y jobs without exceeding budget.
- Conformance target (A, AA, AAA) is already named.

## Skip If (ANY kills it)

- Project has no automated tests yet — start with the accessibility spec first.
- CI budget cannot accommodate an extra job — reduce scope first.
- All a11y work is manual (audit-only) — different methodology applies.

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
| [[a11y-audit-per-screen-checklist]] | sibling discipline cited in decision tree |

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
| `fill-accessibility-as-code-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-accessibility-as-code.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-accessibility-as-code.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[accessibility]]
- [[a11y-audit-per-screen-checklist]]
- [[ci-quality-gate-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
