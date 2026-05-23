# Continuous Discovery

## Summary

**One-sentence:** Maintain a weekly customer-touch habit (interview / survey / observation) feeding a continuously updated assumption tree so discovery is a rhythm, not a project.

**One-paragraph:** Discovery is treated as a habit, not a quarterly project. The weekly touch keeps a rolling assumption tree fresh; the tree drives experiment design without restart cost. Solo founders skip discovery between launches and pay later — the habit prevents that.

**Ефективно для:**

- Solo founder shipping every 2 weeks but talking to no users between launches; needs a 1-hour weekly habit that keeps the assumption tree fresh.

## Applies If (ALL must hold)

- Product has ≥10 reachable users.
- Founder commits ≥1 hr/week to user touch.
- Assumption tree (or equivalent) exists or can be started.

## Skip If (ANY kills it)

- Pre-product phase — use directed discovery instead.
- Mass-market product with no reachable cohort.
- Founder cannot commit any weekly time — burn risk too high.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Reachable user list | csv | CRM / community |
| Assumption tree (seed) | markdown | Discovery output |
| Weekly slot in calendar | calendar event | Calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager/product-discovery` | Cycle-shaped discovery that draws from the rolling tree. |
| `solo/product/product-operations/feedback-management` | Feedback funnel feeding qualitative signal. |

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
| `draft-continuous-discovery` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-continuous-discovery` | haiku | Schema check + threshold checks; deterministic. |
| `review-continuous-discovery` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/continuous-discovery.json` | JSON skeleton conforming to the output contract schema. |
| `templates/continuous-discovery.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-continuous-discovery.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-discovery]]
- [[feedback-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
