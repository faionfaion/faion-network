# Agent Integration — Spatial UX Fundamentals

## When to use
- Designing UI for Apple Vision Pro, Meta Quest, or other XR headsets
- Planning spatial layout of panels, menus, and work surfaces in a 3D environment
- Auditing an existing XR app for ergonomic violations (content too close, too high, peripheral placement)
- Specifying spatial interaction patterns for a development team new to XR
- Creating documentation for a spatial design system (scale, reach zones, field-of-view constraints)

## When NOT to use
- Flat 2D web or mobile interfaces — spatial principles do not transfer and introduce unnecessary complexity
- Early product ideation phases before target hardware is confirmed — spatial constraints vary significantly across headsets
- Accessibility audits without XR-specific assistive technology expertise — spatial a11y is a specialized subfield
- When the development team has no XR SDK experience — design artifacts cannot be implemented without platform capability

## Where it fails / limitations
- Agents cannot simulate 3D space, field of view, or head tracking — all spatial specifications are text descriptions that require human validation in a headset
- Comfort zones (near/mid/far field, angular limits) vary across headsets (Apple Vision Pro vs. Meta Quest 3 vs. HoloLens 2) — agents use generic guidelines that may be wrong for the specific device
- Occlusion and depth perception cannot be described in flat text; agents produce spatially inconsistent specs without 3D modeling tools
- Ergonomics research for XR is still maturing (2024-2026); agent training data may be based on superseded guidelines
- Agent-generated spatial interaction patterns (gaze, pinch, hand tracking) frequently omit the latency and prediction requirements that make them comfortable vs. nauseating

## Agentic workflow
An agent receives a target device spec (headset model, field of view, recommended comfort zones) and a list of UI elements to place spatially. It produces: (1) a spatial layout spec table assigning each element to near/mid/far field with angular offset from center, (2) interaction pattern assignments (gaze-dwell, pinch, hand ray, voice) per element, and (3) an ergonomic risk list flagging elements outside comfort zones. All output must be validated by a human designer in the target headset before development begins.

### Recommended subagents
- General Claude subagent (opus) — spatial design requires novel pattern reasoning across unfamiliar interaction models
- General Claude subagent (sonnet) — element-to-zone assignment tables and interaction pattern documentation

### Prompt pattern
```
You are a spatial UX designer targeting [device: Apple Vision Pro / Meta Quest 3 / HoloLens 2].
Device comfort zone specs:
- Near field: 0.5–1m, primary interactions, ±30° horizontal, ±20° vertical from center
- Mid field: 1–3m, content consumption, ±45° horizontal
- Far field: 3m+, navigation anchors, environmental context only

Given these UI elements: [list]
For each element, specify:
1. Field zone (near / mid / far)
2. Angular placement (degrees H/V from center gaze)
3. Interaction modality (gaze-dwell / pinch / hand ray / voice / controller)
4. Scale (world units at placement distance)
5. Ergonomic risk (Low / Medium / High) with reasoning

Flag any element you cannot place without additional context.
```

