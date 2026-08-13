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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[core-vui-design-principles]]
- [[error-handling-in-vui]]
- [[vui-conversation-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/stress-corpus.sh`

```bash
set -euo pipefail
CLEAN_DIR=${1:-fixtures/clean}
NOISE_DIR=${2:-fixtures/noise}
OUT=${3:-fixtures/mixed}
mkdir -p "$OUT"
for u in "$CLEAN_DIR"/*.wav; do
  for n in "$NOISE_DIR"/*.wav; do
    for snr in 20 10 5; do
      base="$(basename "$u" .wav)_$(basename "$n" .wav)_${snr}dB.wav"
      ffmpeg -y -i "$u" -i "$n" \
        -filter_complex "[1:a]volume=-${snr}dB[bg];[0:a][bg]amix=inputs=2:duration=first" \
        "$OUT/$base" 2>/dev/null
    done
  done
done
```

### `templates/llm-judge-prompt.txt`

```text
Conversation so far: {transcript}
User utterance: "{utterance}"
Assistant response: "{response}"

Score (1-5) each independently. DO NOT see the expected answer.
- intent_match: did the response address the user's likely intent?
- naturalness: would a human speak this way?
- brevity: is the response single-idea and <=15 sec spoken?
- error_recovery: if the previous turn errored, did the response vary + add scaffolding?

Return JSON. Penalise if the response invents facts not in {kb}.
```
