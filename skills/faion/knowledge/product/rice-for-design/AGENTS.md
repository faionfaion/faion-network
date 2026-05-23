# Rice For Design

## Summary

**One-sentence:** RICE adapted for the design backlog: reach=affected user segment, impact=usability lift, confidence=evidence weight, effort=design+dev — emits a ranked design backlog scoped to the friction map.

**One-paragraph:** RICE adapted for the design backlog: reach=affected user segment, impact=usability lift, confidence=evidence weight, effort=design+dev — emits a ranked design backlog scoped to the friction map. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Rice For Design on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Design backlog has ≥10 candidate items and needs prioritisation.
- Friction map (journey + drop-off / complaint data) exists.
- Owner can estimate effort in design-days + dev-days.
- Solo founder or 1-2 person design team owns the queue.

## Skip If (ANY kills it)

- No friction map — do journey mapping first.
- Single-item queue — direct prioritisation.
- Pre-launch with no segment data — RICE inputs unavailable.
- Compliance / regulatory design changes — forced priority.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Friction map | journey + drop-off data | Analytics + interviews |
| Design backlog | list | Linear / Notion |
| Segment size estimates | table | Analytics |
| Effort estimates | design-days + dev-days | Designer + engineer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/feature-prioritization-rice` | Parent RICE methodology. |
| `solo/ux/ui-designer/journey-mapping` | Friction map source. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-rice-for-design` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-rice-for-design` | haiku | Schema check + threshold checks; deterministic. |
| `review-rice-for-design` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rice-for-design.json` | JSON skeleton conforming to the output contract schema. |
| `templates/rice-for-design.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rice-for-design.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[feature-prioritization-rice]]
- [[ui-designer]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
