# Agent Integration — Core VUI Design Principles

## When to use
- Designing a new voice agent or LLM-powered voice interface (Alexa skill, Google Action, custom Twilio/OpenAI Realtime app).
- Auditing transcripts of an existing voice product for verbosity, missing context handling, and unnatural turn-taking.
- Writing the system prompt and dialog policy for a Realtime API or Vapi voice agent — these principles map directly to instructions like "be concise" and "remember last 3 turns".
- Defining acceptance criteria for voice flows in a spec/design doc.

## When NOT to use
- Visual UI work — these principles are voice-specific and applying them to chat or screens leads to over-terse copy.
- IVR phone trees with strict regulatory scripts (banking, healthcare disclosures) — verbose disclaimers are mandatory; "natural" overrides hurt compliance.
- Rapid voice prototype with one-shot intent — full conversational principles are overkill before basic ASR works.

## Where it fails / limitations
- "Natural conversation" is fragile: ASR errors break the illusion, and current LLMs over-acknowledge ("Sure! I can do that for you!"), inflating latency.
- Context awareness costs tokens or memory engineering; long conversations hit Realtime API context limits (~30k tokens) before users notice.
- Simplicity collides with legal/safety requirements — the agent must say the long thing, not the short thing.
- Cultural/linguistic norms differ; principles drawn from US English voice UX do not map cleanly to Japanese, German, Ukrainian.

## Agentic workflow
Use one subagent to draft conversation flows from user stories, a second to lint each turn against the three principles (simplicity, naturalness, context), and a third to evaluate transcripts from real or synthetic users. Hold human-in-the-loop at script approval — voice errors are higher-stakes than text because they cannot be skimmed or edited.

### Recommended subagents
- `vui-script-writer` — turns user stories into prompt + sample dialog turns.
- `vui-linter` — flags long sentences, robotic phrasing, missing follow-ups.
- `vui-eval-agent` — runs transcript replay against the dialog policy and grades adherence.

### Prompt pattern
```
You are a VUI script linter. For each agent turn, return:
- words: count
- principle violations: [verbose|robotic|context-loss|none]
- rewrite: a tighter, conversational version (<=20 words unless legally required)
Reject any turn over 25 words unless flagged "legal:required".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask` (Alexa Skills Kit CLI) | Build/test Alexa skills | `npm i -g ask-cli` |
| `gactions` | Build Google Actions | https://developers.google.com/assistant/actions/gactions |
| `vapi` CLI | Manage Vapi voice agents | `npm i -g @vapi-ai/cli` |
| `openai realtime` examples | Realtime API harness | https://github.com/openai/openai-realtime-agents |
| `twilio` CLI | Phone number, IVR, voice flows | `brew install twilio/brew/twilio-cli` |
| `whisper` / `whisper.cpp` | Local ASR for transcript replay | https://github.com/ggerganov/whisper.cpp |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Realtime API | SaaS | Yes (websocket) | Native voice-in/voice-out, system prompt enforces principles. |
| Vapi | SaaS | Yes (REST + webhooks) | Voice agent platform, easy LLM swap. |
| Retell AI | SaaS | Yes | Phone-first voice agents with eval tooling. |
| ElevenLabs Conversational AI | SaaS | Yes | TTS-led, low-latency. |
| Voiceflow | SaaS | Partial (API) | Designer-friendly canvas, JSON export. |
| Pipecat | OSS | Yes | Python framework for real-time voice pipelines. |

## Templates & scripts
Inline VUI lint heuristic (≤30 lines).

```python
# vui_lint.py
import re, sys, json
WORD_RE = re.compile(r"\b\w+\b")
ROBOTIC = ["please be advised", "as previously mentioned", "i am unable to"]
def lint(turn: str) -> dict:
    words = len(WORD_RE.findall(turn))
    issues = []
    if words > 25: issues.append("verbose")
    low = turn.lower()
    if any(p in low for p in ROBOTIC): issues.append("robotic")
    if "..." in turn or " etc" in low: issues.append("filler")
    return {"words": words, "issues": issues}
if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if line: print(json.dumps({"turn": line, **lint(line)}))
```

Usage: `cat dialog.txt | python vui_lint.py`.

## Best practices
- Constrain LLM output length in the system prompt explicitly: "Reply in one sentence under 20 words unless asked to elaborate." Otherwise models default to chatty.
- Implement barge-in: user must be able to interrupt mid-utterance. Without it, "natural" is a lie.
- Persist last 5 turns + named-entity slots; full-history context blows the budget and increases ASR-error propagation.
- Use prosody/SSML sparingly and only where it earns understanding — over-tuned TTS sounds creepy.
- Run weekly transcript spot-checks; principle drift happens fastest when prompts change without eval.

## AI-agent gotchas
- LLMs over-confirm ("Got it! I'll do that right away!") — this kills latency and feels patronizing. Strip with output post-processing or system prompt.
- Realtime API tool calls add silence; pre-warm with "one moment" filler, but only once per turn.
- Context loss at long-pause boundaries: agents reset state mid-conversation. Snapshot state every turn server-side, not just in model context.
- Numbers and proper nouns hallucinate in TTS. Force phonetic spell-out for SKUs, addresses, codes.
- Human checkpoint: every system-prompt change must replay against a fixed transcript suite before deploy. Otherwise principle regressions ship silently.

## References
- Cathy Pearl, "Designing Voice User Interfaces" (O'Reilly).
- Google Conversation Design Guide: https://developers.google.com/assistant/conversation-design
- Amazon Alexa VUI Best Practices: https://developer.amazon.com/en-US/docs/alexa/alexa-design/get-started.html
- OpenAI Realtime API agent guide: https://platform.openai.com/docs/guides/realtime
- Voiceflow Conversation Design Institute: https://www.conversationdesigninstitute.com/
