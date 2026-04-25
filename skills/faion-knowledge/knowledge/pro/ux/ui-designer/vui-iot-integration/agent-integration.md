# Agent Integration — VUI + IoT Integration

## When to use
- Designing voice-control flows for Alexa Smart Home, Google Home, Apple HomeKit, or Matter devices.
- Authoring "scene" / "routine" definitions ("Goodnight", "I'm leaving") that orchestrate multiple devices.
- Generating intent + slot specs for a custom voice agent that drives Home Assistant, openHAB, or a vendor cloud.
- Auditing partial-failure handling across a multi-device routine.

## When NOT to use
- Single-device voice control with no automation logic (a smart bulb's stock skill is enough).
- Industrial IoT / SCADA — voice control is unsafe; use validated control panels.
- Privacy-sensitive contexts (childcare, medical) where always-on mics are inappropriate.
- Pre-Matter heterogeneous fleets without a unifying hub — voice mapping fragments.

## Where it fails / limitations
- Cloud-vendor smart-home APIs (Alexa, Google) require certification; agent-generated skills cannot ship without manual review.
- Voice latency stacks (ASR → NLU → cloud → device) make real-time control (dimmer ramping) feel laggy.
- Partial failure ("3 of 5 lights turned off") needs explicit acknowledgement; LLMs default to silently optimistic responses.
- Local fallback when cloud is offline is non-trivial; agents tend to ignore it.
- Cross-vendor scene names collide (Alexa's "Movie Time" vs. Google's "Movie") — synonyms get lost.

## Agentic workflow
Use Claude as a "scene composer": given a list of devices + capabilities (lights, locks, thermostat, alarm) and a desired user phrase, it emits a routine spec (ordered steps, parallel groups, retry policy, confirmation script). A second pass generates platform-specific JSON: Alexa Smart Home directive payload, Google Home Graph trait config, HomeKit accessory definition, or Home Assistant `script.yaml`. Voice confirmation copy passes through the same length / blame-free linter used in error-handling-in-vui.

### Recommended subagents
- `general-purpose` Claude subagent — scene composition + routine spec.
- `faion-sdd-executor-agent` — implement Home Assistant automations / vendor skills as SDD tasks.
- A "voice-copy-reviewer" prompt — vet confirmation utterances against time / blame rules.

### Prompt pattern
```
Phrase: "I'm leaving".
Devices: 4 lights (Hue), front-door lock (August), thermostat (ecobee), alarm (Ring).
Order: lock first, then arm alarm, parallel lights+thermostat, confirm last.
Output: Home Assistant script.yaml + Alexa SmartHome SetSceneRequest JSON.
```

```
Audit this routine (JSON below) for partial-failure handling.
List which steps lack rollback or user-facing acknowledgement.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ask-cli` (Alexa Skills Kit CLI) | Deploy Smart Home skill, lambda, intent model | `npm i -g ask-cli` |
| `gactions` | Google Home Actions / smart home schema | https://developers.home.google.com/cloud-to-cloud/get-started |
| `hass` (Home Assistant CLI) | Author / validate `script.yaml`, `automations.yaml` | `pip install homeassistant` |
| `mosquitto_pub` / `_sub` | MQTT testing for Matter / Zigbee2MQTT bridges | `apt install mosquitto-clients` |
| `chip-tool` | Matter device commissioning + control | https://github.com/project-chip/connectedhomeip |
| `nodecg` / `node-red` CLI | Visual flow programming for IoT routines | `npm i -g node-red` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Home Assistant | OSS | Yes (REST + WebSocket API) | Best agent integration target |
| openHAB | OSS | Yes (REST API) | Java-based; good for industrial-ish |
| Alexa Smart Home Skills | SaaS | Yes (ASK CLI) | Vendor certification required |
| Google Home Cloud-to-Cloud | SaaS | Yes (Home Graph API) | Requires Google review |
| Apple HomeKit / HAP | OS framework | Limited | Cert via MFi; agent stubs only |
| Matter / Thread (CSA) | Open standard | Yes (`chip-tool`) | Future-proof; vendor support uneven |
| Hubitat | SaaS-on-device | Yes (Maker API) | Local-first alternative |
| SmartThings (Samsung) | SaaS | Yes (REST API) | Cloud-only; rate-limited |

## Templates & scripts
See `templates.md` for routine spec format. Inline partial-failure linter:

```python
#!/usr/bin/env python3
# routine_lint.py — flag missing rollback / ack in routine spec
import json, sys
routine = json.load(sys.stdin)
issues = []
for i, step in enumerate(routine["steps"]):
    if step.get("critical") and "on_error" not in step:
        issues.append(f"step {i} ({step['action']}) is critical, no on_error rollback")
    if step.get("user_visible") and "ack" not in step:
        issues.append(f"step {i} affects user state, no spoken ack")
if not routine.get("final_confirmation"):
    issues.append("routine has no final spoken confirmation")
sys.exit("\n".join(issues) or 0)
```

## Best practices
- Lock + alarm steps run first in "leaving home" routines — fail-safe ordering.
- Always speak a final summary ("Home secured") with what actually happened, not what was requested.
- Provide a 5-second undo window for destructive actions ("Cancel goodnight").
- Use Matter where possible for new builds; vendor lock-in via Alexa-only skills is a long-term liability.
- Group devices by physical room, not by vendor; users speak in spatial terms.
- Test with cloud disconnected; routines should degrade to local control where the hub supports it.

## AI-agent gotchas
- Claude readily invents device capabilities (e.g., "set the lock to 50%"); validate against the actual capability schema.
- Generated routines often run in parallel without dependency analysis — locking the door before the user is out, etc.
- "Smart home" demos in LLM training often feature unrealistic latency; real cloud round-trips are 1–3 s.
- Agent will skip privacy considerations (always-on mic, voice transcript retention); add a privacy review checkpoint.
- Auto-deploying a routine update can lock users out of their own home — require human approval + dry-run.
- Vendor JSON schemas drift quarterly; pin the API version in the prompt and re-validate on every release.

## References
- https://developer.amazon.com/en-US/docs/alexa/smarthome/understand-the-smart-home-skill-api.html
- https://developers.home.google.com/cloud-to-cloud
- https://csa-iot.org/all-solutions/matter/
- https://www.home-assistant.io/docs/scripts/
- https://www.nngroup.com/articles/voice-iot/
- https://learn.microsoft.com/en-us/azure/iot-edge/
