# Use Case Mapping

## Summary

**One-sentence:** Produces a use-case spec (actor + goal + preconditions + main flow + alternative flows + postcondition per use-case) so engineering and QA share an unambiguous map of what users actually do.

**Ефективно для:** Solo PMs and BAs who keep shipping features that don't fit any real workflow because nobody mapped the actor's full journey.

**One-paragraph:** Products get built without clear understanding of how users actually use them. This methodology pins each use-case to an explicit actor + goal + precondition + numbered main flow + branching alternative flows + postcondition. The output is consumable by engineering, QA, and writers as the single source of behavioural truth. Output is consumed by spec-writing and test-plan authoring.

## Applies If (ALL must hold)

- New feature or product where the flow is non-trivial (>3 user steps).
- Engineering and QA disagree on what 'happy path' means.
- Specification will drive test cases or acceptance criteria.
- Multiple actors interact with the same workflow.

## Skip If (ANY kills it)

- Pure-content changes (copy, image) with no behaviour.
- Backend-only refactors invisible to users.
- Single-step workflows where one acceptance criterion suffices.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| actor list with roles | array | researcher |
| goal statements per actor | string list | researcher |
| current journey data | transcripts/analytics | research |
| acceptance criteria draft | list | BA |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/user-interviews` | Upstream — provides actor journey data. |
| `solo/research/researcher/jobs-to-be-done` | Upstream — provides goal taxonomy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
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
| `templates/use-case-mapping.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/use-case-mapping.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-use-case-mapping.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[user-interviews]] — related methodology.
- [[jobs-to-be-done]] — related methodology.
- [[success-metrics-definition]] — related methodology.
- [[value-proposition-design]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
