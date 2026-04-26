# Agent Integration — Multimodal VUI Design

## When to use
- Designing interfaces that combine voice input with visual display (smart TVs, smart displays, kiosks)
- Building voice assistants that must surface structured data (search results, product cards, maps)
- Accessibility-first products where users alternate between touch and voice input
- Automotive HMI where eyes-free voice + glanceable visual feedback is safety-critical
- Conversational commerce flows (product search → carousel → voice-confirm purchase)

## When NOT to use
- Audio-only environments (earbuds, phone IVR) — no screen available; pure VUI applies
- Text-heavy B2B tools (dashboards, IDEs) — voice adds friction, no multimodal benefit
- Products where latency >2s is unacceptable — ASR + LLM + TTS chain is inherently slow
- Teams without dedicated voice UX expertise — multimodal amplifies design errors, not just design quality

## Where it fails / limitations
- Wake word false-positive rates increase in shared/noisy environments — visual fallback must not require voice to activate
- Screen real estate on smart displays is small; card carousel patterns that work on phones break on 7" displays
- LLM turn latency (1-3s) makes voice feel sluggish without visual streaming feedback (typing indicator, partial display)
- Multimodal state sync breaks when the user switches input mode mid-task; session state must persist across modalities
- Localization doubles: text AND speech assets require separate QA for each locale

## Agentic workflow
A Claude subagent can prototype multimodal dialogue flows by generating VUI scripts paired with visual layout descriptions. The agent handles dialogue turn design, fallback logic, and error state copy. Visual implementation (actual screen layouts, component assembly) requires human designer review — an agent cannot validate touch target sizing or card hierarchy without a rendering environment.

### Recommended subagents
- Custom VUI-prototyper agent — takes a user task, generates a multimodal dialogue script with screen state descriptions per turn; outputs a structured JSON dialogue tree
- `faion-sdd-executor-agent` — can execute implementation tasks from a VUI design spec if the spec is structured in SDD format

### Prompt pattern
```
You are a multimodal VUI designer. Design a voice + visual dialogue for the following task:
Task: {{task_description}}
Device: {{device_type}} (screen size: {{screen_size}})

For each dialogue turn, output:
- voice_prompt: what the assistant says
- visual_state: what appears on screen (component type, content, max 3 items)
- user_actions: valid voice inputs AND touch actions for this state
- fallback: what happens after 5s of silence

Return as JSON array of turns.
```

```
Review this multimodal dialogue for these failure modes:
1. States reachable only by voice (no touch fallback)
2. Visual states with >5 items (cognitive overload)
3. Missing confirmation before destructive actions
Return: [{turn_id, issue, severity, fix}]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gcloud` (Google Cloud SDK) | Access Dialogflow CX, Speech-to-Text, Text-to-Speech APIs | cloud.google.com/sdk |
| `aws` CLI | Amazon Alexa Skills Kit, Polly TTS, Transcribe | aws.amazon.com/cli |
| `az` CLI | Azure Cognitive Services (Speech SDK, LUIS) | learn.microsoft.com/en-us/cli/azure |
| `ffmpeg` | Audio processing, format conversion for TTS output validation | ffmpeg.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dialogflow CX | SaaS (Google) | Yes — REST API | Industry standard for multimodal flows; supports rich responses (cards, chips) |
| Amazon Alexa Skills Kit | SaaS | Yes — REST/SDK | Multimodal templates for Echo Show; APL for visual layer |
| Voiceflow | SaaS | Yes — REST API | Visual dialogue builder with export; good for prototyping |
| Rasa | OSS | Yes — Python API | Self-hosted NLU; pairs with custom TTS |
| ElevenLabs | SaaS | Yes — REST API | High-quality TTS; agent can generate voice previews for design review |
| Figma + Protopie | SaaS | Partial | Protopie can simulate voice triggers; no agent API |
| Botpress | OSS | Yes — REST API | Open-source conversation platform with multimodal nodes |

## Templates & scripts
See templates.md for dialogue turn schema and card layout specifications.

Inline: dialogue tree validator script:
```python
import json, sys

def validate_turns(turns: list) -> list:
    issues = []
    for i, t in enumerate(turns):
        if not t.get("touch_action"):
            issues.append({"turn": i, "issue": "no touch fallback", "severity": "high"})
        visual = t.get("visual_state", {})
        if isinstance(visual.get("items"), list) and len(visual["items"]) > 5:
            issues.append({"turn": i, "issue": "visual overload (>5 items)", "severity": "medium"})
        if t.get("destructive") and not t.get("confirmation_required"):
            issues.append({"turn": i, "issue": "missing confirmation", "severity": "high"})
    return issues

data = json.load(open(sys.argv[1]))
print(json.dumps(validate_turns(data), indent=2))
```

## Best practices
- Design every voice state to have a touch equivalent — users switch modalities mid-session constantly
- Keep voice prompts under 15 words for smart display; longer prompts lose users before visual renders
- Use streaming visual feedback (e.g., waveform animation) during ASR processing — silence feels broken
- Test on actual device hardware before usability testing — emulators do not reproduce touch + voice timing accurately
- Define a clear persona voice before writing any prompts — tone inconsistency across turns destroys trust
- Version control dialogue scripts separately from visual assets; they have different change cadences

## AI-agent gotchas
- Agent-generated dialogue often defaults to formal register; prompt explicitly for the target persona tone
- LLM response latency in a live VUI chain is user-visible (1-3s); agents must design for this, not assume instant response
- When an agent generates a dialogue tree, it cannot validate that visual card components exist in the design system — always cross-reference against component library
- Speech recognition accuracy varies by accent and environment; agent designs assuming high ASR accuracy will fail in real deployment
- An agent cannot hear — audio QA (prosody, pacing, pronunciation) must be done by a human with TTS playback

## References
- Google Conversation Design documentation — developers.google.com/assistant/conversation-design
- Amazon Alexa Multimodal Design Guidelines — developer.amazon.com/en-US/alexa/alexa-skills-kit/design
- "Designing Voice User Interfaces" — Cathy Pearl, O'Reilly 2017
- Voiceflow Multimodal Design Guide — voiceflow.com/docs
- Nielsen Norman Group — Voice Interfaces research — nngroup.com
