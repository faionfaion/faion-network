# User Interviews

## Summary

**One-sentence:** Produces a user-interview report (Mom Test script + diarized transcripts + behavioural-ask outcome per session + frequency-counted insight list) so customer-discovery conversations produce evidence, not compliments.

**Ефективно для:** Solopreneurs whose 'user interviews' keep returning enthusiastic compliments and zero usable insight.

**One-paragraph:** Founders skip user interviews or conduct them poorly: leading questions, pitching instead of listening, accepting 'I would' as data. This methodology pins each session to a Mom Test script (past behaviour, not hypotheticals), enforces a behavioural ask at session end, requires diarized transcripts, and produces a frequency-counted insight list. Output is consumed by problem-validation-2026 and value-proposition-design.

## Applies If (ALL must hold)

- Pre-MVP discovery: understand the problem before building.
- Post-launch retention research: why are users churning?
- Pricing or positioning research where survey data is too thin.
- New segment exploration where you have no prior data.

## Skip If (ANY kills it)

- When A/B testing answers the question faster.
- When the segment is unreachable within a reasonable window.
- When the team has no capacity for diarized transcription + synthesis.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| recruit list with cold/warm tags | array | researcher |
| hypothesis or decision the interview informs | string | PM |
| Mom Test script | markdown | researcher |
| diarized recording setup | tool | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/research-repo-file-naming-convention` | Downstream — transcripts land in the named repo. |
| `solo/research/researcher/problem-validation-2026` | Downstream — consumes the report for tier-scoring. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 failure modes with detector + repair | ~800 |
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
| `templates/user-interviews.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/user-interviews.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-user-interviews.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[problem-validation-2026]] — related methodology.
- [[value-proposition-design]] — related methodology.
- [[use-case-mapping]] — related methodology.
- [[single-interview-fast-loop-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
