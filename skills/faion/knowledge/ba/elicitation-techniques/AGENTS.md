# Elicitation Techniques

## Summary

**One-sentence:** Triangulated elicitation pipeline (interview/workshop/observation/survey/prototype/focus-group/brainstorm) producing typed session artifacts and REQ stubs that cite ≥2 distinct techniques per requirement.

**One-paragraph:** Elicitation draws information from stakeholders about needs, wants, and constraints. Core techniques: interviews, workshops, observation, document analysis, surveys, prototyping, focus groups, brainstorming. Each session produces a typed artifact committed to version control with consent and PII-redaction markers; a synthesis step extracts REQ stubs that cite at least two distinct technique sessions per requirement, enforcing triangulation as an empirical requirement quality gate.

**Ефективно для:**

- Kickoff нової ініціативи з vague stakeholder needs.
- Discovery sprintів, де потрібна triangulation за тиждень.
- Регульовані домени з audit trail elicitation evidence.
- Distributed teams, де sync session фізично неможливі.

## Applies If (ALL must hold)

- Kickoff of a new initiative with vague, contradictory, or undocumented stakeholder needs.
- Migration / replatform where knowledge lives in a few senior employees' heads.
- Regulated domains where elicitation evidence is part of the audit trail.
- Discovery sprints requiring triangulated process within one week using mixed techniques.
- Distributed / async teams where surveys, recorded interviews, async observation are the only channels.

## Skip If (ANY kills it)

- Solo founder or 2-person team where direct conversation is faster than formal sessions.
- Backlog refinement on a stable product — DoR + slice discussions cover it.
- Answer is already in a spec/ADR/RFC — read first, elicit only the gaps.
- Bug triage / incident postmortems — they have their own templates.
- Stakeholders unwilling/unavailable — escalate sponsorship instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Stakeholder map | JSON / Markdown | stakeholder-analysis |
| Session calendar slots | ics / Google Cal | scheduling |
| Recording consent forms | PDF / Markdown | legal |
| PII redaction policy | Markdown | legal / compliance |
| Existing docs catalog | Markdown index | knowledge management |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/glossary-management-living-doc` | Anchor every elicited term to canonical definition. |
| `pro/ba/business-analyst/frontline-validation-protocol` | Operator validation gate for any process claim. |
| `pro/ba/business-analyst/remote-workshop-toolkit` | Workshop technique uses the toolkit. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interview-guide-drafting` | sonnet | Light judgement on non-leading prompts. |
| `workshop-design` | opus | Deep design of consensus protocol + agenda. |
| `session-artifact-typing` | haiku | Mechanical tag of each artifact with technique + scope. |
| `req-stub-synthesis` | sonnet | Synthesise REQ stubs citing ≥2 sessions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-guide.md` | Non-leading 60-minute interview structure with consent + PII block. |
| `templates/workshop-agenda.md` | Structured workshop agenda with breakouts + ground rules. |
| `templates/session-check.py` | Validate session artifact: consent flag, redaction tags, technique attestation. |
| `templates/_smoke-test.md` | Minimum viable session artifact + REQ stub. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-elicitation-techniques.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

- [[frontline-validation-protocol]]
- [[remote-workshop-toolkit]]
- [[glossary-management-living-doc]]
- [[requirements-documentation]]
- [[stakeholder-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.
