# Agent Integration — Multimodal VUI Design

## When to use
- Designing a voice interface for a smart display device (Amazon Echo Show, Google Nest Hub, Alexa-enabled TV)
- Building a product that combines voice input with a visual screen output (not voice-only, not screen-only)
- Auditing an existing VUI for missing visual fallbacks — users who cannot or will not speak need touch/tap alternatives
- Generating APL (Alexa Presentation Language) or equivalent smart display template markup from a design brief
- Prototyping a multimodal conversation flow where visual selection confirms voice ambiguity resolution

## When NOT to use
- Building a voice-only (screenless speaker) interface — pure VUI design methodology is more appropriate
- Building a screen-only UI with optional voice layer — the voice-initiated trigger pattern does not add value here
- The target device has no reliable microphone (IoT sensor, kiosk in high-noise environment without directional mic)
- The user research shows the target audience is strongly opposed to voice interaction (enterprise compliance context)

## Where it fails / limitations
- Multimodal design requires synchronized state between voice and visual layers — AI-generated flows often miss state sync edge cases
- Wake-word false positive rate disrupts the visual experience unexpectedly — AI cannot solve this at the UX layer; hardware matters
- "Voice-initiated, screen-completed" flows break when the user takes longer than the VUI timeout to interact with the visual element
- Smart display APL/response templates are platform-specific — design for Echo Show does not transfer directly to Google Nest Hub
- AI-generated fallback hierarchies often omit the tertiary (keyboard) path for accessibility edge cases
- Touch-to-voice handoff is poorly handled by most AI-generated flow designs — the seam between modalities is where the UX fails

## Agentic workflow
A Claude subagent (Haiku) receives a feature brief specifying the interaction type (voice-initiated/screen-completed, screen-initiated/voice-completed, simultaneous) and generates the multimodal interaction specification: voice trigger phrases, visual output layout, fallback hierarchy, and timeout behavior. A Sonnet subagent reviews the generated spec for state-sync consistency and platform-specific constraints. Human VUI designers validate on actual device hardware.

### Recommended subagents
- General Claude subagent (Haiku) — interaction pattern generation, APL/response template scaffolding
- General Claude subagent (Sonnet) — state-sync consistency review, accessibility fallback audit

### Prompt pattern
```
You are a multimodal VUI designer for [device: Echo Show / Google Nest Hub].
Design the interaction flow for: [feature description]
Interaction type: [voice-initiated screen-completed | screen-initiated voice-completed |
                  voice + visual feedback | voice navigation + visual content]
Output:
1. Voice trigger phrases (primary + 2 alternates)
2. Visual output layout (card/carousel/list/detail)
3. Spoken confirmation summary
4. Fallback hierarchy: primary (voice) → secondary (touch) → tertiary (keyboard if available)
5. Timeout behavior (what happens after [N] seconds of no input)
6. Error state: what to say/show if voice input is not understood
```

```
Review this multimodal flow spec for state-sync issues:
[spec text]
Check:
- Does the visual state stay consistent if the user speaks while touching?
- Are timeouts appropriate for the visual complexity shown?
- Is the fallback hierarchy complete for users who cannot speak?
- Are error recovery paths present for both voice and touch failures?
Output a numbered list of issues with severity (Blocking/High/Low).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Alexa Skills Kit CLI (`ask-cli`) | Deploy Alexa skills with APL templates | `npm install -g ask-cli` / developer.amazon.com/alexa/console |
| Google Actions CLI (`gactions`) | Deploy Google Actions with canvas/rich responses | `npm install -g @assistant/gactions` |
| `pyaudio` | Capture microphone input for local VUI prototyping | `pip install pyaudio` |
| Voiceflow CLI | Export/import conversation flows | voiceflow.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amazon Alexa Presentation Language (APL) | Platform SDK | Yes — JSON templates | Agent can generate APL JSON from design spec |
| Google Assistant Canvas | Platform SDK | Yes — JS/JSON | Agent can scaffold canvas response templates |
| Voiceflow | SaaS | Yes — REST API | Visual conversation flow builder; API for programmatic flow management |
| Dialogflow CX | SaaS | Yes — REST API | Intent/entity management; agent can create intents via API |
| Amazon Polly | SaaS | Yes — REST API | TTS with voice persona selection; SSML control |
| Google Text-to-Speech | SaaS | Yes — REST API | TTS with WaveNet voices and SSML |
| Botpress | OSS | Yes — REST API | Self-hosted conversation management; agent-updatable flows |

## Templates & scripts
See `templates.md` for the multimodal conversation flow template and smart display card layout spec.

APL card generator script (Alexa Echo Show):
```python
import json

def make_apl_card(title: str, items: list[dict], spoken_summary: str) -> dict:
    """Generate a minimal APL list card for Echo Show."""
    return {
        "type": "APL",
        "version": "1.9",
        "document": {
            "type": "APL",
            "mainTemplate": {
                "item": {
                    "type": "Container",
                    "items": [
                        {"type": "Text", "text": title, "style": "textStyleHeading"},
                        {
                            "type": "Sequence",
                            "items": [
                                {
                                    "type": "Text",
                                    "text": item["label"],
                                    "speech": item.get("speech", item["label"]),
                                }
                                for item in items
                            ],
                        },
                    ],
                }
            },
        },
        "datasources": {"spoken_summary": spoken_summary},
    }

if __name__ == "__main__":
    card = make_apl_card(
        "Pasta Recipes",
        [{"label": "Spaghetti Bolognese"}, {"label": "Cacio e Pepe"}],
        "I found 2 pasta recipes.",
    )
    print(json.dumps(card, indent=2))
```

## Best practices
- Always design the fallback hierarchy before the primary interaction — if touch is broken, voice is broken too for a large user segment
- Spoken summaries must be shorter than visual content — users listening cannot process paragraph-length speech
- Set visual element timeouts to match the complexity of what is shown: list (10s), detail card (20s), multi-step form (60s)
- Test with the screen covered (voice-only degradation) and microphone muted (touch-only degradation) separately
- Use SSML prosody tags to control speaking pace for confirmation messages — too fast and users miss the confirmation
- Platform-specific APL templates must be tested on actual Echo Show models — simulator rendering differs from hardware
- Document all supported voice trigger phrases in the skill's interaction model — undocumented phrases fail silently in production

## AI-agent gotchas
- Agent-generated APL JSON often uses deprecated APL version features — specify the target APL version explicitly in the prompt
- Multimodal state sync (voice selects item simultaneously with touch) is an edge case that agent-generated specs routinely miss — add it as an explicit review checklist item
- Agent timeout suggestions are often too short for elderly users or users with cognitive disabilities — require accessibility-minimum timeout values in the prompt (minimum 10s for simple responses)
- Agents conflate "fallback" (user cannot use primary input) with "error" (input was understood but failed) — keep these paths separate in the spec
- Human-in-loop checkpoint: VUI design requires testing with real users on actual hardware before any production deployment — no agent review substitutes for this

## References
- Google multimodal design guidelines: https://designguidelines.withgoogle.com/conversation/multimodal/
- Amazon APL developer docs: https://developer.amazon.com/en-US/docs/alexa/alexa-presentation-language/apl-overview.html
- Nielsen Norman Group multimodal VUI: https://www.nngroup.com/articles/multimodal-voice/
- W3C WCAG 2.2 SC 1.3.4 (Orientation), 2.5.x (Input Modalities): https://www.w3.org/TR/WCAG22/
