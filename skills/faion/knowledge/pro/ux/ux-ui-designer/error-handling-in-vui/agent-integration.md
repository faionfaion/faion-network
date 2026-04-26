# Agent Integration — Error Handling in VUI

## When to use
- Designing fallback dialogs for ASR no-input, no-match, and ambiguous-intent failures.
- Drafting "re-prompt with example" copy for second/third failure passes before escalation.
- Auditing existing skill (Alexa/Google Action/Dialogflow) intents that crash on unhandled utterances.
- Building help/transfer-to-agent escalation paths for IVR or LLM-backed voice bots.

## When NOT to use
- Pure speech-to-text quality issues (model retraining/acoustic tuning, not dialog design).
- Silent/visual UIs where confirmation can be shown on screen — overengineering.
- One-shot transactional voice commands with no multi-turn state (no recovery path needed).

## Where it fails / limitations
- LLM-driven VUIs (Realtime API, Gemini Live) bypass fixed re-prompt ladders; the model improvises and the rung-by-rung fallback model breaks.
- Re-prompts that quote example phrases verbatim push users into parroting and mask the real error rate.
- Hidden barge-in / endpointing thresholds dominate "no input" errors more than copy ever can.
- Telephony channels add 8 kHz codec loss + cross-talk that no copy fix mitigates.

## Agentic workflow
Drive Claude to enumerate failure types per intent, then generate three-rung re-prompt ladders (rapid → constructive → escalation) plus the matching SSML/text. A second pass linting agent checks for blame language ("you said wrong"), missing example phrases on rung 2, and absent escalation on rung 3. Use a separate agent to fuzz the dialog by sampling adversarial transcripts (silence, mumble, code-switch, off-topic).

### Recommended subagents
- `faion-ux-researcher-agent` — synthesize transcript reviews into failure taxonomy.
- `faion-usability-agent` — heuristic eval of re-prompt copy (politeness, clarity, escalation).
- A custom `vui-dialog-linter` (project-local) — regex check for banned phrases ("invalid", "wrong", "didn't work").

### Prompt pattern
```
For intent <X>, list NoInput/NoMatch/Ambiguous/SystemError failure modes.
For each mode, write 3 escalating re-prompts. Rung 2 must include 2 example phrases.
Rung 3 must offer transfer/visual fallback. No blame. SSML where pause >300ms.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` (Alexa Skills Kit) | Lint/test re-prompt sets, simulate utterances | `npm i -g ask-cli` · developer.amazon.com/alexa/alexa-skills-kit/asksdk |
| `gactions` (Google Actions) | Deploy/test conversational webhooks | github.com/actions-on-google/gactions |
| `voiceflow-cli` | Export Voiceflow flows as JSON for review | github.com/voiceflow/api-sdk |
| `rasa` | Open-source dialog testing, story files | `pip install rasa` |
| `nlpaug` | Generate adversarial utterances for fuzzing | `pip install nlpaug` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Voiceflow | SaaS | Yes (REST API) | Dialog manager, exposes flows as JSON for prompt-pattern review |
| Dialogflow CX | SaaS | Yes (gRPC/REST) | Built-in event handlers for no-input/no-match per page |
| Rasa Open Source | OSS | Yes | YAML stories testable in CI; supports custom fallback policies |
| Cognigy.AI | SaaS | Yes | Fallback flows; transcript export for offline analysis |
| OpenAI Realtime API | SaaS | Partial | LLM-native; no rung concept — use system prompt to enforce escalation |
| Microsoft Bot Framework | SaaS/OSS | Yes | Composer scaffolds re-prompts; LU testing via `bf` CLI |

## Templates & scripts
See `templates.md` for re-prompt ladders. Inline lint script (Python, ≤50 lines):

```python
import re, sys, yaml
BANNED = [r"\bwrong\b", r"\binvalid\b", r"\byou said\b", r"\bdidn'?t work\b"]
def check(prompts):
    issues = []
    for intent, rungs in prompts.items():
        if len(rungs) < 3: issues.append(f"{intent}: needs 3 rungs")
        if rungs and not any("example" in r.lower() or "try" in r.lower() for r in rungs[1:2]):
            issues.append(f"{intent} rung2: missing example phrases")
        if rungs and not any(w in rungs[-1].lower() for w in ("agent","help","menu","instead")):
            issues.append(f"{intent} rung3: missing escalation")
        for i, r in enumerate(rungs):
            for pat in BANNED:
                if re.search(pat, r, re.I): issues.append(f"{intent} rung{i+1}: banned '{pat}'")
    return issues
if __name__ == "__main__":
    prompts = yaml.safe_load(open(sys.argv[1]))
    for i in check(prompts): print(i)
```

## Best practices
- Cap rung count at 3; users rarely tolerate a 4th retry — escalate.
- Rotate rung-2 examples per session so users aren't trained to mimic one phrase.
- Log raw ASR hypotheses (not just normalized intent) — reveals systematic mishears.
- Treat "user repeats verbatim louder/slower" as a soft failure even if intent matched — copy is too narrow.
- Vary "I didn't catch that" phrasing across rungs to signal progression, not a stuck loop.
- For telephony, always offer DTMF fallback ("press 1 for…") on rung 3.

## AI-agent gotchas
- LLM voice agents may "hallucinate compliance" — say "transferring you" without firing the tool. Force tool call check in evals.
- Realtime models reset turn-state on long pauses; use server-side endpointing override or you'll silently re-trigger no-input forever.
- Subagents writing copy will default to apologetic templates — explicitly forbid "I'm sorry" stacking.
- Human-in-loop checkpoint: review rung 3 escalation copy with support/legal before shipping (refund, escalate-to-human, transfer phrasing has compliance impact).
- Don't let the agent invent example phrases that aren't in the actual NLU training data — every example must round-trip through the recognizer.

## References
- Cohen, Giangola, Balogh — *Voice User Interface Design* (Addison-Wesley)
- Google Conversation Design — designguidelines.withgoogle.com/conversation
- Alexa Voice Design Guide — developer.amazon.com/alexa/alexa-skills-kit/design
- Nielsen Norman Group — *Voice Interaction UX*
- Dialogflow CX No-Match/No-Input event handlers — cloud.google.com/dialogflow/cx/docs
