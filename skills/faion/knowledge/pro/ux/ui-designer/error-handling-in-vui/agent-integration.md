# Agent Integration — Error Handling in VUI

## When to use
- Designing the reprompt / fallback ladder for an Alexa, Google Action, Siri, or custom voice agent.
- Auditing an existing voice flow that has high "no-match" or drop-off rates.
- Generating per-intent escalation rules (1st / 2nd / 3rd error) before handing off to ASR/NLU engineers.
- Writing varied error utterances to escape the "same message every time" anti-pattern.

## When NOT to use
- Pure text chatbot — use chatbot conversation-design playbooks; voice acoustics don't apply.
- IVR menu where the business mandates rigid DTMF — error recovery is structural, not conversational.
- One-shot voice commands ("Hey X, lights off") with no follow-up state — error path is just a beep + silence.
- Pre-MVP product without real utterance data — you'll over-design errors that never fire.

## Where it fails / limitations
- Agent has no acoustic ground truth; it cannot predict what real users actually mis-say.
- Generated reprompts often violate platform character / time limits (Alexa 8s, Google 60s).
- LLMs default to apologetic, verbose language that bloats reprompts past the 15-second attention cliff.
- Localized error variants need native-speaker review; literal translation breaks prosody.
- Privacy: shipping raw error logs to an agent for analysis can leak PII captured by ASR.

## Agentic workflow
Use Claude as a "reprompt designer" that takes an intent spec and generates a 3-step escalation ladder, multiple utterance variants per step, and the platform-specific schema (Alexa Reprompt, Dialogflow follow-up event, custom JSON). A separate evaluator pass checks each utterance against length / tone / blame-the-user rules. Real conversation logs (anonymized) feed a periodic "reprompt rotation" job that swaps in fresh variants when a step's repeat-rate exceeds threshold.

### Recommended subagents
- `general-purpose` Claude subagent — generate reprompt ladders + variant pools.
- A "voice-copy-reviewer" specialized prompt — score each utterance on concision, blame-free framing, and time-to-speak.
- `faion-sdd-executor-agent` — execute the SDD task that wires the new error flow into the bot's intent handler.

### Prompt pattern
```
Intent: book_flight, slot=destination_city.
Output 3-step ladder. Each step: 2 utterance variants, max 8s spoken,
no blame, must end with an example.
Format: JSON {step, variant, text, est_seconds}.
```

```
Audit these 12 reprompts (input below). For each, return:
{too_long: bool, blames_user: bool, missing_example: bool, suggested_rewrite}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` (Alexa Skills Kit CLI) | Deploy + simulate skills, inspect reprompts | `npm i -g ask-cli` |
| `gactions` | Google Actions CLI for conversational flows | https://developers.google.com/assistant/conversational/quickstart |
| `dialogflow-cli` (community) | Dialogflow ES/CX intent + fallback management | https://github.com/googleapis/nodejs-dialogflow |
| `rasa shell` / `rasa test` | Test fallback policies for OSS NLU | `pip install rasa` |
| `voiceflow-cli` | Export / lint Voiceflow conversation graphs | https://www.voiceflow.com/api |
| `ffprobe` | Measure spoken-duration of generated TTS WAV | `apt install ffmpeg` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Voiceflow | SaaS | Yes (REST API) | Author + version reprompt ladders |
| Botium / Botium Box | OSS + SaaS | Yes | Automated regression tests for error paths |
| Dashbot / VoiceLabs | SaaS analytics | Yes (export API) | Mine "no-match" hotspots, feed back to agent |
| Amazon Alexa Developer Console | SaaS | Yes (ASK CLI) | Production deployment + interaction-model dialect |
| Google Dialogflow CX | SaaS | Yes (gRPC API) | Rich fallback / event handlers |
| Rasa Open Source | OSS | Yes (CLI + REST) | Self-hosted; full control of fallback policy |
| Speechly | SaaS (acquired by Roblox 2024) | Limited | Avoid for new projects |
| ElevenLabs / Azure TTS | SaaS | Yes | Generate spoken samples to validate prosody |

## Templates & scripts
See `templates.md` for the 3-step ladder JSON schema. Inline length checker:

```python
#!/usr/bin/env python3
# reprompt_lint.py — fail CI if any reprompt > 8s spoken or blames user
import json, re, sys
WPM = 150  # average TTS pace
BLAME = re.compile(r"\b(you (didn'?t|forgot|need to|must)|wrong)\b", re.I)

def seconds(text: str) -> float:
    return len(text.split()) / WPM * 60

errors = []
for step in json.load(sys.stdin):
    s = seconds(step["text"])
    if s > 8:
        errors.append(f"too long ({s:.1f}s): {step['text']}")
    if BLAME.search(step["text"]):
        errors.append(f"blames user: {step['text']}")
    if "say " not in step["text"].lower() and step.get("step") >= 2:
        errors.append(f"step{step['step']} missing example: {step['text']}")
sys.exit("\n".join(errors) or 0)
```

## Best practices
- Three strikes max — escalate to human / visual / quit; never loop forever.
- Vary the second and third reprompt; identical retries train users to leave.
- Always include one concrete example phrase by step 2.
- Acknowledge the system's failure ("I'm having trouble"), not the user's speech.
- A/B test reprompts by intent; success rate, not aesthetic preference, is the gate.
- Track per-step abandonment in analytics — anything > 30% means the prompt is wrong.

## AI-agent gotchas
- LLM-generated reprompts trend long and polite; enforce a max-words rule in the prompt.
- "I'm sorry" repeated in every step erodes trust — cap at one apology in the ladder.
- Agent will invent SSML tags that some platforms reject (e.g., Siri ignores most SSML); validate against target.
- Sending raw user logs to an external API to "improve reprompts" is a privacy hazard — anonymize first.
- Agents tend to repeat the same example city/name; force diversity in the prompt or rotate at runtime.
- Do not let an agent auto-deploy reprompt updates; require human approval and staged rollout — one bad copy line lands on millions of speakers instantly.

## References
- https://www.nngroup.com/articles/voice-error-handling/
- https://designguidelines.withgoogle.com/conversation/conversation-design/error-handling.html
- https://developer.amazon.com/en-US/docs/alexa/alexa-design/error-handling.html
- Cathy Pearl, *Designing Voice User Interfaces* (O'Reilly, 2016)
- Erika Hall, *Conversational Design* (A Book Apart, 2018)
