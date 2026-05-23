# Acceptance Criteria Quality Rubric

## Summary

**One-sentence:** Score each acceptance criterion against a 5-axis rubric (testable / atomic / observable / unambiguous / negative-cases) and reject any AC scoring <4/5 before engineering starts.

**One-paragraph:** AC drift is the single biggest source of done-definition disputes. The 5-axis rubric makes drift visible: each AC is graded before engineering accepts the spec. Rejected AC are rewritten; the rubric becomes a contract between PM and dev.

**Ефективно для:**

- Solo PM whose engineers keep asking 'but what does done mean?' — needs a one-page rubric that turns vague AC into binary checks.

## Applies If (ALL must hold)

- Spec contains ≥3 acceptance criteria.
- Engineering will start work based on the spec.
- Reviewer is available before kickoff.

## Skip If (ANY kills it)

- Bug fix with single obvious AC (reproduction case).
- Spike / research — AC don't apply.
- AC already gold-plated and well-tested elsewhere.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Draft spec with AC | markdown | PM doc |
| Rubric reference | table | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager/spec-writing` | Source artefact whose AC are graded. |

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
| `draft-ac-quality-rubric` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-ac-quality-rubric` | haiku | Schema check + threshold checks; deterministic. |
| `review-ac-quality-rubric` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ac-quality-rubric.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ac-quality-rubric.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ac-quality-rubric.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-writing]]
- [[product-roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
