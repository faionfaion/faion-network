# Agent Integration — AI + Spatial Computing

## When to use
- Designing XR (AR/VR/MR) interfaces that adapt to physical environment context
- Building AI-driven spatial UI that pre-positions content based on scene understanding
- Generating spatial layout specifications for Apple Vision Pro, Meta Quest, or WebXR targets
- Auditing existing spatial UI for contextual awareness gaps
- Prototyping voice + gesture interaction flows for 3D environments

## When NOT to use
- Standard 2D web/mobile UI — spatial computing overhead adds no value
- Early concept validation — spatial UX requires hardware to meaningfully test
- Budget-constrained projects where XR hardware deployment is not planned
- Contexts where latency is unacceptable (AI scene understanding adds ~50–200ms)

## Where it fails / limitations
- AI scene understanding models misclassify rooms under poor lighting or cluttered environments
- Gesture prediction degrades significantly with non-standard user postures or physical disabilities
- Voice integration fails in noisy public spaces; fallback interaction model is mandatory
- No open standard for spatial UI component libraries — every platform (visionOS, OpenXR) has its own primitives
- Personalization models require sufficient usage history; cold-start UX is always degraded
- Battery and thermal constraints on standalone HMDs limit AI inference frequency

## Agentic workflow
A Claude subagent can generate spatial UI specifications (layout grids, depth layers, gaze target sizes) from a natural language brief and a target platform. For context-adaptive behaviors, the agent produces a decision matrix mapping detected scene types to UI states. Human review is mandatory before hardware prototyping because agents cannot run XR simulators or validate spatial ergonomics.

### Recommended subagents
- `haiku` — generating boilerplate spatial layout specs, depth-layer tables, gaze-target checklists
- `sonnet` — scene-type decision matrices, AI capability mapping, interaction pattern documentation

### Prompt pattern
```
You are designing a spatial UI for [platform: visionOS / Meta Quest / WebXR].
Environment: [room type or use case].
Generate: (1) depth layer assignments for each UI panel, (2) gaze target sizes in degrees of visual angle, (3) fallback interaction for voice failure, (4) AI adaptation rule for each scene type.
Output as structured JSON.
```

```
Audit this spatial UI spec for: (1) missing fallback interactions, (2) gaze targets below 2° visual angle, (3) AI assumptions with no graceful degradation. List issues with severity High/Medium/Low.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `reality-composer-pro` | Apple visionOS UI prototyping | Xcode toolchain, macOS only |
| `adb` + Meta Developer Hub | Quest app sideloading and debugging | https://developer.meta.com/docs/ |
| `spatialdocs` (unofficial) | OpenXR spec CLI lookup | pip install spatialdocs |
| `webxr-emulator` | Browser-based XR simulation | https://github.com/MozillaReality/WebXR-emulator-extension |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma + Spatial Plugin | SaaS | Partial | No native 3D; 2D mockups only, export to Unity/Unreal |
| Unity with MRTK3 | OSS | Partial | Mixed Reality Toolkit; scripting via C# API |
| Needle Engine | SaaS/OSS | Yes (WebXR) | Three.js-based, deployable from Unity, REST API available |
| Gravity Sketch | SaaS | No | VR-native 3D design tool; no headless/API access |
| ShapesXR | SaaS | No | Collaborative XR prototyping; no agent API |
| Niantic Lightship VPS | SaaS | Yes | Visual positioning API; REST + SDK for scene anchoring |

## Templates & scripts
See templates.md for spatial UI specification templates (depth layer table, scene-type decision matrix).

Minimal scene-type decision matrix generator:
```python
SCENE_TYPES = ["living_room", "office", "kitchen", "outdoor", "unknown"]

def decision_matrix(scene: str) -> dict:
    rules = {
        "living_room": {"layout": "relaxed", "info_density": "low", "voice": True},
        "office":      {"layout": "compact",  "info_density": "high", "voice": False},
        "kitchen":     {"layout": "glanceable","info_density": "low", "voice": True},
        "outdoor":     {"layout": "minimal",  "info_density": "low", "voice": True},
        "unknown":     {"layout": "default",  "info_density": "medium", "voice": True},
    }
    return rules.get(scene, rules["unknown"])
```

## Best practices
- Define gaze target minimum size as 2° of visual angle (≈ 35px at 1m on typical HMD)
- Always design a graceful degradation path for every AI-driven adaptation — AI will fail
- Use depth layers deliberately: UI at 0.5m (near), 1–2m (mid), 4m+ (far); never mix reading distances in one panel
- Test voice commands with at least 3 non-native English speakers early — recognition degrades heavily with accents
- Separate spatial layout from AI logic: layout specs should work without AI; AI adds enhancement only
- Anchor persistent UI to world (not head) by default — head-locked UI causes nausea

## AI-agent gotchas
- Agents cannot simulate XR hardware — all spatial ergonomic decisions require human sign-off before build
- Scene classification outputs from AI are probabilistic; agent specs must include explicit confidence thresholds and fallback rules
- LLM hallucination risk is high for platform-specific constraints (e.g., visionOS eye-tracking limits) — always cite official platform docs
- Personalization model designs produced by agents need human review for privacy compliance (GDPR/CCPA) before implementation
- Agents tend to propose head-locked UI (easy to specify) — flag and reject; world-anchored is always preferred

## References
- https://developer.apple.com/visionos/human-interface-guidelines/
- https://developer.meta.com/docs/horizon/design/spatial-design-principles/
- https://www.w3.org/TR/webxr/ (WebXR Device API)
- https://learn.microsoft.com/en-us/windows/mixed-reality/mrtk-unity/ (MRTK3)
- Nielsen Norman Group — Spatial UX: https://www.nngroup.com/articles/spatial-ux/
