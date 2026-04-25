# Agent Integration — VUI Conversation Design

## When to use
- Designing intent-based dialog flows for Alexa, Google Assistant, IVR systems, or in-app voice features.
- Authoring happy-path + repair branches (missing entity, ambiguous entity, no-match, no-input) for a single user goal.
- Producing prompt copy in different prompt classes (open, directed, option, confirmation) and tagging it for analytics.
- Migrating a chatbot script to voice, where prosody, brevity, and turn-taking change the design.

## When NOT to use
- LLM-only "freestyle" conversation where intents and slots are not pre-defined — that needs different methodology (RAG-driven dialog, agentic conversation).
- Pure GUI form-filling — no turn-taking benefits from VUI design patterns.
- Asynchronous chat (email, ticketing) where wait times remove the real-time turn-taking constraint.
- One-shot voice commands with no follow-up (smart-home toggle), where dialog flow is degenerate.

## Where it fails / limitations
- Methodology assumes intent+entity NLU; LLM-based open-domain dialog needs different scaffolding (function-calling, tool use, state tracking).
- Wake-word and barge-in design depend on platform capability flags not covered here.
- Confirmation prompts ("Is that correct?") feel robotic when overused; methodology does not specify when to skip implicit confirmation.
- No coverage of latency, prosody, or SSML — yet those determine whether a perfect dialog graph sounds natural.
- Disambiguation depth grows quickly; methodology does not bound how many clarification turns before falling back to human/agent.

## Agentic workflow
Pair a deterministic dialog graph with an LLM only at edges that benefit from generation: paraphrasing prompts, generating disambiguation alternatives, classifying low-confidence inputs. Keep state in code (intent, slot map, last_prompt_class), not in the LLM. Pipeline: (1) `flow-author` drafts the canonical graph from a goal spec, (2) `prompt-writer` produces 3-5 variants per node tagged by class, (3) `repair-coverage-checker` enumerates missing repair paths, (4) `dialog-runner` executes the graph at runtime, calling LLMs only on no-match/disambiguation.

### Recommended subagents
- `flow-author` — sonnet; from {intent, slots, success_criteria} produces a happy + repair graph as JSON.
- `prompt-writer` — haiku; emits 3-5 utterance variants per prompt class, tagged for A/B selection.
- `repair-coverage-checker` — sonnet; lints a graph for missing no-match, no-input, max-retry, and escape-to-human transitions.
- `disambiguator` — sonnet; on low-confidence runtime input, proposes a clarifying prompt grounded in current slots.
- `barge-in-policy` — haiku; decides if the system should pause TTS when the user starts speaking, given utterance class.

### Prompt pattern
```
You are repair-coverage-checker. Given <flow_json>, verify each prompt node has:
- a no-match transition (and a max-retry escalation)
- a no-input transition with timeout
- an escape-to-human path within 3 retries
- confirmation for any destructive action.
Output JSON: {missing:[{node_id, defect}], escalation_paths:[...]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` v2 | Build/test Alexa skills, simulate intents | developer.amazon.com/docs/smapi/ask-cli-intro.html |
| `gactions` | Google Assistant Conversational Actions (where still available) | developers.google.com/assistant |
| `voiceflow-cli` | Sync Voiceflow projects, dialog JSON export | github.com/voiceflow/voiceflow-cli |
| `rasa` CLI | Train/test OSS NLU + dialog policy | rasa.com/docs/rasa |
| `botpress` CLI | OSS conversation studio | botpress.com/docs |
| `azure-bot-cli` | Bot Framework Composer projects | learn.microsoft.com/azure/bot-service |
| `pipecat` | Realtime voice agent framework (LLM + ASR + TTS) | github.com/pipecat-ai/pipecat |
| `livekit-cli` | Realtime audio infra for voice agents | docs.livekit.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Voiceflow | SaaS | Yes — REST | Visual dialog builder, agent-friendly export |
| Amazon Lex / Connect | SaaS | Yes — REST/boto3 | IVR + chat; intent + slot model |
| Google Dialogflow CX | SaaS | Yes — REST | State-machine dialogs |
| Rasa Open Source | OSS | Yes — Python SDK + CLI | Self-host, full state control |
| Botpress | OSS + SaaS | Yes — REST | Studio editor + LLM blocks |
| Azure Bot Framework | SaaS | Yes — REST | Composer + adaptive dialogs |
| Pipecat / Vapi / Retell | SaaS/OSS | Yes — APIs | LLM-first realtime voice agents (different paradigm) |
| ElevenLabs / Azure Neural TTS / OpenAI TTS | SaaS | Yes — REST | Render prompts to audio for review |

