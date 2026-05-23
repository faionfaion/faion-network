# Design Review PR Checklist

## Summary

**One-sentence:** A PR-time design-QA checklist (10 items across token usage, component reuse, motion compliance, accessibility, content rules, breakpoint coverage) that gates whether the implementation matches the design handoff.

**One-paragraph:** Design handoff covers the upstream side; this methodology covers the downstream side: once dev opens the PR, a named designer or design-engineer reviews the 10-item checklist with evidence per item. Output is a per-PR design-QA record + a pass / changes-needed decision that blocks merge until design adherence is verified.

**Ефективно для:**

- Продукт із design-system + token каталогом, що ризикує drift'у на PR-level.
- Команди з design-engineering rotation, де designer review є required-gate.
- Регулярний UI-throughput із потребою audit-trail (token usage, state coverage).
- Контроль handoff-deviation — кожне відхилення повертається назад у design surface.

## Applies If (ALL must hold)

- Product has a design system with tokens + component library.
- Design-to-dev handoff methodology in use OR similar handoff bundle exists.
- PR touches UI code (components, styles, routes) — backend / docs-only PRs skip.
- A designer or design-engineer is available as a PR reviewer (or rotates for coverage).

## Skip If (ANY kills it)

- No design system in place — establish tokens + components first.
- Single-person dev-and-designer team — self-review checklist is sufficient.
- Prototype / spike PR explicitly marked 'experimental, not for design adherence'.
- Design adherence is acknowledged out-of-scope for the project phase (early MVP); add later.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Design system docs | token catalog + component catalog | design team |
| Handoff package | linked from story / PR | design-to-dev-handoff output |
| PR-platform reviewer rules | config | platform admin |
| Designer time allocation | calendar block <=20%/week | design ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-management]] | Names the designer/design-engineer as required reviewer in the engagement model. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology covering 10-item coverage, named reviewer, evidence-per-item, lane discipline, delta loop | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for design-QA record + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: rubber-stamp, evidence-skipped, lane-creep, silent-delta | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: classify PR -> run 10 items -> flag deltas -> decide -> log | 700 |
| `content/06-decision-tree.xml` | essential | PR classification -> run-or-skip routing | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pr-diff-classification` | haiku | Detect whether PR touches UI files (components, styles, routes). |
| `token-usage-audit` | sonnet | Diff PR vs token catalog; flag raw values. |
| `motion-a11y-audit` | sonnet | Verify motion, prefers-reduced-motion, focus order in implemented code. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-qa-checklist.md` | 10-item checklist printable card. |
| `templates/design-qa-record.json` | JSON skeleton for the per-PR record. |
| `templates/pr-comment.md` | PR comment template with per-item status. |
| `templates/scan-pr-for-raw-values.py` | Lints PR diff for raw colors / spacing / px instead of token usage. |
| `templates/audit-component-reuse.py` | Detects new components vs design-system catalog. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-review-pr-checklist.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[stakeholder-management]]
- [[release-planning]]
- [[product-explainability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
