# Product Discovery

## Summary

**One-sentence:** Time-boxed (1-4w) de-risking of an idea across the four product risks (value, usability, feasibility, viability) before committing build resources, producing a discovery report with a go / hold / no-op verdict.

**One-paragraph:** Time-boxed (1-4w) de-risking of an idea across the four product risks (value, usability, feasibility, viability) before committing build resources, producing a discovery report with a go / hold / no-op verdict. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Product Discovery on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Idea backed by ≥1 stakeholder request but no validated demand signal.
- Build effort would exceed 2 weeks if the idea were committed today.
- ≥5 representative users reachable for interviews / prototype tests.
- Time-box of 1-4 weeks available before the build decision.

## Skip If (ANY kills it)

- Already-validated idea with paying customers — skip discovery, scope MVP.
- Pure refactor / infra / compliance work with no user-facing risk.
- No reachable target users — go do problem-validation first.
- Discovery would exceed the cost of building (small / cheap features).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Idea brief | 1-page doc | Stakeholder |
| Target segment | persona + reachability proof | CRM / Discord |
| Discovery budget | 1-4 week time-box | Planning |
| Risk hypothesis list | value/usability/feasibility/viability | Team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/continuous-discovery` | Provides ongoing customer voice; this scopes a time-boxed instance. |
| `solo/product/product-planning/mvp-scoping` | Downstream consumer of the discovery verdict. |

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
| `draft-product-discovery` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-product-discovery` | haiku | Schema check + threshold checks; deterministic. |
| `review-product-discovery` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/product-discovery.json` | JSON skeleton conforming to the output contract schema. |
| `templates/product-discovery.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-discovery.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[continuous-discovery]]
- [[mvp-scoping]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
