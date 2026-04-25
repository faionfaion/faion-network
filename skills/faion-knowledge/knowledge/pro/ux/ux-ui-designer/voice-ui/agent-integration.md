# Agent Integration — Voice UI (VUI) Design Basics

## When to use
- Designing voice features end-to-end: assistants, voice commands in apps, IVR, accessibility voice alternatives.
- Drafting sample dialogues, intents, slots, prompts, reprompts, confirmation strategy.
- Migrating legacy NLU bots (Dialogflow, Lex) to LLM-powered conversation runtimes.
- Defining voice-first error recovery and multimodal fallback.

## When NOT to use
- Visual UI work where voice is decorative — invest in core flow first.
- Highly private contexts (medical detail entry, financial account numbers) without strong auth.
- Noisy or shared environments without push-to-talk or wake-word handling.
- Browsing/exploring tasks — visual lists out-perform voice for discovery.

## Where it fails / limitations
- ASR (speech recognition) accuracy degrades with non-native accents, kids, elderly voices.
- LLM-based VUIs hallucinate confirmations ("Done!") without verifying the back-end action.
- Latency budget: total round-trip > 1.5s feels broken; LLMs typically push past it without streaming.
- Reprompts pile up if the user is interrupted by a noise — design needs barge-in handling.
- Privacy: utterance logs contain PII; retention policy must be in design, not an afterthought.
- Without a visible "ear", users don't know if the system is listening — endpointing UX is critical.

## Agentic workflow
Use a subagent to author sample dialogues from a use-case spec, then expand each dialogue into intents, slots, primary prompts, reprompt ladders, and confirmation strategy. A second agent runs Wizard-of-Oz simulation by reading typed user inputs and replying with prompt outputs, generating realistic transcripts to stress-test the design. Human review for any irreversible action prompts.

### Recommended subagents
- `faion-usability-agent` — drafts dialogues, prompts, error reprompts, confirmation matrix.
- `faion-ux-researcher-agent` — runs Wizard-of-Oz testing, accent diversity recruitment.
- `faion-sdd-executor-agent` — implements on Alexa SDK / Dialogflow CX / Rasa / OpenAI Realtime.

### Prompt pattern
```
For feature <feature>, write 3 happy-path dialogues, 2 error
dialogues, and 1 fallback dialogue. Use natural English, no
marketing tone. Mark each system turn with intent + slot table.
```

```
Given intent <name> with slots <slot list>, generate 8 utterance
variants spanning command, polite, terse, and conversational
register. List any utterance that would collide with intent <other>.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` | Alexa Skill lifecycle | `npm i -g ask-cli`; developer.amazon.com/alexa |
| `gactions` | Google Conversational Actions | developers.google.com/assistant/conversational/gactions |
| `dialogflow` (gcloud component) | Dialogflow CX agents | cloud.google.com/dialogflow/cx/docs |
| `rasa` | OSS dialogue framework | `pip install rasa`; rasa.com |
| `voice2json` | Offline NLU prototyping | voice2json.org |
| OpenAI Realtime / Whisper CLI | Streaming ASR + LLM voice | platform.openai.com/docs/guides/realtime |
| `pipecat` | Voice-agent pipeline framework | github.com/pipecat-ai/pipecat |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Alexa Skills Kit | SaaS | Yes — ASK SDK + CLI | Certification still human-gated. |
| Dialogflow CX / ES | SaaS | Yes — REST + CLI | Strong slot filling. |
| Amazon Lex v2 | SaaS | Yes — CLI + CloudFormation | Ties to AWS infra. |
| Rasa | OSS | Yes — fully scriptable | Best for self-hosted, on-prem. |
| Microsoft Copilot Studio | SaaS | Partial — REST API | Power Platform tie-in. |
| LiveKit Agents | OSS | Yes — Python SDK | Best for real-time voice agents. |
| ElevenLabs / OpenAI TTS | SaaS | Yes — REST | Voice synthesis quality bench. |
| Vapi / Retell AI | SaaS | Yes — REST | Phone-based voice agents. |

## Templates & scripts
See `templates.md` for Voice Flow + Prompt Writing templates and `examples.md` for sample dialogues. Inline minimal Rasa intent/utterance file:

```yaml
version: "3.1"
nlu:
  - intent: set_timer
    examples: |
      - set a timer for [15 minutes](duration)
      - set a [15 minute](duration) timer
      - timer [15 min](duration)
      - start a [pasta](name) timer for [10 minutes](duration)
      - countdown [90 seconds](duration)
responses:
  utter_timer_confirm:
    - text: "Timer set for {duration}, starting now."
  utter_timer_reprompt_no_input:
    - text: "How long should the timer run?"
  utter_timer_fallback:
    - text: "I didn't catch that. Try saying '15 minutes' or 'half an hour'."
```

## Best practices
- Write dialogues before intents — design follows speech, not the other way around.
- Cap a single prompt at ~14 words; long prompts get interrupted.
- Implicit confirmation ("Adding milk to your list") for low-risk; explicit for high-risk + irreversible.
- Reprompt ladder: 1) rephrase, 2) examples, 3) fallback (visual / human / alternative).
- Always include a `cancel` / `nevermind` intent at every turn.
- Stream TTS as soon as the first phrase is decided — do not wait for full response.
- Test with at least 5 accents and 2 age groups before launch.

## AI-agent gotchas
- LLMs hallucinate "Done." without verifying the action; require the agent to call the tool first, then narrate.
- Agents under-generate utterance variants — force minimum 5 across registers.
- Slot validation: agents accept anything; require a typed schema (duration: ISO8601, currency: ISO4217).
- Endpointing in LLM voice agents: agent must support barge-in or users will talk over it.
- Privacy: agent must redact PII in logged transcripts before storing.
- Confirmation drift: an LLM rephrases "place the order" softer each turn — pin the wording.

## References
- Cathy Pearl, *Designing Voice User Interfaces*, O'Reilly 2017.
- Erika Hall, *Conversational Design*, A Book Apart 2018.
- Google Conversation Design — designguidelines.withgoogle.com/conversation/
- Alexa Design Guide — developer.amazon.com/en-US/docs/alexa/alexa-design/get-started.html
- NN/g, "Voice First" research — nngroup.com/articles/voice-first/
- OpenAI Realtime API guide — platform.openai.com/docs/guides/realtime
- LiveKit Agents — docs.livekit.io/agents/