```
Ergonomic audit prompt:
Given this spatial layout specification: [spec]
Identify violations of these XR ergonomic rules:
- No UI elements above 25° vertical (neck strain)
- No interactive elements closer than 0.5m (vergence-accommodation conflict)
- No critical information in the bottom 20° (obscured by body/hands)
- No text smaller than 0.5° visual angle at placement distance
- Interaction targets minimum 1cm × 1cm at placement distance
Output: table of violations with severity (Critical / Warning) and remediation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity XR Interaction Toolkit | Primary XR development SDK with spatial interaction primitives | https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest |
| `@react-three/fiber` | React-based 3D/XR rendering for web-based spatial UI | `npm i @react-three/fiber` / https://docs.pmnd.rs/react-three-fiber |
| `@react-three/xr` | WebXR bindings for React Three Fiber | `npm i @react-three/xr` / https://github.com/pmndrs/xr |
| RealityKit (Swift) | Apple spatial computing framework | https://developer.apple.com/documentation/realitykit |
| Unreal Engine XR | High-fidelity XR with Blueprint spatial scripting | https://dev.epicgames.com/documentation/en-us/unreal-engine/xr-development-in-unreal-engine |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reality Composer Pro | Apple tool (free) | No | Spatial scene authoring for visionOS; no API but produces USDA scene files |
| Figma (beta spatial) | SaaS | Partial (REST API) | Limited spatial frame support; primary value is spec documentation, not 3D layout |
| ShapesXR | SaaS | No | VR-native spatial prototyping; collaborative but no agent API |
| Gravity Sketch | SaaS | No | 3D sketching in VR; exports to GLTF for dev handoff |
| WebXR Device API | Browser standard | Yes (script) | Test spatial layouts in browser-based XR without dedicated hardware via emulators |

## Templates & scripts
See `templates.md` (if present) for spatial layout documentation patterns.

Inline helper — compute visual angle and minimum element size at a given distance:
```python
#!/usr/bin/env python3
"""
spatial-comfort.py — compute XR element sizing requirements
Usage: python spatial-comfort.py <distance_meters> <min_visual_angle_degrees>
"""
import sys, math

distance = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
min_angle_deg = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5  # 0.5° min for text

min_angle_rad = math.radians(min_angle_deg)
min_size_m = 2 * distance * math.tan(min_angle_rad / 2)
min_size_cm = min_size_m * 100

# Interaction target minimum (1cm at distance, or 1.5° angular size)
interact_angle_rad = math.radians(1.5)
interact_size_m = 2 * distance * math.tan(interact_angle_rad / 2)

print(f"Distance:          {distance}m")
print(f"Min text size:     {min_size_cm:.2f}cm ({min_angle_deg}° visual angle)")
print(f"Min touch target:  {interact_size_m*100:.2f}cm (1.5° visual angle)")
print(f"Comfort zone:      {'Near (<1m)' if distance < 1 else 'Mid (1-3m)' if distance < 3 else 'Far (3m+)'}")
if distance < 0.5:
    print("WARNING: Below 0.5m — vergence-accommodation conflict zone")
```

## Best practices
- Design for the mid field (1-3m) as the default work surface — near field is reserved for immediate feedback, far field for navigation only
- Specify element dimensions in meters (world units) at the intended placement distance, not pixels — pixel sizing is meaningless in XR
- Never place persistent UI above the horizontal plane of the user's eye level — users cannot comfortably look up for extended periods
- Interaction modality assignment must account for platform constraints: visionOS primary = gaze + pinch; Quest primary = hand ray or controller; HoloLens = hand gesture + voice
- Test every layout standing and seated — ergonomic comfort zones differ significantly between postures
- Spatial audio is a design element, not a developer concern — specify audio feedback for all interaction events in the spatial spec

## AI-agent gotchas
- All spatial specifications are hypothetical until validated in a physical headset — treat agent output as a starting brief for human design review, never as implementation-ready specs
- Comfort zone numbers in agent training data may reflect older guidelines (pre-2024 Apple Vision Pro) — verify against current platform HIG for the specific device
- Agents frequently conflate angular size (degrees) with world-space size (meters) — ensure the spec explicitly uses one unit system
- Latency budgets for comfortable XR interaction (gaze tracking < 20ms, hand tracking < 10ms reprojection) are implementation constraints that must be flagged to the engineering team; agents do not surface them
- Human checkpoint required: every spatial layout must be walked through by a designer wearing the target headset before any 3D asset or interaction code is written

## References
- https://www.nngroup.com/articles/spatial-ux/
- https://developer.apple.com/design/human-interface-guidelines/spatial-design
- https://www.interaction-design.org/literature/article/xr-ergonomics
- https://developer.meta.com/horizon/documentation/unity/unity-design/
- https://www.smashingmagazine.com/2025/spatial-ux/
