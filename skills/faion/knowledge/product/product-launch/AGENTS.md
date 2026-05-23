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

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Launch brief (problem/audience/value) | markdown | PM doc |
| Success metrics list | table | analytics plan |
| Audience segments | csv | CRM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager/spec-writing` | Spec is the input artefact this methodology launches. |
| `solo/product/product-manager/roadmap-design` | Roadmap context — where this launch sits in the sequence. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
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
| `templates/product-launch.json` | JSON skeleton conforming to the output contract schema. |
| `templates/product-launch.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-launch.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-writing]]
- [[roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
