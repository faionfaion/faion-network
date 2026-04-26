# VUI Accessibility and Inclusivity

## Summary

Methodology for designing voice user interfaces that work equitably across accents, dialects, speech impediments, age groups, and languages. The core rule: never build a voice-only path — always pair every voice interaction with a visual or touch alternative.

## Why

Traditional voice systems trained on narrow datasets fail for non-native speakers, elderly users, people with stutters or other speech variations, and users in noisy environments. Inclusive VUI design reduces recognition errors, expands market reach, and satisfies WCAG requirements for perceivable, operable, understandable, and robust interfaces.

## When To Use

- Designing or auditing a VUI or voice assistant feature
- Evaluating speech recognition training data for diversity gaps
- Adding multimodal feedback (visual, haptic) to a voice interface
- Writing error-recovery dialogue scripts for voice flows
- Specifying accent calibration or pronunciation correction features
- Conducting inclusive usability testing with diverse voice participants

## When NOT To Use

- Pure GUI components with no voice interaction — use standard accessibility checklist instead
- Backend ASR model training (this methodology covers UX design, not ML training pipelines)
- Text-based chatbots with no speech I/O — different interaction model

## Content

| File | What's inside |
|------|---------------|
| `content/01-inclusivity-rules.xml` | Core design rules: diverse dataset requirements, visual alternatives, speech variation tolerance, privacy controls |
| `content/02-patterns.xml` | Inclusive VUI patterns with examples: clear prompts, error recovery, confirmation dialogs, multimodal feedback |

## Templates

none
