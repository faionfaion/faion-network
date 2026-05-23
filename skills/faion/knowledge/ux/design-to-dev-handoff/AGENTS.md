# Design-to-Dev Handoff

## Summary

**One-sentence:** Process for handing off a finished design to engineering with a complete spec, walkthrough video, and acceptance criteria so engineering can ship without follow-up questions.

**One-paragraph:** Most production bugs trace back to gaps in the handoff. This process pins a four-step ritual: (1) ship a handoff-spec (states, tokens, motion, a11y, edge cases, code map), (2) record a 5-min walkthrough video naming gotchas, (3) co-write acceptance criteria with engineering, (4) hold a 15-min handoff sync where eng can ask questions. The handoff artefact lives in the repo next to the code.

**Ефективно для:**

- Solo founder doing weekly design→eng handoffs to remote engineers.
- Designer + AI-agent pair where the agent generates code from the spec.
- Cross-timezone teams where async handoff has to work first-time.
- Pre-launch design freeze where handoff loss must be near-zero.

## Applies If (ALL must hold)

- A design is ready for engineering (out of iteration, into ship).
- Engineering owner (or agent) is identified.
- A handoff-spec-template can be filled and a 15-min sync scheduled.
- Acceptance criteria can be co-written before code starts.

## Skip If (ANY kills it)

- Prototype-only work that will not ship.
- Design system primitive maintained directly by eng — different process.
- Live-edit work where designer is in the codebase — no handoff needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Filled handoff-spec | JSON / MD | handoff-spec-template output |
| Walkthrough video | Loom / mp4 URL | Designer recording |
| Acceptance criteria draft | MD | Designer + eng pre-write |
| Eng owner handle | string | Team directory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/handoff-spec-template` | Spec artefact this process delivers. |
| `solo/ux/edge-case-checklist` | Edge cases consumed in the spec. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-handoff-package` | sonnet | Per-handoff judgement on spec completeness. |
| `validate-package` | haiku | Deterministic check that spec / video / AC / sync are all present. |
| `multi-component-handoff` | opus | Cross-component synthesis for a flow-level handoff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-to-dev-handoff.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/design-to-dev-handoff.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-to-dev-handoff.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[handoff-spec-template]]
- [[edge-case-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
