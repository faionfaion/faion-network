# Release Planning

## Summary

**One-sentence:** Cross-team release bundling, scheduling, and communication discipline (release-train cadence, readiness matrix, deprecation comms, change-control artefacts) for paying-customer products.

**One-paragraph:** Fixed-cadence release train (weekly/biweekly/monthly), T-7d readiness matrix per function (eng/QA/support/sales/marketing/legal), >=90-day deprecation comms with customer-facing notes, named post-release monitor with rollback triggers. Output: release-plan markdown + readiness matrix + release notes.

**Ефективно для:**

- Multi-team release крізь engineering, support, sales-enablement, marketing, legal.
- Releases з paying customers, де breaking changes/deprecations присутні.
- Release calendar slipped двічі поспіль — shrink contents, скоротити cycle.
- Regulated/contractual deploy windows із customer-facing change-control артефактами.

## Applies If (ALL must hold)

- Multi-team release crossing engineering, support, sales-enablement, marketing, and legal.
- Releases with paying customers where breaking changes or deprecations are present.
- Release calendar has slipped twice in a row.
- Regulated or contractual deploy windows require customer-facing change-control artifacts.
- Release-train cadence reviews where the PM owns whether the train left full or empty.

## Skip If (ANY kills it)

- Internal tooling without external customers.
- Pre-PMF product shipping daily without deprecation surface.
- One-shot launches — use launch-readiness-review.
- Single-team product where coordination overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Release calendar | schedule | PM / release ops |
| Cross-function owner roster | table | org chart |
| Customer notification list | CRM segment | marketing / CS |
| Change-control template | doc | compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[launch-readiness-review]] | Provides per-release gate framework the readiness matrix mirrors. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: fixed cadence, readiness matrix, 90-day deprecation, customer-facing notes, post-release monitor | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for release-plan | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: ad-hoc dates, hidden readiness, short-deprecation, commit-log-notes | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: cadence -> matrix -> deprecation comms -> notes -> monitor | 900 |
| `content/05-examples.xml` | medium | Worked release plan with deprecation + post-release monitor | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on external customers + multi-team + breaking changes | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `readiness-matrix-author` | sonnet | Pull status from owners + assemble matrix. |
| `release-notes-customer-render` | sonnet | Convert commit log into customer-facing notes. |
| `post-release-monitor-plan` | haiku | Templated monitor + rollback assignment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/release-plan.md` | Release plan skeleton with cadence + matrix + deprecations. |
| `templates/release-notes.md` | Customer-facing release notes template. |
| `templates/release_readiness_lint.py` | Lint script for readiness matrix completeness. |
| `templates/prompt-manifest-generation.txt` | Prompt template for change-control manifest. |
| `templates/prompt-readiness-matrix.txt` | Prompt template for matrix synthesis. |
| `templates/prompt-release-notes.txt` | Prompt template for customer-facing notes. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-release-planning.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[launch-readiness-review]]
- [[stakeholder-management]]
- [[product-explainability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
