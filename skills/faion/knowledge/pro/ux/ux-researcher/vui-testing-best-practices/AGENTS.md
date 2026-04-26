# VUI Testing Best Practices

## Summary

VUI testing validates voice interfaces across three accuracy tiers (ASR word-error rate, NLU intent+slot F1, dialog task completion) using a two-tier suite: deterministic scripted-fixture assertions and LLM-judge scoring for naturalness and repair quality. The method covers corpus construction, noise-injection stress testing, metric tracking, and CI integration.

## Why

Voice interfaces fail in ways that standard usability testing misses: ASR provider upgrades shift accuracy silently, no-input and barge-in edge cases break state machines, and naturalness degrades invisibly when prompts are repeated verbatim on retry. Separating test tiers (deterministic vs LLM-judge) and tracking ASR, NLU, and dialog completion independently isolates where regressions originate.

## When To Use

- Pre-launch validation of a voice skill or custom agent: stress-test intent recognition and dialog flow.
- Multilingual/accent expansion: regression-test ASR accuracy and prompt naturalness across locales.
- Continuous regression: every NLU model or prompt change re-runs utterance fixture corpus.
- Field testing prep: scripted noise-injection runs before recruiting real users.

## When NOT To Use

- Voice is a minor shortcut (tap-to-speak search) — standard usability testing covers it.
- No working dialog model yet — start with Wizard-of-Oz prototyping.
- Single-turn command testing only — an NLU benchmark (intent classification F1) is sufficient.

## Content

| File | What's inside |
|------|---------------|
| `content/01-test-layers.xml` | Five testing layers (unit, integration, user, stress, accessibility), key metrics, two-tier suite architecture. |
| `content/02-corpus-design.xml` | Utterance corpus construction from real logs, noise injection, locale variants, barge-in and no-input test requirements. |
| `content/03-antipatterns.xml` | LLM-judge biases, synthetic TTS fixture risk, privacy rules, cost tiering for suites. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-plan.md` | VUI test plan: objectives, fixture inventory, metric targets, CI tier schedule. |
| `templates/stress-corpus.sh` | Shell script: mix clean utterances with ambient-noise stems at multiple SNR levels. |
| `templates/llm-judge-prompt.txt` | Per-turn LLM judge prompt scoring intent_match, naturalness, brevity, error_recovery. |
