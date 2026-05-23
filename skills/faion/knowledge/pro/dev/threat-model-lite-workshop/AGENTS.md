---
slug: threat-model-lite-workshop
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 60-minute threat-model lite workshop facilitation: data-flow whiteboard, STRIDE-Lite per element, top-5 prioritised threats, named mitigation owners.
content_id: "2ee157ca5886079e"
complexity: medium
produces: playbook-step
est_tokens: 4100
tags: [threat-model, workshop, security, qa, lite]
---
# Threat Model Lite Workshop

## Summary

**One-sentence:** 60-minute threat-model lite workshop facilitation: data-flow whiteboard, STRIDE-Lite per element, top-5 prioritised threats, named mitigation owners.

**One-paragraph:** 60-minute threat-model lite workshop facilitation: data-flow whiteboard, STRIDE-Lite per element, top-5 prioritised threats, named mitigation owners. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-threat-model-lite-workshop.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- QA engineer rollout security-testing program у середній команді (5-15 devs).
- New feature scoped для launch, нема full TM workshop часу.
- Cross-functional (eng + product + QA) education на STRIDE basics.
- Recurring cadence (per quarter / per major feature) where Lite scales > Full.

## Applies If (ALL must hold)

- Team ≥5 people willing to spend 60 minutes on threat-modelling
- New feature or service-edge scoped within session
- Data-flow diagram can be drawn on whiteboard in <15 min
- Mitigation owners can be named within the session

## Skip If (ANY kills it)

- Compliance context needs full STRIDE TM, not Lite
- <5 attendees — workshop dynamics break down
- Team has no shared security vocabulary — workshop becomes 101 lecture
- No follow-up ownership — workshop output dies in slides

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-threat-model-lite-workshop` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-threat-model-lite-workshop.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[stride-lite-checklist-for-architects]]
- [[threat-model-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
