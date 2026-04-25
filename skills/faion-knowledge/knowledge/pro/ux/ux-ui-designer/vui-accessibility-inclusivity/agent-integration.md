# Agent Integration — VUI Accessibility and Inclusivity

## When to use
- Building voice agents or IVR for diverse user bases — non-native speakers, accented English/Ukrainian/Spanish, elderly users, users with motor or visual impairments.
- Auditing an existing voice product for ASR error rate by demographic group; voice UX failure is rarely uniform.
- Localizing a voice agent into a new language or regional dialect (UA-PT, EN-IN, ES-AR).
- Designing voice as the accessibility alternative to a touch UI (kiosk, automotive, hands-busy contexts).

## When NOT to use
- Single-locale, single-accent, narrow-demographic prototype — full diversity testing can wait until validation.
- Heavy ambient-noise contexts where ASR fails for everyone — fix the audio pipeline (echo cancel, beamforming) before fairness work.
- Phone-tree IVR with rigid menu prompts — touch-tone fallback is the inclusive design path; accent-handling is secondary.

## Where it fails / limitations
- Most major ASR engines have measurable bias: error rates 1.5-2x higher for non-white-male speakers (Stanford 2020 study still directionally true with 2025 models).
- LLM voice agents inherit the bias of underlying ASR + TTS; switching the LLM does not fix it.
- "Accent calibration" prompts often feel othering ("please speak more clearly") — design must be invisible to the user.
- Speech variation (stutter, dysarthria, very fast/slow tempo) is rarely well-supported; accommodation usually requires per-user tuning.
- Visual alternatives are mandatory; deaf-blind users still need captions, and pure-voice flows exclude them.

## Agentic workflow
Run an evaluation harness across a demographically representative test set (commercial corpora + synthetic + real user volunteers) measuring word error rate (WER) and intent accuracy by group. Use a subagent to generate synthetic accented test phrases via SSML/voice clones, another to compute WER, a third to recommend accommodations (extended timeouts, simpler grammar, visual fallback). Human-in-the-loop required for fairness sign-off — synthetic data underestimates real bias.

### Recommended subagents
- `vui-fairness-evaluator` — runs intent + WER across demographic slices, outputs disparity report.
- `accent-test-generator` — creates SSML test phrases for accent and tempo variations.
- `accommodation-recommender` — proposes per-user adjustments (timeout, repeat prompts, visual fallback).
- `inclusive-script-rewriter` — flags idioms, slang, jargon that fail non-native speakers.

### Prompt pattern
```
For each VUI prompt, return:
- reading_grade_level (Flesch-Kincaid)
- idiom_count
- jargon_terms[]
- non_native_friendly_rewrite (if grade>8 or idioms>0)
- estimated_intent_accuracy_drop_for_non_native (low/medium/high)
Reject any prompt with grade > 8 unless required by domain (medical, legal).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whisper` / `whisper.cpp` | Multi-lingual ASR baseline for evaluation | https://github.com/ggerganov/whisper.cpp |
| `jiwer` | Compute WER, CER for ASR evaluation | `pip install jiwer` |
| `mozilla-voice-stt` (DeepSpeech successor) | OSS ASR, good for self-hosting | https://github.com/mozilla/voice-stt |
| `Common Voice` (datasets) | Mozilla open accent-diverse corpus | https://commonvoice.mozilla.org/ |
| `pyttsx3` / `edge-tts` / `gTTS` | TTS variation for synthetic test data | `pip install edge-tts` |
| `speechdiff` | Compare ASR outputs across providers | https://github.com/openai/whisper |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| AssemblyAI | SaaS | Yes (REST) | Good speaker-diarization, fairness metrics published. |
| Deepgram | SaaS | Yes | Strong accent coverage, custom-model training. |
| Speechmatics | SaaS | Yes | Industry leader on accent fairness. |
| OpenAI Whisper API | SaaS | Yes | Best general accent support; still has bias. |
| Mozilla Common Voice | OSS dataset | Yes | Public, accent-tagged voice data. |
| ElevenLabs voice library | SaaS | Yes (cloning) | Synthesize diverse accents for test corpora; respect consent. |

## Templates & scripts
Inline WER-by-segment evaluator (≤45 lines).

```python
# vui_fairness.py
import csv, sys, jiwer
from collections import defaultdict

# CSV columns: utterance_id, accent, age_group, ref_text, hyp_text
def evaluate(path: str):
    by_group = defaultdict(lambda: {"refs": [], "hyps": []})
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in ("accent", "age_group"):
                g = (key, row[key])
                by_group[g]["refs"].append(row["ref_text"])
                by_group[g]["hyps"].append(row["hyp_text"])
    overall = jiwer.wer(
        sum((v["refs"] for v in by_group.values()), []),
        sum((v["hyps"] for v in by_group.values()), []),
    )
    rows = [("group", "value", "n", "wer")]
    for (k, v), data in sorted(by_group.items()):
        wer = jiwer.wer(data["refs"], data["hyps"])
        rows.append((k, v, len(data["refs"]), round(wer, 3)))
    rows.append(("overall", "-", "-", round(overall, 3)))
    for r in rows: print("\t".join(map(str, r)))

if __name__ == "__main__":
    evaluate(sys.argv[1])
```

Disparity flag: any subgroup WER > 1.5x overall WER triggers human review.

## Best practices
- Test with real users, not just synthesized speech — clones flatten real prosody and underestimate failure.
- Default to extended ASR timeouts (3-5s after end-of-speech) for users who pause; reduce only on confirmed fast-talker profile.
- Keep grammar simple: short imperatives, no idioms, no contractions in critical instructions.
- Provide always-on visual transcript on devices that have a screen — universal benefit, not "accessibility opt-in".
- Confirm before acting on low-confidence ASR; never silently misroute.

## AI-agent gotchas
- LLMs assume English idioms work for everyone; lint and rewrite for ESL users with reading-level constraints.
- Synthetic accent test data underestimates real-world WER; complement with Common Voice or commissioned recordings.
- Confidence scores from ASR are not calibrated equally across groups — high-confidence misrecognitions happen more often for accented speech.
- Tool calls that require exact spelling (names, addresses) need spell-out fallback or visual confirmation, especially for non-native speakers.
- Human checkpoint: fairness review with at least one tester per major target accent group before launch; periodic re-evaluation when ASR provider updates.

## References
- Koenecke et al., "Racial disparities in automated speech recognition," PNAS 2020.
- W3C Accessible Voice Design notes (Working Draft, evolving).
- Common Voice open dataset and dashboards: https://commonvoice.mozilla.org/
- "Voice User Interface Design" by Cohen, Giangola, Balogh.
- ITU-T F.745 accessibility guidance for telecommunication services.
- Speechmatics fairness report: https://www.speechmatics.com/company/fairness
