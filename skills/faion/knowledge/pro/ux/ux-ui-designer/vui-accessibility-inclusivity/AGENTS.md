# VUI Accessibility and Inclusivity

## Summary

A methodology for designing voice interfaces that serve diverse user populations: non-native speakers, accented speech, elderly users, and those with motor or visual impairments. Apply word-error-rate (WER) fairness evaluation across demographic slices, keep prompt language at reading grade 8 or below, and always provide a visual transcript alternative. Voice is an accessibility modality, not an add-on feature.

## Why

Major ASR engines show 1.5-2x higher error rates for non-white-male speakers (Stanford 2020; directionally confirmed with 2025 models). Switching the LLM does not fix ASR bias. Failure to test across accents produces voice flows that exclude the populations they claim to serve, violating the inclusive design intent and creating legal exposure under ADA/AODA/EAA.

## When To Use

- Building voice agents or IVR for diverse user bases: non-native speakers, elderly users, motor- or visually-impaired users.
- Auditing an existing voice product for ASR error rate by demographic group.
- Localizing a voice agent into a new language or regional dialect.
- Designing voice as the accessibility alternative to a touch UI (kiosk, automotive, hands-busy context).

## When NOT To Use

- Single-locale, single-accent, narrow-demographic prototype — full diversity testing can wait until validation.
- Heavy ambient-noise contexts where ASR fails for everyone — fix the audio pipeline (echo cancel, beamforming) first.
- Phone-tree IVR with rigid menu prompts — touch-tone fallback is the inclusive design path; accent-handling is secondary.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Accent/language support rules, benefit matrix by user group, prompt simplicity requirements |
| `content/02-agent-patterns.xml` | Agentic fairness-evaluation workflow, subagent roles, WER prompt pattern, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/vui_fairness.py` | WER-by-demographic evaluator: reads CSV of utterances, groups by accent/age, prints disparity table |

## Scripts

none
