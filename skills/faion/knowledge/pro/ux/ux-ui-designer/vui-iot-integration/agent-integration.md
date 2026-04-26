# Agent Integration — VUI + IoT Integration

## When to use
- Designing voice control flows for smart home / industrial IoT (lights, locks, HVAC, scenes).
- Authoring multi-device routines ("Goodnight", "Leaving") that fan out commands across vendors.
- Mapping intents/utterances to device APIs (Matter, Home Assistant, SmartThings, Alexa, Google Home).
- Designing failure / partial-success / undo behavior across heterogeneous device fleets.

## When NOT to use
- Pure visual app UI work — use core-vui-design-principles only if a voice channel is in scope.
- Single-device, single-vendor remote control with no scene logic (manufacturer SDK is enough).
- Safety-critical automation (medical, alarm dispatch) — needs domain regulatory layer, not VUI patterns.
- Privacy-sensitive flows (door unlock, payments) without an explicit confirmation / auth design.

## Where it fails / limitations
- Cross-vendor parity drifts: Matter abstracts most attributes but not vendor-specific scenes.
- Latency stacks: NLU + intent routing + cloud bridge + Zigbee/Z-Wave hop can exceed 2s.
- Partial failures (3 of 5 devices respond) need explicit verbalization, not silent success.
- Wake-word false triggers from media playback corrupt routine logs and trigger unintended actions.
- Privacy: utterance transcripts often persist on vendor cloud — disclose and provide opt-out.

## Agentic workflow
Use a subagent to draft sample dialogues and intent/slot tables from a device inventory, then verify each utterance against vendor capability matrices (Matter cluster IDs, Alexa Smart Home capability interfaces, Google Smart Home traits). A second pass generates undo-flows and partial-failure prompts. Keep humans in the loop for any scene that touches doors, locks, alarms, or thermostats outside a safe range.

### Recommended subagents
- `faion-usability-agent` — drafts dialogues, intents, error reprompts, confirmation strategy.
- `faion-ux-researcher-agent` — runs Wizard-of-Oz or remote diary studies with smart-home users.
- `faion-sdd-executor-agent` — implements the routine in Home Assistant YAML / Alexa Skill / Google Action.

### Prompt pattern
```
You are a VUI designer. Given device inventory <list> and routine <name>,
output: (1) sample happy-path dialogue, (2) intent + slots table,
(3) partial-failure prompt, (4) undo prompt. No marketing language.
```

```
Validate utterance "<phrase>" against Matter cluster <id> and
Alexa capability <interface>. List any unsupported parameter.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` (Alexa) | Build, deploy, test Alexa Skills + smart-home interfaces | `npm i -g ask-cli`; developer.amazon.com/alexa/alexa-skills-kit |
| `gactions` | Google Actions / Smart Home action lifecycle | developers.google.com/assistant/conversational/gactions |
| Home Assistant CLI (`hass`) | Manage scripts, automations, voice intents | home-assistant.io/docs |
| `matter-tool` / `chip-tool` | Commission Matter devices, exercise clusters | github.com/project-chip/connectedhomeip |
| `voice2json` | Offline NLU prototyping (intent + slot extraction) | voice2json.org |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Home Assistant | OSS | Yes — REST + WS API, YAML configs editable by agents | Best target for cross-vendor scenes; Assist pipeline integrates LLMs. |
| Alexa Smart Home | SaaS | Partial — ASK SDK callable, certification is human-gated | Capability interfaces define which utterances are valid. |
| Google Home / Smart Home Actions | SaaS | Partial — gactions CLI, but device traits change | LLM-friendly via Gemini integration in Home APIs. |
| SmartThings | SaaS | Yes — REST API, scenes via API | Good for Samsung-heavy households. |
| Matter (CSA) | OSS standard | Yes — chip-tool + ecosystem bridges | Commission once, control via any controller. |
| Picovoice / Rhino | SaaS+OSS | Yes — on-device intent inference, deterministic | Useful when cloud round-trip is unacceptable. |

## Templates & scripts
See `templates.md` and `examples.md` in this dir for routine and dialogue templates. Inline routine skeleton (Home Assistant `script.yaml`):

```yaml
leaving_home:
  alias: "I'm leaving"
  sequence:
    - service: lock.lock
      target: { entity_id: lock.front_door }
    - service: light.turn_off
      target: { area_id: [living_room, kitchen, bedroom] }
    - service: climate.set_temperature
      target: { entity_id: climate.main }
      data: { temperature: 18 }
    - service: alarm_control_panel.alarm_arm_away
      target: { entity_id: alarm_control_panel.home }
    - service: tts.cloud_say
      data:
        entity_id: media_player.kitchen
        message: "Home secured. Have a good day."
  mode: single
```

## Best practices
- Always emit one terminal confirmation per routine, not per device, to avoid voice spam.
- Implement an explicit `undo last` intent with a 60s window scoped to the originating user.
- Use implicit confirmation for low-risk (lights), explicit for high-risk (locks, garage, alarms).
- Reserve scene names from common english stems: avoid "set" / "turn" / "play" as the scene noun.
- Log device-level success/failure separately from utterance-level so analytics can find weak nodes.
- Test in noisy conditions (kids, TV) — wake-word false-trigger rate is the dominant UX killer.

## AI-agent gotchas
- LLM-generated utterance lists drift to single phrasing; force at least 5 lexical variants per intent.
- Agents tend to skip undo and partial-failure paths — require these as named output sections.
- Vendor capability matrices change; cache them and version-pin in the prompt or RAG.
- Never let an agent auto-deploy a routine that touches locks, alarms, garage, or thermostat extremes — gate behind human approval.
- Voice transcripts in vendor cloud are PII; agents must not echo full transcripts in logs/prompts.
- Matter cluster IDs are numeric — agents hallucinate them; ground via `chip-tool` discovery.

## References
- Matter 1.4 spec — csa-iot.org/all-solutions/matter/
- Alexa Smart Home capability interfaces — developer.amazon.com/en-US/docs/alexa/device-apis/list-of-interfaces.html
- Google Smart Home device traits — developers.google.com/assistant/smarthome/traits
- Home Assistant Assist pipeline — home-assistant.io/voice_control/
- Cathy Pearl, *Designing Voice User Interfaces*, O'Reilly 2017 — chapter on multi-device.
- NN/g, "Voice-First Devices Hit Usability Roadblocks" — nngroup.com/articles/voice-first/
