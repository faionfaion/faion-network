# Multimodal VUI Design

## Summary

Design voice + visual interfaces for smart displays by specifying four interaction patterns (voice-initiated screen-completed, screen-initiated voice-completed, voice + visual feedback, voice navigation + visual content) and enforcing a three-tier fallback hierarchy (voice → touch → keyboard). Every feature requires explicit timeout behavior, error state handling, and state-sync verification.

## Why

Voice-only interfaces cannot display complex data; screen-only UIs miss the hands-free use case. The combination requires synchronized state between voice and visual layers — the seam between modalities is where the UX fails. Explicit fallback hierarchies and timeout rules prevent the most common breakages.

## When To Use

- Designing a voice interface for a smart display (Amazon Echo Show, Google Nest Hub, Alexa TV)
- Building a product combining voice input with screen output
- Auditing an existing VUI for missing visual fallbacks
- Generating APL or equivalent smart display template markup from a design brief
- Prototyping a multimodal conversation flow where visual selection resolves voice ambiguity

## When NOT To Use

- Building a voice-only screenless speaker interface — pure VUI methodology is more appropriate
- Building a screen-only UI with optional voice layer — voice-initiated patterns add no value
- Target device has no reliable microphone (high-noise kiosk without directional mic)
- User research shows the target audience strongly opposes voice interaction

## Content

| File | What's inside |
|------|---------------|
| `content/01-interaction-patterns.xml` | Four multimodal patterns; smart display card layouts; fallback hierarchy rules |
| `content/02-anti-patterns.xml` | State-sync failures, platform APL differences, timeout edge cases, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/apl-card-generator.py` | Generate Alexa Presentation Language (APL) list card JSON for Echo Show |
| `templates/prompt-design-flow.txt` | Haiku prompt: feature brief → full multimodal interaction spec with fallback hierarchy |
| `templates/prompt-review-flow.txt` | Sonnet prompt: spec → state-sync and accessibility audit with severity ratings |
