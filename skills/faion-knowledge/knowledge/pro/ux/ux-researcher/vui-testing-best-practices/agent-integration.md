# Agent Integration — VUI Testing Best Practices

## When to use
- Pre-launch validation of an Alexa Skill, Google Action, or custom voice agent: stress-test intent recognition + dialog flow before certification.
- Multilingual/accent expansion: regression-test ASR accuracy and prompt naturalness across locales using batched audio fixtures.
- Continuous regression: every voice prompt or NLU model change re-runs a corpus of utterance fixtures and asserts intent + slot extraction accuracy.
- Field testing prep: scripted noise-injection runs before recruiting real users.

## When NOT to use
- Voice is a single shortcut, not a primary interface (e.g., a "tap-and-hold to speak" search): standard usability testing covers it.
- You don't yet have a working dialog model — start with Wizard-of-Oz prototyping, not test automation.
- Single-turn command testing only: an NLU benchmark (intent classification F1) is enough; a full VUI test suite is overkill.

## Where it fails / limitations
- Synthetic TTS test audio does not replicate real human prosody — accuracy numbers are optimistic versus production traffic.
- Background-noise injection in test fixtures misses physical room acoustics (reverb, multi-mic beamforming) that smart speakers actually face.
- Long-context retention bugs only surface in conversations >10 turns; most automated suites stop at 3-5.
- LLM-judges of "did the assistant respond appropriately?" are biased toward verbose, polite responses and miss curtness/friction issues.
- Privacy: voice fixtures with real PII cannot be replayed in cloud ASR — leaks customer data.

## Agentic workflow
Run a two-tier suite: (1) deterministic test cases over scripted utterance fixtures asserting intent/slot/dialog-state machine outcomes; (2) LLM-judge tier scoring response naturalness, error recovery, and goal completion against a rubric. A coordinator subagent picks which tier each test belongs in, runs them in parallel, and produces a report keyed by feature + locale + noise condition. Human reviewers sign off any LLM-judge regression before promoting to production.

### Recommended subagents
- `faion-ux-researcher-agent` — designs the test corpus (utterance variants, persona-based scenarios, edge cases).
- `faion-testing-developer` (from `free/dev/testing-developer`) — wires fixtures into pytest/jest harness, manages CI integration.
- `faion-accessibility-specialist` — reviews coverage for accent diversity, speech impairment patterns, hearing-related response cues.
- `faion-llm-integration` agent (from `geek/ai/llm-integration`) — runs the LLM-judge tier with stable rubric prompts.

### Prompt pattern
LLM-judge per turn:
```
Conversation so far: {transcript}
User utterance: "{utterance}"
Assistant response: "{response}"
Score (1-5) on: intent_match, naturalness, brevity, error_recovery.
Return JSON. Penalize if response invents facts not in {kb}.
```
Corpus generator:
```
Generate 30 phrasings of the intent "{intent}" varying formality, length, and dialect (en-US, en-GB, en-IN). Include 5 ungrammatical variants real users might say.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask` (Alexa Skills Kit CLI) | Invoke skills, run simulator, fetch logs | `npm i -g ask-cli`; https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html |
| `gactions` | Google Actions Builder CLI | https://developers.google.com/assistant/conversational/df-asdk/actions-sdk/gactions-cli |
| OpenAI Whisper / `whisper-cli` | OSS ASR for fixture transcription + comparison | `pip install openai-whisper` |
| `ffmpeg` | Mix utterance audio with ambient-noise stems for stress fixtures | distro package |
| `sox` | Pitch/speed perturbation to simulate accent/age variation | distro package |
| `pytest-voice` (custom harnesses) | Drive intent-resolution assertions in CI | n/a; build per-project |
| Voiceflow CLI | Export dialog model + test cases | https://www.voiceflow.com |
| `pyttsx3` / `gTTS` / ElevenLabs API | Synthesize test utterances at scale | `pip install pyttsx3 gtts` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Alexa Developer Console + SMAPI | SaaS | Yes — full REST API + ask-cli | Required for skill certification testing |
| Actions on Google + gactions | SaaS | Yes | Google Assistant simulator + logs |
| Voiceflow | SaaS | Yes — API for dialog export, test runs | Strong for prototype + regression suites |
| Bespoken | SaaS | Yes — CLI + Jest plugin | Voice-app testing platform; CI-friendly |
| Vocalize.ai | SaaS | Partial | Real-device farm, accent panels |
| Pulse Labs | SaaS | Partial — booked panels | Real-user voice testing recruitment |
| Rasa | OSS | Yes — full Python | Self-hosted NLU + test runner (`rasa test`) |
| OpenAI Whisper / Deepgram / AssemblyAI | OSS / SaaS | Yes | ASR ground-truthing; Deepgram has streaming API |
| ElevenLabs | SaaS | Yes — API | High-quality TTS for fixture diversity |

## Templates & scripts
See `templates.md` for the test-plan and metrics sheet. Minimal noise-injection harness:

```bash
# stress_corpus.sh — mix clean utterances with ambient noise stems at 3 SNRs
set -euo pipefail
CLEAN_DIR=fixtures/clean
NOISE_DIR=fixtures/noise   # cafe.wav, traffic.wav, tv.wav
OUT=fixtures/mixed
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

## Best practices
- Build the utterance corpus from real anonymized logs first, synthesize variants second; pure-LLM-generated corpora over-represent grammatical, in-domain phrasings.
- Track three accuracy tiers separately: ASR (word error rate), NLU (intent + slot F1), and dialog (task completion). A regression in only one tier tells you exactly where to look.
- Always include a "barge-in" test (user interrupts mid-prompt) and a "no input" test (timeout); these break dialog state machines more than utterance variation.
- Pin ASR model versions in CI — provider-side ASR upgrades silently shift WER and break tests overnight.
- For LLM-judge naturalness scoring, use pairwise comparison ("Is response A or B more natural?") not absolute 1-5 scores; pairwise is more reliable.
- Run the same suite in two locales minimum even for monolingual launches — reveals locale-leaking copy and fallback bugs.

## AI-agent gotchas
- Don't let the LLM-judge see the expected answer when scoring naturalness — anchoring bias inflates scores. Score blind, then compute correctness separately.
- ASR transcripts contain noise tokens ("[unintelligible]", "uh"); your assertion harness must normalize before exact-match. Use a fuzzy-match fallback with a logged threshold.
- Synthetic TTS used for fixtures may use the same vendor as your TTS output → false-high naturalness. Use a different TTS engine for fixtures than for product output.
- Latency: ASR + LLM judge per turn is slow. Parallelize per-test, but cap concurrency at provider rate limits or the suite hits 429s and silently passes.
- Cost: a 1000-utterance × 3-noise × 2-locale × LLM-judge sweep is non-trivial. Tier the suite: smoke (10 utterances, every commit) → full (nightly) → field-replay (release).
- Privacy: never send raw user-recorded audio to a cloud LLM judge. Transcribe first locally, redact PII, then judge the text.

## References
- Nielsen Norman Group — Testing Voice Usability: https://www.nngroup.com/articles/testing-voice-usability/
- Amazon — Test your Alexa skill: https://developer.amazon.com/en-US/docs/alexa/custom-skills/test-your-skill.html
- Google — Conversation Design: https://developers.google.com/assistant/conversational/design
- Cohen, Giangola, Balogh — *Voice User Interface Design* (Addison-Wesley)
- Pearl, Cathy — *Designing Voice User Interfaces* (O'Reilly)
- Bespoken docs — https://docs.bespoken.io/
