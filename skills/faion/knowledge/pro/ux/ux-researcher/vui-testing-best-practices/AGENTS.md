---
slug: vui-testing-best-practices
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a two-tier VUI test report (deterministic + LLM-judge) keyed to feature × locale × noise with per-tier accuracy metrics.
content_id: "4cbc3e9248a0028f"
complexity: deep
produces: report
est_tokens: 4900
tags: [voice-testing, quality-assurance, llm-judge, nlu-testing, asr]
---
# VUI Testing Best Practices

## Summary

**One-sentence:** Produces a two-tier VUI test report (deterministic + LLM-judge) keyed to feature × locale × noise with per-tier accuracy metrics.

**One-paragraph:** Voice interfaces fail in ways usability tests miss: ASR provider upgrades shift WER silently, no-input and barge-in edge cases break state machines, and naturalness degrades when prompts repeat verbatim on retry. This methodology separates deterministic assertions (intent/slot/dialog-state) from LLM-judge scoring (naturalness, error recovery, completion), tracks ASR + NLU + dialog metrics independently, pins ASR model versions in CI, and tiers the suite (smoke → full → field-replay). Corpus is built from real anonymised logs first, then LLM-augmented. Stress fixtures mix utterances with ambient noise at 3 SNR levels.

**Ефективно для:**

- Pre-launch validation Alexa/Google/custom voice-agent: stress-test intents + dialog flow.
- Continuous regression на ASR/NLU/prompt changes — три рівні метрик окремо.
- Multilingual/accent expansion: regression-test ASR + naturalness across locales.
- Field-prep noise injection: TV/traffic/cafe stems на 20/10/5dB SNR.

## Applies If (ALL must hold)

- Pre-launch or continuous regression for a voice agent (Alexa, Google Action, custom LLM-VUI).
- Need to track ASR, NLU, and dialog metrics separately (not aggregated).
- LLM-judge tier is available and rate limits permit the cost.

## Skip If (ANY kills it)

- Voice is a single shortcut, not a primary interface — standard usability testing covers it.
- No working dialog model yet — start with Wizard-of-Oz prototyping, not test automation.
- Single-turn command testing only — an NLU benchmark (intent F1) is enough.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Utterance corpus | WAV + transcript JSON | real user logs, anonymised |
| Ambient noise stems | WAV (cafe / traffic / tv) | recorded or licensed |
| ASR model version pin | string | provider release notes |
| LLM-judge rubric | text | this methodology template |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[testing-developer]] | CI fixture wiring + pytest harness conventions |
| [[llm-integration]] | LLM-judge call patterns and rate-limit discipline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 700 |
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
| `templates/test-plan.md` | VUI test-plan skeleton: objectives, fixtures, metric targets, CI tier schedule |
| `templates/stress-corpus.sh` | Bash: mix clean utterances with ambient noise at 20/10/5dB SNR via ffmpeg |
| `templates/llm-judge-prompt.txt` | Per-turn LLM judge prompt scoring intent_match, naturalness, brevity, error_recovery |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-testing-best-practices.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[core-vui-design-principles]]
- [[error-handling-in-vui]]
- [[vui-conversation-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
