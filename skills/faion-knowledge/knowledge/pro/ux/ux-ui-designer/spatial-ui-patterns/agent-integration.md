# Agent Integration — Spatial UI Patterns

## When to use
- Designing a visionOS, Quest, HoloLens, or Magic Leap app where 2D windowed metaphors don't suffice (3D scene, room-scale, mixed-reality content).
- Porting an existing 2D app to spatial computing — needs panel-type decisions (world/head/body/hand-locked) and window-management rules.
- Authoring spatial design guidelines for a brand entering XR.
- Reviewing a third-party XR design for ergonomic, accessibility, and field-of-view risks.
- Building HUDs in games or industrial XR (training, telepresence, surgical planning).

## When NOT to use
- Pure phone or desktop products; spatial constructs add cognitive overhead and confuse users.
- Simple 2D content shown inside a headset's flat-window mode (e.g., a Safari tab in visionOS) — standard responsive design rules apply, not spatial-UI patterns.
- Prototyping at the storyboard stage where the platform is undecided; decide platform first, patterns second.
- Static signage / passive AR overlays without interaction.

## Where it fails / limitations
- Panel-type taxonomy (world/head/body/hand) varies by platform: visionOS uses `Window`, `Volume`, `ImmersiveSpace`; Unity XR Interaction Toolkit uses `XR Origin` + tracked-rig anchors; OpenXR has different reference spaces. Pattern names do not transfer 1:1.
- "Head-locked" UI is widely advised against (Apple HIG forbids it for visionOS) — agents recommending it from generic XR sources will fail review.
- Field-of-view, IPD (interpupillary distance), and pass-through optics differ per device; "60° comfortable cone" is a rule of thumb, not a constant.
- Hand-attached UI assumes reliable hand tracking; in environments with gloves, low light, or controllers-only, the pattern collapses.
- Spatial memory only works if anchors persist across sessions; many platforms wipe room mesh on reboot.

## Agentic workflow
Use agents to enumerate pattern fitness against device capabilities and to generate first-pass scene scaffolds. The decision of which panel type fits which content is design-led; agents can produce candidate matrices and emit Unity / Reality Composer Pro / SwiftUI templates from a chosen pattern. Pair every agent suggestion with the platform HIG (visionOS HIG, Meta Horizon OS guidelines, MRTK design guides) — generic spatial advice is the source of most review failures.

### Recommended subagents
- `faion-usability-agent` — orchestrates a spatial usability review against the DO/DON'T list in `README.md`.
- A purpose-built `panel-type-mapper` subagent: input = list of UI surfaces (menu, alert, reference doc, tool palette), output = recommended panel type + platform mapping (visionOS / Quest / HoloLens) + rationale.
- `faion-sdd-executor-agent` — generates SwiftUI `WindowGroup` / `ImmersiveSpace` scaffolds or Unity prefabs from the chosen pattern.
- A `comfort-check` subagent that scores a layout against ergonomic constraints (panel distance, arm-raise frequency, FoV occupancy, motion sickness triggers).

### Prompt pattern
"Given UI surfaces: `[main menu, contextual tools, system alert, reference document]`, target platform `visionOS 2`, pose seated. Map each surface to a panel type from {world-locked, body-locked, hand-attached} and to the corresponding visionOS scene type (`WindowGroup`, `Volume`, `ornament`). Justify each choice against the visionOS HIG."

"Score this layout for ergonomic risk: panel A at 0.3 m world-locked, panel B head-locked overlay, panel C hand-attached on left wrist. Use criteria: arm-raise duration, FoV occupancy >40%, head-locked anti-pattern, occlusion. Emit a table with risk levels and fixes."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Reality Composer Pro | visionOS scene authoring | Bundled with Xcode 15+ |
| Unity 6 + XR Interaction Toolkit | Cross-platform XR app development | https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest |
| Mixed Reality Toolkit (MRTK3) | HoloLens / OpenXR patterns | https://github.com/MixedRealityToolkit/MixedRealityToolkit-Unity |
| ShapesXR | Browser/headset prototyping | https://www.shapesxr.com |
| Meta Spatial SDK | Quest mixed-reality dev | https://developers.meta.com/horizon/develop |
| visionOS Simulator (`xcrun simctl`) | Headless run for CI | https://developer.apple.com/documentation/visionos |
| OpenXR Loader / `openxr_runtime_list` | Runtime introspection | https://www.khronos.org/openxr/ |
| Blender + glTF exporter | Authoring 3D assets | https://www.blender.org / https://www.khronos.org/gltf/ |
| Bezi | Cross-disciplinary 3D design tool | https://bezi.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Apple Reality Composer Pro | Desktop app | Limited (Swift codegen) | visionOS authoritative |
| Unity Cloud | SaaS | Yes (CLI + REST) | Build farm, asset bundles |
| Meta Quest Developer Hub | Desktop app | Partial | Logs and ADB shortcuts |
| ShapesXR | SaaS | Limited | Multi-user XR prototyping |
| Bezi | SaaS | Limited | Figma-like for 3D |
| Sketchfab | SaaS | Yes (REST API) | Asset hosting + glTF |
| Holopundit / Polycam | SaaS | Yes (REST API) | Room/object scanning for anchors |
| Microsoft Mesh | SaaS | Limited | Collaborative spatial spaces |
| Meta Horizon Worlds tools | SaaS | Limited | Social VR; closed ecosystem |
| Niantic Lightship | SaaS | Yes (REST + SDK) | AR cloud, persistent anchors |

