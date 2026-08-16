# Product Launch

## Summary

**One-sentence:** Run an outcome-driven product launch: stage-gated checklist, audience-segment cadence, on-launch monitors, and a 14-day post-launch review that decides scale/hold/rollback.

**One-paragraph:** Sequences launch work across pre-launch (assets + monitors), launch day (release + announce), and post-launch (review + scale-down). Every gate carries an explicit go/no-go threshold tied to metrics so 'we launched' becomes a measurable event with a sign-off and a rollback path, not a press release.

**Ефективно для:**

- Solo founder shipping a paid feature or new product to a list of ≥50 active users; needs a launch playbook that survives single-operator constraints and ends with a measurable post-launch decision.

## Applies If (ALL must hold)

- Launching a paid or significant free product to ≥1 audience segment.
- Pre-launch checklist required (assets, support, monitors).
- Post-launch review window ≥14 days available before next major change.

## Skip If (ANY kills it)

- Silent feature toggle for internal use only.
- Bug fix or maintenance release with no audience comms.
- No metrics infrastructure to evaluate launch success.
- Pre-PMF, where 'launch' is premature — keep iterating in discovery.
- Compliance or regulator-mandated release with no marketing surface.
- Single-customer enterprise deploy — use the account-handoff playbook instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Launch brief (problem/audience/value) | markdown | PM doc |
| Success metrics list | table | analytics plan |
| Audience segments | csv | CRM |
| Positioning statement | 1-page doc | PM |
| Channel inventory | table (email, social, blog, paid) | marketing |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager/spec-writing` | Spec is the input artefact this methodology launches. |
| `solo/product/product-manager/roadmap-design` | Roadmap context — where this launch sits in the sequence. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip + run rules: stage gates, segmented cadence, rollback, armed monitors, +14d window, one positioning segment, per-channel runbook, three-channel floor | 1200 |
| `content/01-planning.xml` | medium | Launch types, the T-8 to T+2 timeline, asset checklist, channel matrix, launch-day-of-week, pre-written rollback narrative | 1000 |
| `content/02-execution.xml` | medium | Launch-day DRI + human-held kill switch, monitoring thresholds, testimonials in 48h, 7-day retro, banned launch-copy words, press unreliability | 1050 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: press-release launch, no rollback plan, metrics vacuum, multi-segment mush, single-channel launch | 1000 |
| `content/04-procedure.xml` | essential | 6-step procedure: position -> pre-launch -> dry-run -> launch day -> first 72h -> +14d review | 1000 |
| `content/05-examples.xml` | essential | Worked examples: a concrete indie-dev launch hitting its metric, plus a stage-gated paid-plan launch | 900 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-product-launch` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-product-launch` | haiku | Schema check + threshold checks; deterministic. |
| `review-product-launch` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/product-launch.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/product-launch.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/product-launch.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/launch-plan.md.j2` | Launch plan skeleton — timeline, asset checklist, channels, metrics, rollback narrative |
| `templates/launch-plan.md` | Launch plan skeleton — timeline, asset checklist, channels, metrics, rollback narrative Generated from `templates/launch-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/launch-day-checklist.md.j2` | Launch-day runbook with DRI-approved announcement sequence. |
| `templates/launch-day-checklist.md` | Launch-day runbook with DRI-approved announcement sequence. Generated from `templates/launch-day-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-launch.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[spec-writing]]
- [[roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
