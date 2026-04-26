# Agent Integration — Core VUI Design Principles

## When to use
- Designing voice-first features (Alexa/Google Assistant skills, IVR menus, in-car voice, accessibility voice nav).
- Adding voice input/output to multimodal apps where the LLM both listens and speaks.
- Auditing existing voice flows for verbosity, missing context tracking, or unnatural phrasing.
- Generating prompt/response copy for an agent's text-to-speech layer where SSML, pacing, and turn-taking matter.

## When NOT to use
- Pure GUI/keyboard apps where voice is not a modality — visual hierarchy guidance lives elsewhere.
- Backend-only agents with no spoken output (chat-text agents need conversation design, not VUI principles per se).
- One-shot transactional bots where users never have a follow-up turn — these need scripts, not principles.

## Where it fails / limitations
- Principles are platform-agnostic; they do not encode Alexa-specific certification rules or Google Assistant policy gates.
- "Natural conversation" is locale/culture-bound — guidance assumes English/Western norms; idioms in UA/RU/PT need re-tuning.
- Context awareness requires session/state infrastructure outside the principles themselves; principles will be silently violated if the runtime drops state.
- No coverage of latency budgets — principles say "be brief" but not "<800 ms first token" which actually matters for perceived naturalness.

## Agentic workflow
Use a single specialist subagent that takes a user goal plus dialog turn history and emits the next system utterance plus a short rationale tagged against the three principles. Keep the agent stateless — pass full turn context in each invocation. For larger flow design, run a planner agent that drafts a happy path and 2-3 repair branches, then a critic agent that scores each utterance against simplicity/naturalness/context with concrete edits.

### Recommended subagents
- `vui-copywriter` — sonnet; rewrites system utterances for brevity, natural phrasing, follow-up offers.
- `vui-critic` — sonnet; reviews dialog turns against the three principles and flags violations with line refs.
- `dialog-flow-designer` — sonnet; produces happy/repair/disambiguation branches from a single intent spec.

### Prompt pattern
```
You are vui-copywriter. Rewrite the system response below to satisfy:
(1) Simplicity — drop redundant phrasing, units, timestamps unless asked.
(2) Naturalness — sound like a person, offer one helpful follow-up.
(3) Context — refer back to <last_user_turn> implicitly, do not restate it.
Return JSON: {utterance, rationale, removed_words}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` (Amazon Alexa Skills Kit CLI v2) | Scaffold/deploy/test Alexa skills, simulate utterances | `npm i -g ask-cli` · developer.amazon.com/docs/smapi/ask-cli-intro.html |
| `gactions` (Google Actions Builder CLI) | Deploy Conversational Actions, run preview | `gcloud components install gactions` · developers.google.com/assistant/conversational/build/projects |
| `voiceflow-cli` | Sync Voiceflow projects, export dialog JSON | `npm i -g @voiceflow/cli` · github.com/voiceflow/voiceflow-cli |
| `bspeech` / Azure `speech-cli` | TTS/STT round-trip testing for utterance pacing | docs.microsoft.com/azure/cognitive-services/speech-service/spx-overview |
| `ffmpeg` + `sox` | Measure response audio length, gaps, peak level | ffmpeg.org / sox.sourceforge.net |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Voiceflow | SaaS | Yes — public API, project export JSON | Visual dialog builder; agents can mutate flows via `/v2/projects` |
| Amazon Alexa (ASK) | SaaS | Yes — SMAPI REST | Certification gates require human-in-loop |
| Google Assistant Actions Builder | SaaS (sunset for new in 2024 except for select partners) | Limited — gactions CLI | Check current availability before committing |
| Rasa Open Source | OSS | Yes — REST + Python SDK | Self-hosted, full control over NLU+dialog policy |
| ElevenLabs / OpenAI TTS / Azure Neural TTS | SaaS | Yes — REST | Test how copy actually sounds; SSML support varies |
| Botpress | OSS + SaaS | Yes — Studio API | Conversation design with branchable flows |

## Templates & scripts
See `templates.md` for prompt/response skeletons. Quick utterance linter:

```python
# vui_lint.py — flag verbose/unnatural lines
import re, sys, json

LIMITS = {"chars": 120, "clauses": 2, "absolutes": ("successfully", "currently", "in your local timezone")}

def lint(text: str) -> list[str]:
    issues = []
    if len(text) > LIMITS["chars"]:
        issues.append(f"too-long:{len(text)}")
    if text.count(",") + text.count(";") + 1 > LIMITS["clauses"]:
        issues.append("too-many-clauses")
    for word in LIMITS["absolutes"]:
        if word in text.lower():
            issues.append(f"filler:{word}")
    if not re.search(r"[?.!]$", text):
        issues.append("missing-terminal-punctuation")
    return issues

if __name__ == "__main__":
    data = json.load(sys.stdin)  # {"turns":[{"role":"system","text":"..."}]}
    for i, t in enumerate(data["turns"]):
        if t["role"] == "system":
            problems = lint(t["text"])
            if problems:
                print(f"turn {i}: {problems}")
```

## Best practices
- Co-author every system utterance with a TTS preview — text that reads fine often sounds wrong; latency between user end-of-speech and first audio matters more than utterance length.
- Encode the three principles as evaluator rubrics in a JSON schema, not free-form review — agents apply them more reliably with `{simplicity:0..3, naturalness:0..3, context:0..3}`.
- Track explicit dialog-state slots (intent, last_entity, pending_confirmation) in agent context; never reconstruct from utterance history alone — it drifts.
- Keep VUI copy in a versioned content repo separate from code — designers iterate without merge conflicts; agents fetch latest at runtime.
- Build a small "ground-truth" set of 30-50 representative dialog snippets and run any new prompt/model change against it before promoting.

## AI-agent gotchas
- LLMs love filler ("Just to confirm...", "I'd be happy to..."). Add a stop-list to the system prompt or post-process — the model will not self-edit reliably.
- Context-awareness regressions are silent: the agent answers but ignores prior turn. Always include the last 3-5 turns verbatim in the prompt and assert the response references at least one entity from them.
- Disambiguation prompts ("5 minutes or 5 hours?") are easy to skip when the model is over-confident. Force the model to emit a `confidence` score and route low-confidence to a clarification agent.
- Never let the LLM both decide "is auth required?" and "speak the response" in one call for sensitive operations — split into a policy agent and a response agent (see vui-privacy-security).
- TTS engines mispronounce brand names and codes. Maintain an SSML lexicon side-file; agents must wrap proper nouns with `<phoneme>` or `<sub>` tags before sending to TTS.
- Avoid asking the model to count words/characters — it is unreliable. Enforce length limits in code post-generation.

## References
- Cathy Pearl, "Designing Voice User Interfaces" (O'Reilly, 2016).
- Google Conversation Design — designguidelines.withgoogle.com/conversation/.
- Amazon Alexa Design Guide — developer.amazon.com/docs/alexa/alexa-design/get-started.html.
- Nielsen Norman Group — "Voice Interaction UX" (nngroup.com/articles/voice-first/).
- Erika Hall, "Conversational Design" (A Book Apart).
