# Multimodal VUI Design

## Summary

**One-sentence:** Produces a voice + visual interaction spec for smart displays with four interaction patterns and a three-tier fallback hierarchy (voice → touch → keyboard) plus state-sync verification.

**One-paragraph:** Smart displays (Echo Show, Nest Hub, Alexa TV) combine voice input + screen output. Four interaction patterns cover the design space: voice-initiated screen-completed, screen-initiated voice-completed, voice + visual feedback, voice navigation + visual content. Every feature requires a three-tier fallback (voice → touch → keyboard), explicit timeout behaviour, error-state handling, and state-sync verification between voice intent and on-screen UI. This methodology produces a feature-level spec encoding all four.

**Ефективно для:** voice-UX engineer, що проектує Alexa / Google smart-display experience і потребує fallback + state-sync verification.

## Applies If (ALL must hold)

- Designing a voice interface for a smart display (Echo Show, Nest Hub, Alexa TV).
- Product combines voice input with screen output.
- Fallback hierarchy + state-sync verification are mandatory deliverables.

## Skip If (ANY kills it)

- Pure voice (no display) — use voice-only methodology.
- Pure screen (no voice) — use standard UI methodology.
- Smart display is the secondary surface — design primary first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Feature brief | markdown | PM |
| Target devices + APL version | list + version | engineering |
| Accessibility constraints | JSON | a11y team |
| Localization scope | list (locales) | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[llm-powered-conversational-ai]] | ASR/LLM/TTS pipeline context. |
| [[ai-design-assistant-patterns]] | Pattern catalogue. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-spec` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/feature-spec.json` | JSON skeleton with feature_id + pattern + fallback + timeout + error + statesync + locales. |
| `templates/_smoke-test.json` | Filled play-recipe-cards spec. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llm-powered-conversational-ai]]
- [[ai-design-assistant-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the spec; mis-routing leads to producing the wrong artefact shape.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature-spec.json`

```json
{
  "feature_id": "FILL_ME",
  "pattern": "FILL_ME",
  "fallback_tiers": [
    "voice",
    "touch",
    "keyboard"
  ],
  "timeout_ms": 8000,
  "error_state_ui": "FILL_ME",
  "statesync_test_path": "FILL_ME",
  "locales": [
    "en-US",
    "es-MX",
    "uk-UA"
  ]
}
```

### `templates/_smoke-test.json`

```json
{
  "feature_id": "FILL_ME",
  "pattern": "FILL_ME",
  "fallback_tiers": [
    "voice",
    "touch",
    "keyboard"
  ],
  "timeout_ms": 8000,
  "error_state_ui": "FILL_ME",
  "statesync_test_path": "FILL_ME",
  "locales": [
    "en-US",
    "es-MX",
    "uk-UA"
  ]
}
```
