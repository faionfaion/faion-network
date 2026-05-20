---
slug: error-handling-in-vui
tier: pro
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A three-rung re-prompt ladder for voice interface error recovery: rung 1 — brief re-ask; rung 2 — constructive re-ask with two example phrases; rung 3 — escalation to visual fallback, DTMF, or human agent.
content_id: "09b767fa3be9320a"
tags: [voice-ui, error-handling, asr, conversational-design, vui]
---
# Error Handling in VUI

## Summary

**One-sentence:** A three-rung re-prompt ladder for voice interface error recovery: rung 1 — brief re-ask; rung 2 — constructive re-ask with two example phrases; rung 3 — escalation to visual fallback, DTMF, or human agent.

**One-paragraph:** A three-rung re-prompt ladder for voice interface error recovery: rung 1 — brief re-ask; rung 2 — constructive re-ask with two example phrases; rung 3 — escalation to visual fallback, DTMF, or human agent. Cap at three rungs; escalate on rung 4 input instead of looping. Never use blame language ("you said wrong", "invalid"). Every example phrase on rung 2 must exist in the NLU training data.

## Applies If (ALL must hold)

- Designing fallback dialogs for ASR no-input, no-match, and ambiguous-intent failures.
- Drafting re-prompt copy with example phrases for second/third failure passes.
- Auditing existing Alexa/Google Action/Dialogflow intents for unhandled utterances.
- Building help or transfer-to-agent escalation paths for IVR or LLM-backed voice bots.

## Skip If (ANY kills it)

- Pure speech-to-text quality issues—model retraining or acoustic tuning, not dialog design.
- Silent or visual-only UIs where confirmation can be shown on screen.
- One-shot transactional commands with no multi-turn state (no recovery path needed).

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ux/ux-ui-designer/`
