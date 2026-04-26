# VUI Test Plan

**Project:** [Name]
**Platform:** [Alexa / Google / Custom LLM-VUI / IVR]
**Locales:** [e.g., en-US, en-GB]
**ASR Model Version:** [Pin version here]

## Objectives
- Validate intent recognition accuracy before launch
- Stress-test dialog flow completion across noise conditions
- Regression-test after NLU model or prompt changes

## Test Suite Structure

| Tier | Trigger | Utterance Count | LLM Judge? |
|------|---------|-----------------|------------|
| Smoke | Every commit | 10 | No |
| Full | Nightly | All fixtures | Yes |
| Field-replay | Pre-release | Real session sample | Yes |

## Fixture Inventory

| File | Intent | Variant Count | Noise Conditions |
|------|--------|---------------|------------------|
| [fixtures/set-timer.wav] | set-timer | 30 | clean, cafe-20dB, traffic-10dB |

## Metric Targets

| Metric | Target | Blocking? |
|--------|--------|-----------|
| ASR WER | &lt;5% | Yes |
| NLU Intent F1 | &gt;0.90 | Yes |
| Task completion | &gt;85% | Yes |
| LLM-judge naturalness | &gt;3.5/5 avg | No (advisory) |

## LLM-Judge Configuration
- Model: [pin version]
- Temperature: 0
- Blind scoring: YES (judge does not see expected answer before scoring naturalness)
- Comparison method: pairwise for naturalness, absolute for correctness

## Privacy
- All fixtures: anonymized before storage
- Cloud LLM judge receives: text transcripts only, no raw audio
- PII redaction tool: [e.g., presidio]
