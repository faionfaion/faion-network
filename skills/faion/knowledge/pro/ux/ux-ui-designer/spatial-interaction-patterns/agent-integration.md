# Agent Integration — Spatial Interaction Patterns

## When to use
- Choosing input modality (hands / controllers / gaze / voice / gesture) per task in an XR app.
- Designing interaction state machines for direct manipulation, ray-cast selection, or gaze+dwell.
- Drafting accessibility-friendly multi-modal alternatives (voice or gaze fallback for fine motor).
- Specifying gesture vocabulary and conflict resolution in mixed-input apps.

## When NOT to use
- 2D mobile/desktop interactions — wrong vocabulary entirely.
- Pure 360° lean-back content where the user does not interact.
- Pre-strategy phases — pair with `spatial-ux-fundamentals` first to set field/scale before pattern choice.

## Where it fails / limitations
- Fixed pattern catalog hides hardware-specific constraints: Vision Pro is gaze-pinch first; Quest 3 emphasizes controllers; HoloLens leans hand-tracking + air-tap.
- Doesn't address fatigue economics (gorilla-arm, dwell fatigue, controller wrist load) — needs supplementary ergonomic data.
- Multi-input conflict (voice + hand + gaze in same moment) is a known failure mode the table glosses over.
- Performance: heavy hand-tracking + ray-cast at 90 Hz causes thermal throttling on standalone HMDs.
- Accessibility: gaze+dwell users with nystagmus or limited gaze control have no fallback in many engines.

## Agentic workflow
Drive Claude to produce a per-task input matrix (task × modality) with a recommended primary + fallback, then expand each into a state machine (idle → hover → engaged → committed → released) with timing thresholds. A second agent runs heuristic checks: conflict between modalities, missing accessibility fallback, fatigue red flags. Engine code (Unity XR / RealityKit / WebXR) is generated only after human review of the state machine.

### Recommended subagents
- `faion-ux-researcher-agent` — usability-test plan for each pattern with HMD users.
- `faion-usability-agent` — heuristic eval for fatigue, conflict, and accessibility.
- A custom `xr-input-state-linter` — given a state-machine spec, flag missing transitions or overlapping triggers.

### Prompt pattern
```
For task <T> on <device>, produce:
- Primary input modality + rationale (precision, fatigue, social context).
- Fallback modality (accessibility / when primary unavailable).
- State machine: idle, hover, engaged, committed, released. Trigger + timing per transition.
- Conflict rules vs. concurrent modalities.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity `xr-interaction-toolkit` | Standard XR input abstraction | docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit |
| OpenXR `khronos-tools` | Cross-vendor input layer | khronos.org/openxr |
| `Apple visionOS Simulator` (xcrun simctl) | Drive gaze-pinch in CI | developer.apple.com/visionos |
| `meta-quest-developer-hub` | Sideload + capture input traces | developer.oculus.com/downloads |
| Three.js + WebXR Input Profiles | Web-based gesture testing | github.com/immersive-web/webxr-input-profiles |
| MediaPipe Hands | Hand-tracking outside HMD for prototyping | google.github.io/mediapipe |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Unity 6 + XRI | Commercial | Yes (CLI build) | De facto standard XR input library |
| Unreal + OpenXR | Commercial | Partial | More codegen friction |
| Apple RealityKit / Reality Composer Pro | Free (Apple) | Limited | Vision Pro native; gaze+pinch idioms baked in |
| Bezi / ShapesXR | SaaS | Partial | Spatial wireframing with input intent |
| Microsoft MRTK3 (Mixed Reality Toolkit) | OSS | Yes | Hand + voice + eye for HoloLens/Quest |
| Tobii / Pupil Labs | SaaS + SDK | Yes | Standalone eye-tracking SDKs for fallback design |

## Templates & scripts
See `templates.md`. Inline state-machine linter (≤50 lines):

```python
import json, sys
REQUIRED = {"idle", "hover", "engaged", "committed", "released"}
def lint(spec):
    issues = []
    for ix, ix_spec in spec["interactions"].items():
        states = {s["name"] for s in ix_spec["states"]}
        missing = REQUIRED - states
        if missing: issues.append(f"{ix}: missing states {missing}")
        triggers = {}
        for s in ix_spec["states"]:
            for t in s.get("transitions", []):
                key = (s["name"], t["trigger"])
                if key in triggers:
                    issues.append(f"{ix}: duplicate trigger {t['trigger']} from {s['name']}")
                triggers[key] = t["to"]
        if not ix_spec.get("fallback_modality"):
            issues.append(f"{ix}: missing fallback modality")
        if ix_spec.get("primary_modality") == "gaze_dwell" and \
           ix_spec.get("dwell_ms", 0) < 600:
            issues.append(f"{ix}: dwell <600ms causes mis-fire")
    return issues
if __name__ == "__main__":
    for i in lint(json.load(open(sys.argv[1]))): print(i)
```

## Best practices
- Default to the platform's idiomatic primary (gaze-pinch on Vision Pro, controllers on Quest, air-tap on HoloLens) and only override with strong reason.
- Always pair direct manipulation with a ray-cast fallback for distant or large objects — reach is not infinite.
- Throw + physics is satisfying but discoverable only with onboarding; don't make it a primary action.
- Provide haptic + audio + visual confirmation on commit; spatial input is noisier than touch.
- Use 600-1200 ms dwell defaults for gaze-confirm; below 600 ms causes mis-fires, above 1200 ms feels broken.
- Budget for "fatigue scenes" — design 5-min sit breaks into long workflows.

## AI-agent gotchas
- LLMs invent gestures that the platform doesn't recognize (custom finger snaps, etc.); constrain to OpenXR / platform gesture sets only.
- Generated state machines often skip the `released` state, leaking event handlers in engine code.
- Auto-generated Unity / RealityKit code drifts behind SDK versions; pin versions in the prompt.
- Human-in-loop checkpoint: any new gesture or pattern must be validated in HMD by a designer; agents cannot judge fatigue, comfort, or social-acceptability ("clap in public" passes lint but fails reality).
- For accessibility: the agent must explicitly justify fallback modality choice; do not accept "user can also use controller" without a switch/voice path.

## References
- Apple Human Interface Guidelines — visionOS Inputs — developer.apple.com/design/human-interface-guidelines/inputs
- Meta Quest VR Interaction Patterns — developer.oculus.com/resources
- Microsoft MRTK3 docs — learn.microsoft.com/windows/mixed-reality/mrtk-unity
- *Designing for Mixed Reality* — Kharis O'Connell
- OpenXR Specification — khronos.org/openxr
- W3C WebXR Input Profiles — github.com/immersive-web/webxr-input-profiles
