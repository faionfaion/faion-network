# Stakeholder Communication

## Summary

**One-sentence:** Selects one of 5 dialogue modes (interview, brainstorm, clarification, validation, socratic) and emits a Power/Interest-mapped engagement plan with templates per quadrant.

**One-paragraph:** Stakeholder communication selects a dialogue mode before any conversation: Interview (requirements gathering), Brainstorm (option generation), Clarification (resolving ambiguity), Validation (confirming understanding), Socratic (probing assumptions). Selecting the wrong mode — e.g. Socratic questions during a validation session — produces incoherent conversations and erodes trust. Stakeholder mapping by power/interest grid determines communication frequency and channel per quadrant.

**Ефективно для:**

- Requirements-gathering with a new stakeholder.
- Pre-meeting prep when the goal isn't clear.
- Selecting communication cadence per stakeholder.
- Coaching a junior PM out of mode-mixing in 1:1s.

## Applies If (ALL must hold)

- Conversation goal is identifiable (one of 5 modes).
- Stakeholder can be placed on a power/interest grid.
- Author has time to prepare; not an ambush.
- Multiple stakeholders make a stakeholder map worthwhile.

## Skip If (ANY kills it)

- Pure social conversation — no mode needed.
- Bilateral negotiation — use `negotiation` methodology.
- Conflict already escalated — use `difficult-conversations`.
- Single ad-hoc Slack DM — over-engineered.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder list | names + roles + decision power | PM |
| Goal per conversation | one sentence | session owner |
| Channel constraints | live / video / async / written | logistics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[active-listening]] | RASA discipline within Interview mode |
| [[mom-test]] | discovery-discipline upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `stakeholder-mapping` | sonnet | Light judgment on power/interest. |
| `mode-selection` | sonnet | Goal interpretation. |
| `plan-draft` | sonnet | Agenda + opening composition. |

## Templates

| File | Purpose |
|------|---------|
| `templates/meeting-prep.md` | Mode-tagged meeting prep skeleton |
| `templates/prompt-interview-guide.txt` | Prompt for an Interview-mode question set |
| `templates/prompt-socratic-chain.txt` | Prompt for a Socratic probe chain |
| `templates/requirement-capture.md` | Requirements capture skeleton (Interview output) |
| `templates/validation-email.md` | Validation write-back email skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-communication.py` | Validate stakeholder-communication artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[active-listening]]
- [[mom-test]]
- [[brainstorming-techniques]]
- [[difficult-conversations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by goal type to one of the 5 modes, each leaf referencing the rule that governs that mode.
