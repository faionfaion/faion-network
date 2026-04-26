# Agent Integration — Spatial Interaction Patterns

## When to use
- Selecting input modality (hands, controllers, gaze, voice, gesture) for a Vision Pro / Quest / WebXR feature.
- Designing direct-manipulation, ray-cast, or gaze+dwell flows for a 3D scene.
- Auditing accessibility of an XR app's interaction model.
- Generating XR Interaction Toolkit (Unity) or RealityKit / SwiftUI gesture stubs from interaction specs.

## When NOT to use
- 2D web/mobile UI — modality is touch/mouse/keyboard, irrelevant here.
- Pure passive media (360° video) without user input.
- Hardware target undecided — patterns differ sharply across Vision Pro (eye+pinch) vs. Quest (controllers/hands) vs. HoloLens.
- One-off demos where pattern consistency doesn't matter.

## Where it fails / limitations
- LLMs cannot validate ergonomics: arm fatigue, FOV blind spots, hand-tracking jitter.
- Gaze+dwell timing is platform-specific (Vision Pro pinch-confirm replaces dwell entirely).
- Agents tend to over-mix modalities; real apps need a primary modality with secondary fallback.
- No reliable way for an agent to test interaction comfort without a human in a headset.
- Cross-platform porting (Quest hand-tracking → Vision Pro eye-tracking) requires re-design, not re-mapping.

## Agentic workflow
Use Claude as an "interaction-pattern selector": given a feature spec + target headset, it returns a primary modality, a fallback, and the gesture spec (event names, dwell timings, haptic cues). A second pass generates platform-specific scaffolding — Unity XR Interaction Toolkit components, RealityKit `Gesture` modifiers, or WebXR `XRInputSource` handlers. Hand off to a developer subagent for code-level implementation; reserve a human in-headset session for ergonomics sign-off before merge.

### Recommended subagents
- `general-purpose` Claude subagent — modality selection + interaction spec.
- `faion-sdd-executor-agent` — implement an SDD task once the spec is approved.
- A custom `xr-gesture-author` prompt — emit Unity / RealityKit / WebXR gesture stubs from a JSON spec.

### Prompt pattern
```
Feature: select item from a 6-cell grid menu, anchored 1.2 m in front.
Headset: Apple Vision Pro.
Constraint: hands-free preferred (user holds a coffee cup).
Output: primary modality + fallback + RealityKit Gesture stub.
```

```
Convert this interaction spec (JSON below) into Unity XR Interaction Toolkit
components: XRGrabInteractable, XRDirectInteractor, XRRayInteractor.
Include Input System bindings for Quest 3 controllers + hand-tracking.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity `XR Interaction Toolkit` (UPM) | Standard XR input abstraction | `com.unity.xr.interaction.toolkit` |
| OpenXR Loader (Unity / Unreal) | Cross-vendor XR runtime | https://www.khronos.org/openxr/ |
| Apple `xcrun simctl` + visionOS sim | Test interactions in simulator | Xcode 15+ |
| Meta `ovrmetricstool` | Measure hand-tracking jitter / latency | Quest Developer Hub |
| `webxr-emulator` (Chrome ext.) | Debug WebXR `XRInputSource` events | https://github.com/MozillaReality/WebXR-emulator-extension |
| `gltf-transform` | Bake interaction colliders into glTF | `npm i -g @gltf-transform/cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Unity XR Interaction Toolkit | OSS (UPM) | Yes (Unity CLI) | De-facto standard |
| Apple RealityKit | OS framework | Yes (Swift codegen) | Vision Pro native |
| Meta Interaction SDK | OSS | Yes | Hand-tracking pose library |
| Microsoft MRTK3 | OSS | Yes (UPM) | HoloLens + cross-platform |
| ShapesXR | SaaS | No public API | Author interaction storyboards manually |
| WebXR Device API (browser) | Web standard | Yes (JS codegen) | `navigator.xr` |
| Ultraleap (formerly Leap Motion) | SaaS+SDK | Yes (CLI samples) | Mid-air haptics + hand tracking |

## Templates & scripts
See `templates.md` for the interaction-spec JSON schema. Inline modality selector heuristic:

```python
#!/usr/bin/env python3
# pick_modality.py — recommend primary input given context
import json, sys
spec = json.load(sys.stdin)
# spec keys: hands_free, distance_m, precision, accessibility, headset
def pick(s):
    if s["accessibility"] == "low_motor":
        return "gaze+dwell" if s["headset"] != "vision_pro" else "eye+pinch"
    if s["hands_free"] and s["distance_m"] < 1.5:
        return "voice"
    if s["distance_m"] < 0.8:
        return "direct_hand"
    if s["precision"] == "high":
        return "controller_ray"
    return "hand_ray"
print(json.dumps({"primary": pick(spec)}))
```

## Best practices
- One primary modality per feature; secondary is a fallback, not a co-equal.
- Ray-cast for far (> 0.8 m), direct-grab for near (< 0.8 m); never mix in the same target.
- Always include haptic / audio confirmation; visual-only feedback is insufficient in XR.
- Respect Vision Pro's eye+pinch convention — don't invent a gaze-dwell pattern users have to relearn.
- Provide a "rest pose" for hands; constant arm-up gestures cause gorilla arm in < 60 s.
- Map every gesture to a discoverable affordance (highlight, glow, label); XR has no tooltips.

## AI-agent gotchas
- Claude conflates Vision Pro and Quest interaction grammars; pin the headset name explicitly in every prompt.
- Hand-tracking false positives (pinch detected on grab) are invisible to the agent; require human QA.
- Agent may suggest "swipe in air" patterns that have no physical anchor — they fail in practice.
- Generated Unity XRI code often targets deprecated 1.x API; pin XRI 2.5+ in the prompt.
- Privacy: gaze data is biometric; agent should warn before logging eye-tracking events to analytics.
- Don't let an agent auto-tune dwell time; sub-optimal values trigger nausea or false selections.

## References
- https://developer.apple.com/design/human-interface-guidelines/eyes
- https://developer.apple.com/design/human-interface-guidelines/gestures
- https://developers.meta.com/horizon/design/hands-design-intro/
- https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/index.html
- https://www.khronos.org/openxr/
- https://learn.microsoft.com/en-us/windows/mixed-reality/design/interaction-fundamentals
- Jerald, *The VR Book: Human-Centered Design for Virtual Reality* (ACM/Morgan & Claypool)
