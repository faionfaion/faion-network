# Agent Integration — VR Design Patterns

## When to use
- Fully-immersive Quest, Vision Pro (immersive scene), Pico, Index, Vive deployments.
- Designing locomotion, in-VR menus, hand-tracking interactions, or seated/room-scale modes.
- Migrating a 2D enterprise tool (training, collaboration, design review) to a VR-native experience.
- Specifying comfort defaults and accessibility fallbacks for a VR build.

## When NOT to use
- AR / passthrough / MR-first apps — see `ar-design-patterns` and `immersive-design-principles` instead.
- 360° video viewers without interaction — patterns over-engineer the experience.
- Web-based WebXR demos with <2 min target session — most patterns assume sustained presence.

## Where it fails / limitations
- Locomotion comfort varies wildly by individual; "teleport works for everyone" is a myth.
- Floating UI panels obey simulator physics, not human ergonomics — wrist fatigue rises after ~8 min of pinch input.
- Guardian/chaperone boundary is platform-specific (Meta vs. SteamVR vs. visionOS); patterns can't be device-agnostic.
- Hand-tracking jitter under low light makes precise selection unreliable; agents that test in well-lit dev rooms over-trust it.
- Eye-tracking gaze-and-confirm is not yet portable; visionOS uses it natively, Quest 3 doesn't.

## Agentic workflow
Use agents to map interaction requirements to known VR patterns (locomotion choice, menu placement, comfort vignette, selection method) and to generate playtest scripts. Final pattern selection requires in-headset verification with at least 5 testers including one who's prone to motion sickness.

### Recommended subagents
- `faion-ux-researcher-agent` — produces presence/immersion questionnaires (IPQ, SSQ, PQ), recruits VR-novice + expert mix.
- `faion-usability-agent` — heuristic evaluation against Oculus VRCs and Apple visionOS HIG.

### Prompt pattern
```
Recommend VR design patterns for:
  task: <task description>
  duration: <minutes>
  device: Quest3|VisionPro|Pico4|Index
  pose: seated|standing|room-scale
  user_familiarity: novice|intermediate|expert

Output JSON:
  locomotion: {method, justification, comfort_score}
  ui_placement: {anchor, hand_attached|world|wrist}
  selection: gaze+pinch|controller_ray|direct_touch|voice
  comfort: {vignette, snap_turn_deg, frame_rate_min}
  fallbacks: [accessibility_fallback per interaction]
Cite Oculus VRC or Apple HIG section per recommendation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ovrplatformutil` | Quest store submission, perf metrics export | https://developer.oculus.com/downloads/package/oculus-platform-utility/ |
| `OVRMetricsTool` / `OVR Performance HUD` | On-device frame-time, dropped frames | Meta dev portal |
| `xcrun simctl` (visionOS) | Vision Pro simulator boot/launch from CI | Xcode 15+ |
| `OpenXR validation layer` | Conformance checking pre-submission | https://github.com/KhronosGroup/OpenXR-SDK |
| `Unity Test Framework` (CLI mode) | Headless playmode tests for scene logic | Unity docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Unity + XR Interaction Toolkit | Commercial | Yes (CLI builds) | De facto VR dev stack. |
| Unreal Engine + OpenXR | Source-available | Yes (Horde CI) | Higher fidelity, steeper learning. |
| Godot XR | OSS | Yes | Lightweight, growing OpenXR support. |
| Reality Composer Pro | macOS app | Limited | visionOS scenes; manual workflow. |
| ShapesXR | SaaS | Partial | Multi-user spatial review; export to Unity. |
| Bezel | SaaS | Partial | Spatial design tool with Figma-like UX. |
| Meta Horizon Worlds Studio | SaaS | No | Closed ecosystem; not for production B2B. |

## Templates & scripts
See `templates.md` for locomotion decision tree and UI-placement matrix. Inline VRC checklist generator:

```bash
#!/usr/bin/env bash
# gen-vrc-check.sh — emit Oculus VRC pre-submission checklist
APP="${1:?app name}"
OUT="qa/$APP/vrc-check.md"
mkdir -p "qa/$APP"
cat > "$OUT" <<MD
# $APP — VRC Pre-Submission

## Performance
- [ ] 72 Hz sustained on Quest 2 (or 90 Hz on Quest 3)
- [ ] CPU/GPU level set, no thermal throttle in 15 min run
- [ ] Stage memory <2.5 GB (Quest 2)

## Comfort
- [ ] No head-locked HUD
- [ ] Snap turn 30°/45° option
- [ ] Smooth-turn vignette toggle
- [ ] Reduce-motion accessibility setting

## Input
- [ ] Both controller and hand-tracking supported (or graceful fallback)
- [ ] Left-handed binding option
- [ ] Sit/stand recenter

## Boundaries
- [ ] Guardian visible during locomotion
- [ ] Resume-from-boundary path defined

## Accessibility
- [ ] Subtitle support
- [ ] Color-blind friendly UI
- [ ] One-handed mode
MD
```

## Best practices
- Default locomotion: teleport + snap-turn for novice, smooth-locomotion + comfort vignette for opt-in.
- Anchor primary UI to a wrist or world panel within 1.5 m; head-locked = nausea.
- Provide both seated and standing modes; recenter must be one-button accessible at all times.
- Audio is half the experience: spatial audio cues reduce visual UI clutter and improve presence.
- Keep first-time-user orientation under 60 seconds; longer onboarding gets skipped or abandoned.
- Always ship a 2D fallback build for screenshots, marketing, and accessibility — VR-only excludes ~15% of buyers.

## AI-agent gotchas
- Agents propose smooth-locomotion as default because it "feels natural" — it ships motion sickness. Force teleport-first.
- Hand-tracking patterns generated from Apple HIG don't apply to Meta SDKs; pin device per prompt.
- Frame-budget claims need on-device validation; LLMs cannot estimate draw calls or fillrate.
- "Use gaze + confirm for selection" is correct on Vision Pro and wrong on Quest 3 (no eye-tracking on standard Quest 3); pin device.
- Guardian/chaperone integration code differs per platform; agents tend to merge APIs into a Frankenstein call. Specify SDK version in prompt.
- Comfort vignette parameters (size, fade-in time) need playtest tuning; agent defaults are conservative-to-broken.

## References
- Apple, *visionOS Human Interface Guidelines — Immersive Experiences*. https://developer.apple.com/design/human-interface-guidelines/immersive-experiences
- Meta, *Oculus VRC for Quest*. https://developer.oculus.com/resources/bp-vrc-quest/
- Jerald, *The VR Book* (2015).
- LaViola et al., *3D User Interfaces: Theory and Practice* (2nd ed., 2017).
- Bowman et al., *3D User Interfaces: Theory and Practice* — companion empirical studies on locomotion.
