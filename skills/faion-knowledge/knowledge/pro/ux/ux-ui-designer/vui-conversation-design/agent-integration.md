# Agent Integration — VUI Conversation Design

## When to use
- Building Alexa Skills, Google Actions, Siri shortcuts, or custom voice assistants on top of LLMs.
- Designing IVR replacements with intent + entity routing (banking, support, scheduling).
- Hands-busy / eyes-busy contexts: cooking, driving, factory floor, surgery, accessibility.
- Adding a voice channel to an existing chatbot — the dialog model differs significantly from text.
- LLM-powered conversational agents that need a deterministic dialog skeleton on top of free-form generation.

## When NOT to use
- Privacy-sensitive flows (passwords, medical results) where overheard speech is unacceptable.
- High-precision input (URLs, codes, IDs longer than ~6 chars) — voice degrades sharply.
- Markets with low ambient assistant adoption — discovery and habit formation cost outpaces value.
- Tasks requiring visual scanning (tables, comparison shopping, long lists).

## Where it fails / limitations
- ASR error rate compounds across turns; after 3 turns, end-to-end success can drop below 70% in noisy environments.
- Long prompts and confirmations destroy conversational flow; users tune out after ~15 seconds of TTS.
- Cultural/accent bias in commercial ASR (Google, Whisper, Deepgram) silently degrades non-mainstream-English speakers.
- Wake word false positives leak audio to cloud — privacy/regulatory concern in EU and healthcare.
- Multi-turn LLM dialog forgets entities mid-conversation when context window is naive — you need explicit state, not "the model will remember."

## Agentic workflow
Treat conversation design as a state machine the agent both authors and tests. Subagents draft intents/entities/prompts, generate dialog flow YAML, simulate user variants (terse/verbose/non-native/interrupted), and produce regression turns. A human owns voice-and-tone style and the final TTS samples — agents can't hear cadence.

### Recommended subagents
- `faion-ux-researcher-agent` — recruits and scripts moderated voice studies, writes WoZ (Wizard of Oz) protocols.
- `faion-usability-agent` — runs heuristic review against Google Conversation Design Principles + Alexa Design Guide.
- `faion-sdd-executor-agent` — implements dialog state machine + intent handlers from approved spec.

### Prompt pattern
```
Draft a dialog spec for intent: <intent_name>.
Output YAML:
  intent: <name>
  entities: [{name, type, prompt, reprompt, confirmation}]
  happy_path: [turns]
  edge_cases:
    missing_entity: [...]
    ambiguous_value: [...]
    no_input: [...] (3 reprompts then graceful exit)
    no_match: [...] (escalation after 2)
  confirmation_strategy: implicit|explicit|none
  max_turns: <int>
  timeout_seconds: <int>
Ground every prompt ≤12 spoken words. No invented entities.
```

```
Generate 20 paraphrases per intent for training data.
Vary: formality, dialect, interruption style, partial utterances.
Mark: {clean | with_filler | corrected_self}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` | Alexa skill scaffold, deploy, test | https://developer.amazon.com/en-US/docs/alexa/smapi/ask-cli-intro.html |
| `gactions` | Google Action build/deploy/simulate | https://developers.google.com/assistant/conversational/build/projects |
| `rasa` | OSS NLU + dialog management with CLI training/eval | https://rasa.com/docs/ |
| `whisper` / `whisperx` | OSS ASR for voice corpus transcription | https://github.com/openai/whisper |
| `sox` / `ffmpeg` | Voice sample normalization, noise injection for robustness tests | https://sox.sourceforge.net |
| `say` (macOS) / `espeak` (Linux) | Quick TTS for prototyping prompts | built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Voiceflow | SaaS | Yes — REST + design API | Strong agentic export (JSON spec). |
| Botpress | OSS + SaaS | Yes | LLM-native, self-hostable. |
| Rasa | OSS | Yes | Best for on-prem / regulated. |
| Dialogflow CX | SaaS | Yes | State-based; integrates with Vertex AI. |
| Amazon Lex | SaaS | Yes | AWS-native; good for IVR replacement. |
| Deepgram / AssemblyAI | SaaS ASR | Yes (REST) | Better than Whisper for streaming + diarization. |
| ElevenLabs / PlayHT | SaaS TTS | Yes | Voice cloning; persona consistency for branded VUI. |

## Templates & scripts
See `templates.md` for dialog flow YAML and prompt-design table. Inline state machine validator:

```python
# dialog_lint.py — flag missing reprompts and unbounded loops
import yaml, sys
spec = yaml.safe_load(open(sys.argv[1]))
errs = []
for intent in spec["intents"]:
    if not intent.get("max_turns"):
        errs.append(f"{intent['intent']}: missing max_turns cap")
    for ent in intent.get("entities", []):
        if not ent.get("reprompt"):
            errs.append(f"{intent['intent']}.{ent['name']}: no reprompt")
    if "no_input" not in intent.get("edge_cases", {}):
        errs.append(f"{intent['intent']}: missing no_input handling")
for e in errs: print(e)
sys.exit(1 if errs else 0)
```

## Best practices
- Implicit confirmation > explicit. "5-minute timer started" beats "Did you want a 5-minute timer? Yes or no?"
- Cap reprompts at 3, then graceful exit with channel-switch offer ("I'll text you a link").
- Variable prompts beat fixed prompts after turn 2 — repetition kills perceived intelligence.
- Design for barge-in: users will interrupt long TTS; if your stack can't handle it, shorten everything.
- Voice + visual (multi-modal) flows need separate scripts. A great voice prompt is a terrible screen prompt.
- Test with kitchen-noise, traffic, and a partner-talking-nearby — silent-room ASR scores are vanity numbers.

## AI-agent gotchas
- LLMs over-confirm. Every "Just to confirm…" turn is a tax; force the agent to justify each one.
- Generated paraphrase corpora cluster around the LLM's own register, missing dialect and code-switching. Augment with real voice logs.
- Do not let an LLM generate the wake word or branded voice persona unsupervised — TTS pronunciation lands wrong on syllable stress.
- Dialog state must be explicit (slot-filling, frame), not "in the prompt." Long-context models fake competence and then drop entities at turn 5.
- Privacy: do not pipe raw user audio into a cloud LLM without redaction; strip names, account numbers, PHI before logging.
- Streaming ASR partial results trigger premature LLM responses if you don't gate on `is_final`. Pin a stability threshold.

## References
- Pearl, *Designing Voice User Interfaces* (O'Reilly, 2016).
- Cohen, Giangola, Balogh, *Voice User Interface Design* (2004) — still the canonical IVR text.
- Google, *Conversation Design Principles*. https://developers.google.com/assistant/conversation-design/welcome
- Amazon, *Alexa Design Guide*. https://developer.amazon.com/en-US/docs/alexa/alexa-design/get-started.html
- Nielsen Norman Group, *Voice Interaction*. https://www.nngroup.com/articles/voice-interaction/
- Anthropic, *Building Voice Agents with Claude* — current best-practice guide for LLM-powered VUI.
