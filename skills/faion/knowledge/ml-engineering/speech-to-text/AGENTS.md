# Speech-to-Text Integration

## Summary

**One-sentence:** Picks an STT provider (OpenAI Whisper, GPT-4o Transcribe, AssemblyAI, Deepgram, ElevenLabs Scribe, faster-whisper local) by use case (batch vs streaming) and ships a typed transcription service with timestamps + diarization + custom vocab.

**One-paragraph:** Modern STT APIs differ 10-20× on latency (150 ms vs 5 s), accuracy (WER), language support (30-125 languages), and cost ($0.002-$0.04/min). Choosing wrong burns budget or misses accuracy. Real-time captioning needs ≤300ms latency (ElevenLabs Scribe, Deepgram); batch transcription tolerates seconds (Whisper); self-hosted faster-whisper breaks even at ≈500 hours/month. The pattern: declare use-case constraints → pick provider → wire typed `Transcript {text, segments[], speakers[]?, confidence}` → add custom-vocabulary boost where domain words matter → stream OR batch by SLO.

**Ефективно для:**

- Meeting / podcast / video indexing — batch Whisper або GPT-4o Transcribe з timestamps вистачає; цінник $0.003-0.006/min.
- Real-time captioning та voice commands — ElevenLabs Scribe (150ms) або Deepgram Nova (200ms).
- Industry-specific vocabulary (medical, legal, finance) — custom-vocab boost у Deepgram або AssemblyAI знижує WER 20-40%.
- High-volume (≥500h/month) — self-host faster-whisper економить 60-80% проти cloud.

## Applies If (ALL must hold)

- Feature requires turning audio into text (commands, captions, transcripts)
- Audio quality ≥ 8 kHz mono (lower → fix recording first, no provider fixes garbage in)
- Language is in the chosen provider's supported list

## Skip If (ANY kills it)

- Audio is synthetic TTS output — transcribe the source text instead
- Language not in any provider's list — bail, no point picking
- Cost prohibitive AND no GPU available for local — re-scope feature

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `use-case-constraints.yaml` | YAML | product/PM (real-time vs batch, max latency, WER target) |
| `audio-samples-eval/` | folder of WAV / MP3 | 30-min representative clip per language |
| `monthly-volume-hours.json` | JSON | finance / analytics estimate |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `text-to-speech` | Often paired in voice-agent stack |
| `cost-optimization` | Provider pricing comparison |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: latency-bucket provider pick, custom-vocab discipline, WER eval gate, self-host break-even, output schema | 1100 |
| `content/02-output-contract.xml` | essential | `stt-config.yaml` schema + `Transcript` JSON shape | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: real-time on Whisper, no custom vocab, no WER eval, hard-coded provider, missing diarization fallback | 900 |
| `content/04-procedure.xml` | essential | 5 steps: scope use case → bench providers → pick → wire fallback → ship + monitor | 700 |
| `content/05-examples.xml` | essential | Worked example: support-call transcription with Deepgram + custom medical vocab | 500 |
| `content/06-decision-tree.xml` | essential | Routes by latency + privacy + volume to provider | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audio_sample_bench` | n/a (deterministic) | WER computation |
| `provider_compare_drafting` | sonnet | Trade-off analysis |
| `stt_config_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/transcription-api.py` | OpenAI Whisper batch call with timestamps |
| `templates/transcription-service.py` | FastAPI service wrapping AssemblyAI streaming |
| `templates/stt-config.schema.yaml` | Schema for stt-config.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable stt-config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-speech-to-text.py` | Lint stt-config.yaml | Pre-commit |

## Related

- [[text-to-speech]] — paired in voice agents
- [[tool-use-function-calling]] — STT often feeds tool-calling LLM
- external: [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text) · [Deepgram Nova-2](https://deepgram.com/) · [AssemblyAI](https://www.assemblyai.com/) · [faster-whisper](https://github.com/SYSTRAN/faster-whisper)

## Decision tree

See `content/06-decision-tree.xml`. Branches by latency requirement, privacy, monthly volume → {Whisper batch, GPT-4o Transcribe, Deepgram, AssemblyAI, ElevenLabs Scribe, faster-whisper local}.
