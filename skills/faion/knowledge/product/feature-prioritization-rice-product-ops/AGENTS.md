# Feature Prioritisation — RICE

## Summary

**One-sentence:** Score features by Reach × Impact × Confidence ÷ Effort; rank by descending RICE; refuse to commit anything with confidence <50% or effort >team-week without a spike.

**One-paragraph:** RICE turns prioritisation arguments into arithmetic. The score forces explicit estimates per dimension; the comparison is the score not the dimension. Confidence floor + effort ceiling keep low-evidence bets out of Now and prevent multi-week scope from sneaking in unspiked.

**Ефективно для:**

- Solo PM with ≥5 features competing for the same engineering hour; needs a defensible, repeatable ordering rather than a HiPPO vote.

## Applies If (ALL must hold)

- ≥5 features contending for the next slot.
- Reach and impact can be estimated within an order of magnitude.
- Decision needs to be auditable / explainable to stakeholders.

## Skip If (ANY kills it)

- Single contested item — RICE doesn't decide between 1.
- Compliance / contractual deadline — RICE doesn't override.
- All items same persona + same job — use kano or another lens.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature list | csv | Backlog |
| Reach unit policy (users/week vs lifetime) | table | Team doc |
| Effort estimation scale (person-weeks) | table | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/backlog-management` | Source of items that enter scoring. |
| `solo/product/product-manager/spec-writing` | Downstream artefact for the top-RICE item. |

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
| `draft-feature-prioritization-rice` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-feature-prioritization-rice` | haiku | Schema check + threshold checks; deterministic. |
| `review-feature-prioritization-rice` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feature-prioritization-rice.json` | JSON skeleton conforming to the output contract schema. |
| `templates/feature-prioritization-rice.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feature-prioritization-rice.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[backlog-management]]
- [[spec-writing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