## Templates & scripts
See `templates.md` and `examples.md` for panel-decision tables and visionOS / Unity scene scaffolds.

Inline visionOS scaffold:

```swift
// SpatialApp.swift — minimal scene set with Window + Volume + ImmersiveSpace
import SwiftUI
import RealityKit

@main
struct SpatialApp: App {
  var body: some Scene {
    WindowGroup(id: "main") {            // body-locked-ish 2D panel
      ContentView()
    }
    .windowStyle(.plain)

    WindowGroup(id: "tools", for: ToolID.self) { _ in
      ToolPaletteView()                  // body-locked tool surface
    }
    .windowResizability(.contentSize)

    ImmersiveSpace(id: "scene") {        // world-anchored 3D content
      RealityView { content in
        let anchor = AnchorEntity(.head)
        content.add(anchor)
      }
    }
    .immersionStyle(selection: .constant(.mixed), in: .mixed)
  }
}
```

## Best practices
- Default to **world-locked** for reference content and **body-locked** for primary UI; reserve hand-attached for ephemeral / quick-access tools.
- Set comfort distance ≥ 1 m for primary panels; closer than 0.5 m forces vergence-accommodation conflict.
- Cap panel angular size at ~40° of FoV; bigger surfaces force head movement.
- Keep all interactive targets ≥ 60×60 pt at 1 m apparent distance (visionOS), or ≥ ~3 cm physical for direct touch.
- Provide redundant input modalities: gaze-and-pinch, controller, voice — never assume hand tracking is reliable.
- Use depth and parallax to convey hierarchy, not size alone; size scales unpredictably with distance.
- Persist anchors across sessions where possible (`ARWorldMap`, OpenXR persistent anchors); rebuild gracefully when persistence fails.
- Test seated, standing, and walking poses; layouts that work seated often fail at room scale.
- Add accessibility: provide flat-window fallback for users who cannot tolerate immersive content.

## AI-agent gotchas
- Models often confuse AR overlay (phone-screen) patterns with HMD (headset) patterns — prompts must specify the device class.
- LLMs cite "head-locked HUD" as standard practice from older XR literature; current Apple/Meta guidance is the opposite.
- Coordinate system gotchas: visionOS uses meters, Unity uses meters by default but assets often arrive in cm; agents drop one zero and put panels 10 m away.
- Generated SwiftUI scenes frequently mix `Window` and `ImmersiveSpace` incorrectly; only one ImmersiveSpace can be active.
- Hand-tracking gestures named differently per platform ("pinch" vs "select" vs "air-tap") — agents must use platform terms in code.
- Generated assets may use disallowed shaders (e.g., transparent on visionOS performance budget) — require shader review.
- Voice intents in spatial apps need privacy disclosures; agent-generated code often omits Info.plist usage strings, blocking App Store review.

## References
- Apple visionOS Human Interface Guidelines — https://developer.apple.com/design/human-interface-guidelines/visionos
- Meta Horizon OS UX guidelines — https://developers.meta.com/horizon/design
- Microsoft Mixed Reality Design Guidelines — https://learn.microsoft.com/en-us/windows/mixed-reality/design/design
- Khronos OpenXR specification — https://registry.khronos.org/OpenXR/
- Mike Alger — *VR Interface Design Pre-Visualisation Methods* (foundational, 2015)
- Jason Jerald — *The VR Book: Human-Centered Design for Virtual Reality* (ACM Books)
