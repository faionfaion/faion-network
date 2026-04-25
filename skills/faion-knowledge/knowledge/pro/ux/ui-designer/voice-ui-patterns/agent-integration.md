# Agent Integration — Voice UI Patterns & Guidelines

## When to use
- Designing a new voice agent (Alexa skill, Google Action, Siri Shortcut, custom GPT/Claude voice bot).
- Producing prompt copy, error ladder, and confirmation patterns from a feature spec.
- Auditing an existing voice flow against NNG / Google / Amazon design guidelines.
- Generating multimodal (voice + screen) flows for displays — Echo Show, Pixel Tablet, Apple CarPlay.

## When NOT to use
- Pure text chatbot (no audio); use chatbot conversation-design playbooks instead.
- IVR with regulatory script requirements (banking, healthcare); legal-mandated wording overrides UX guidance.
- Pre-product validation phase — design utterances on real user data, not on imagined scripts.
- Languages with limited TTS quality where prosody coaching is futile.

## Where it fails / limitations
- LLM-generated prompts skew long and polite; users zone out after 15 seconds.
- Prosody / SSML coverage varies wildly across platforms (Siri ignores most SSML).
- Privacy: shipping real conversation transcripts to an LLM for "improvement" risks PII leakage.
- Cross-cultural prosody norms (politeness, directness) need native speakers, not auto-translation.
- Latency reality (1–3 s round trip) is invisible at design time; agent-designed turn lengths often miss the mark.

## Agentic workflow
Use Claude as a "voice pattern librarian" that turns an intent spec into a full conversation graph: greeting, prompt copy, slot capture, confirmation, error ladder (3 steps), help, exit, repeat. A second linter pass scores each utterance on length (≤ 8 s), blame-free framing, example presence, and platform compliance. Output is exported as Voiceflow JSON, Alexa Skills Kit interaction model, or Dialogflow agent. Real-data improvement loop: anonymized analytics feed a "rotate variants" job that swaps fresh utterances when retention drops.

### Recommended subagents
- `general-purpose` Claude subagent — full conversation graph synthesis.
- `faion-sdd-executor-agent` — implement SDD tasks for the voice agent backend.
- A "voice-copy-reviewer" prompt — score / rewrite copy against length + tone rules.
- `faion-improver` skill — sustain weekly improvement loop on retention metrics.

### Prompt pattern
```
Intent: order_pizza, slots=size,toppings,address.
Platform: Alexa Skills Kit.
Output: full conversation graph JSON (greeting, slot fills with reprompts,
confirmation, success ack, error ladder x3, help, exit) — each utterance
labeled with est_seconds and intent variants.
```

```
Audit this Voiceflow export for:
- prompts > 8 s spoken
- repeat utterances across error steps
- missing exit affordance
- intents lacking help phrase
Return list with severity.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` (Alexa Skills Kit CLI) | Author + simulate Alexa skills | `npm i -g ask-cli` |
| `gactions` | Google Actions / Conversational Actions | https://developers.google.com/assistant |
| `dialogflow` (gcloud) | Dialogflow CX agents from CLI | https://cloud.google.com/dialogflow |
| `voiceflow` API | Export / version conversation graphs | https://www.voiceflow.com/api |
| `rasa shell` / `rasa test` | Test OSS NLU + policy routing | `pip install rasa` |
| `botium-cli` | Cross-platform conversational regression | `npm i -g botium-cli` |
| ElevenLabs / Azure Speech CLI | Generate spoken samples for prosody review | https://elevenlabs.io/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Voiceflow | SaaS | Yes (REST API) | Best authoring + agent target |
| Amazon Alexa Developer Console | SaaS | Yes (ASK CLI) | Required for Alexa launch |
| Google Dialogflow CX | SaaS | Yes (gRPC API) | Rich state machine |
| Apple Siri / SiriKit | OS framework | Limited | Intents extension only |
| Rasa Open Source | OSS | Yes (REST + CLI) | Self-hosted, full control |
| Botpress | OSS + SaaS | Yes (CLI + REST) | LLM-native chatbot platform |
| Botium | OSS + SaaS | Yes | Conversational regression testing |
| Dashbot / VoiceLabs | SaaS analytics | Yes (export API) | Mine retention + drop-off |

## Templates & scripts
See `templates.md` for conversation-graph schema. Inline copy linter:

```python
#!/usr/bin/env python3
# vui_lint.py — score voice copy against guidelines
import json, re, sys
WPM = 150
BLAME = re.compile(r"\b(you (didn'?t|forgot|need to|must)|wrong)\b", re.I)

def secs(t): return len(t.split()) / WPM * 60

issues = []
for node in json.load(sys.stdin)["nodes"]:
    for u in node.get("utterances", []):
        if secs(u) > 8: issues.append(f"long ({secs(u):.1f}s) [{node['id']}]: {u}")
        if BLAME.search(u): issues.append(f"blames user [{node['id']}]: {u}")
    if node["type"] == "error" and "say " not in (node.get("hint") or "").lower():
        issues.append(f"error node {node['id']} lacks example phrase")
sys.exit("\n".join(issues) or 0)
```

## Best practices
- One idea per turn; if there are two, ask twice or show on screen.
- Vary reprompts — never identical at step 2 and step 3.
- Confirm only high-stakes actions (money, deletion); low-stakes get implicit ack.
- Provide an "escape hatch" exit on every node — users must always know how to quit.
- Localize prosody, not just words — politeness and pacing vary by language.
- Track per-node abandonment; > 30% means the prompt fails users, not vice versa.

## AI-agent gotchas
- Claude defaults to verbose, apologetic tone — explicitly bound max words and ban "I'm so sorry" repetition.
- Generated SSML may include tags rejected by target platform; validate against the platform's SSML spec.
- LLMs invent example cities / names from a tiny pool ("New York", "John") — force diversity in the prompt.
- Don't auto-deploy voice copy; one bad line lands on millions of devices instantly. Stage rollouts.
- PII in transcripts must be redacted before any LLM analysis call; build a sanitizer step.
- Multimodal prompts (voice + screen) easily fall out of sync; keep canonical pairs in JSON, not parallel docs.

## References
- https://designguidelines.withgoogle.com/conversation/
- https://developer.amazon.com/en-US/docs/alexa/alexa-design/get-started.html
- https://www.nngroup.com/articles/voice-ux/
- Cathy Pearl, *Designing Voice User Interfaces* (O'Reilly, 2016)
- Erika Hall, *Conversational Design* (A Book Apart, 2018)
- https://abookapart.com/products/conversational-design
- VoiceFirst.fm podcast archive
