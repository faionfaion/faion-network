# Backlog Grooming and Roadmapping

## Summary

**One-sentence:** Produces a groomed backlog + Now/Next/Later roadmap (RICE or MoSCoW scores + ≤3 P0 items + estimate-flagged AI scores) so weekly grooming produces a roadmap leaders trust without false date precision.

**Ефективно для:** Solo PMs whose backlog has 47 P0 items and a roadmap with dates nobody believes.

**One-paragraph:** Backlogs become unsearchable graveyards without weekly grooming; roadmaps with dates become political theatre. This methodology pins weekly grooming with RICE/MoSCoW scoring, caps P0 items at 3, marks AI-generated scores as [estimate], and translates the backlog into a Now/Next/Later horizon roadmap. Output is consumed by sprint planning and outcome-based-roadmaps.

## Applies If (ALL must hold)

- Backlog > 20 items needs weekly triage.
- Multiple stakeholders submit feature requests.
- Roadmap is shared with leadership or customers.
- Operator runs ≥1 sprint cadence.

## Skip If (ANY kills it)

- Backlog < 10 items — manual sort suffices.
- Pre-product phase — no backlog yet, only hypotheses.
- One-week throwaway project.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| backlog file | markdown/yaml | PM |
| scoring framework | RICE | MoSCoW | PM |
| current sprint capacity | tokens/hours | operator |
| strategic horizon | Now/Next/Later definition | founder |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/feature-prioritization-rice` | Sibling — provides RICE scoring rubric. |
| `solo/product/product-manager/outcome-based-roadmaps` | Downstream — consumes groomed backlog. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/backlog-grooming-roadmapping.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/backlog-grooming-roadmapping.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-backlog-grooming-roadmapping.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[feature-prioritization-rice]] — related methodology.
- [[feature-prioritization-moscow]] — related methodology.
- [[outcome-based-roadmaps]] — related methodology.
- [[backlog-management]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
