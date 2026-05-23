---
slug: vui-conversation-design
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a multi-turn voice-dialog spec modelled as a state machine with explicit intents/entities/prompts, ≤12-word prompts, cap of 3 reprompts, and separate voice + screen scripts validated in realistic noise conditions.
content_id: "50b47ba24bfb8d6a"
complexity: medium
produces: spec
est_tokens: 4100
tags: [vui, conversation-design, dialog, voice-agent, intent-routing]
---
# VUI Conversation Design

## Summary

**One-sentence:** Produces a multi-turn voice-dialog spec modelled as a state machine with explicit intents/entities/prompts, ≤12-word prompts, cap of 3 reprompts, and separate voice + screen scripts validated in realistic noise conditions.

**One-paragraph:** Multi-turn voice conversations must be modelled as state machines. Each state has explicit intents, entities, prompts, and reprompt strategy. Reprompts cap at 3 (otherwise abandonment). Prompts stay at ≤12 spoken words. Voice scripts diverge from screen prompts (the same content cannot serve both modalities). Realistic-noise testing (kitchen, traffic, multiple speakers) catches edge cases pure-quiet testing misses. This methodology outputs a spec consumed by Dialogflow / Alexa / custom-LLM dialog engines.

**Ефективно для:**

- Multi-turn voice flow design where same conversation has happy + edge paths.
- Reprompt strategy для missing-entity / ambiguous-input / no-match.
- Separate voice-script + screen-prompt authoring.
- Noise-condition test plan.

## Applies If (ALL must hold)

- Voice flow has ≥2 turns (i.e., it is a conversation, not a single command).
- Multiple intents / entities live within the flow.
- Engineering can consume a state-machine spec.

## Skip If (ANY kills it)

- Single-turn command (use voice-ui spec).
- Pure transcript dictation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use-case map | Markdown | PM |
| Intent + entity list | JSON | VUI designer |
| Noise-test environment access | list | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[voice-ui]] | intent + slot vocabulary upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: state-machine-explicit, reprompt-cap-3, prompt-12-word-limit, separate-voice-screen-scripts, noise-test-required, handle-no-match-and-ambiguous | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `model-states` | sonnet | State design with transitions. |
| `write-voice-scripts` | sonnet | Concise spoken phrasings. |
| `noise-test` | haiku | Mechanical condition list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/dialog-spec.json` | Skeleton dialog spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-conversation-design.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[voice-ui]]
- [[vui-iot-integration]]
- [[vui-testing-best-practices]]
- [[vui-accessibility-inclusivity]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by turn count + state-machine completeness; enforces reprompt cap + noise-test coverage. Each leaf cites a rule from `01-core-rules.xml`.