## Templates & scripts
See `templates.md` for prompt-class palettes. Repair coverage check (TS):

```ts
// repair_check.ts — flag dialog nodes missing required transitions
type Node = { id: string; transitions: { trigger: string; to: string }[]; class?: "open"|"directed"|"option"|"confirm"; destructive?: boolean };
const REQUIRED = ["no-match", "no-input", "max-retry"];

export function lintFlow(nodes: Node[]): {node_id: string; defect: string}[] {
  const issues: {node_id: string; defect: string}[] = [];
  for (const n of nodes) {
    const triggers = new Set(n.transitions.map(t => t.trigger));
    for (const r of REQUIRED) {
      if (!triggers.has(r)) issues.push({ node_id: n.id, defect: `missing:${r}` });
    }
    if (n.destructive && !triggers.has("explicit-confirm")) {
      issues.push({ node_id: n.id, defect: "destructive-without-confirm" });
    }
  }
  return issues;
}
```

## Best practices
- Write the happy path last. Authoring no-match, no-input, and barge-in first forces honest design and exposes ambiguity early.
- Cap retries at 3 on any node; the 3rd no-match transitions to human or alternative modality (text fallback, app deep link).
- Use implicit confirmation for low-stakes ("Set timer for 5 minutes.") and explicit confirmation only for destructive/irreversible actions.
- Vary prompt copy on retry — repeating the same wording feels broken. Maintain at least 3 variants per node and rotate.
- Tag every prompt with class + intent + retry-count for analytics; without this you cannot measure where the dialog fails.
- Keep slot prompts directed when the entity space is large ("What city?") and option-style only when ≤ 4 options.
- Never break the user's mental model on barge-in. If the user interrupts mid-prompt with a relevant utterance, accept it; if irrelevant, gracefully resume.

## AI-agent gotchas
- LLMs producing dialog flows skip "no-input" and "max-retry" transitions reliably. Run `repair-coverage-checker` on every draft.
- Function-calling models confuse intent boundaries when slots are filled across turns; always echo the consolidated slot state into the next prompt.
- TTS-rendered prompts often need rewriting that reads-fine but speaks-fine. Render variants and listen — agents cannot self-evaluate prosody.
- Avoid LLM-generated unbounded paraphrases at runtime — they drift in tone and length. Pre-generate 3-5 vetted variants offline and rotate.
- For LLM-first realtime agents (Pipecat, Vapi), classical intent/slot design still helps shape system prompts; do not throw it out.
- Disambiguation with LLMs can over-clarify. Cap at one clarification turn; on the second ambiguous input, fall back to a directed prompt or human.
- Confidence thresholds for ASR are noisy. Calibrate per-locale; the same model ID has different confidence distributions in EN vs UA vs RU.

## References
- Cathy Pearl, "Designing Voice User Interfaces" (O'Reilly).
- Google Conversation Design — developers.google.com/assistant/conversation-design/welcome.
- Amazon Alexa Design Guide — developer.amazon.com/docs/alexa/alexa-design/get-started.html.
- Nielsen Norman Group — "Voice Interaction UX" (nngroup.com/articles/voice-interaction/).
- A List Apart — "All Talk and No Buttons: The Conversational UI" (alistapart.com).
- "Conversational AI: Dialogue Systems" — Jurafsky & Martin, Speech and Language Processing, ch. on dialog.
