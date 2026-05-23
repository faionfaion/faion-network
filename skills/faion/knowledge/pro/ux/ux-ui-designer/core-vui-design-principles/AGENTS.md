---
slug: core-vui-design-principles
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a VUI principle spec covering simplicity (short single-idea responses), natural conversation (follow-up awareness, turn-taking), and context awareness (memory of prior turns) for all voice runtimes from Alexa Skills to LLM Realtime agents.
content_id: "fe27bcf2bbcae8d0"
complexity: medium
produces: spec
est_tokens: 4200
tags: [voice-ui, vui, principles, conversational-design, latency]
---
# Core VUI Design Principles

## Summary

**One-sentence:** Produces a VUI principle spec covering simplicity (short single-idea responses), natural conversation (follow-up awareness, turn-taking), and context awareness (memory of prior turns) for all voice runtimes from Alexa Skills to LLM Realtime agents.

**One-paragraph:** Three foundational principles for voice user interfaces: simplicity (responses are short, single-idea, with branching options last); natural conversation (assistant tracks turn-taking, honours barge-in, handles follow-ups); context awareness (remember prior turns, adapt to user preferences, maintain task state). Apply across intent-based platforms (Alexa Skills, Google Actions) and LLM-native runtimes (Claude voice, OpenAI Realtime).

**Ефективно для:**

- Design baseline для будь-якого voice runtime — від Alexa до Realtime API.
- Чек single-idea response довжини (>=15 sec → split).
- Context-window memory спеца — design contract для multi-turn.
- Barge-in + turn-taking: розповсюдити на intent-based + LLM-native voice.

## Applies If (ALL must hold)

- Designing a voice-first or voice-augmented interface.
- Multi-turn dialog is in scope (not single command).
- Both intent-based and LLM-native runtimes are under consideration.

## Skip If (ANY kills it)

- Single-command voice shortcut (e.g. 'pause music') — principles overkill.
- Push-to-talk transcription only with no spoken response — different scope.
- Audio playback without dialog interaction — use audio UX, not VUI principles.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use cases list | scenario descriptions | product brief |
| Runtime target | Alexa | Google | Siri | LLM-native | platform decision |
| Persona | voice tone + register | brand guidelines |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[vui-conversation-design]] | Detailed conversation flow guidance builds on these principles |
| [[error-handling-in-vui]] | Recovery is a downstream concern |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vui-principles-spec.md` | Voice-runtime principle spec listing simplicity + natural conversation + context awareness with concrete knobs |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-core-vui-design-principles.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[vui-conversation-design]]
- [[error-handling-in-vui]]
- [[vui-testing-best-practices]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
