# Agent Integration — Spatial UI Patterns

## When to use
- Designing UI for visionOS, Meta Quest (Horizon OS), HoloLens, Magic Leap 2, or Android XR.
- Porting 2D mobile/desktop apps to spatial environments and choosing panel anchoring.
- Defining window-management rules (snap, group, dock, recall) for an XR product.
- Reviewing existing XR UIs for fatigue (arm-raising, near-field clutter, FOV violations).

## When NOT to use
- 2D mobile/desktop UIs — patterns assume 3D positioning and head/hand tracking.
- AR overlays on flat phone screens (handheld AR like ARKit on iPhone) — those have a different interaction model; some patterns transfer but anchoring rules differ.
- VR-only games where bespoke diegetic UI dominates — system patterns may conflict with game fiction.

## Where it fails / limitations
- Apple visionOS, Meta Horizon OS, and Android XR have diverging anchoring vocabularies (windows, volumes, immersive spaces vs panels vs surfaces); mapping is not 1:1.
- Hand-attached UI assumes hand tracking; controller-only experiences need different ergonomics.
- "Respect personal space" is anthropometric and varies by user height/seated-vs-standing — methodology gives no measured ranges.
- Spatial memory ("return to position") requires persistent world anchors which are platform-specific (ARKit world map, OpenXR Reference Spaces).
- Patterns are silent on shared/multi-user spatial UI (co-presence, avatars, ownership of panels).

## Agentic workflow
Spatial UX work has more constraints than freedom — agents are useful for constraint checking, not for creative anchoring decisions. Pipeline: (1) `panel-classifier` infers the right anchor type from a panel's content+behavior spec, (2) `comfort-checker` verifies placement against angular/distance/FOV constraints per platform, (3) `interaction-mapper` proposes input modalities (gaze+pinch, hand ray, controller). Always pair with human prototyping in-headset — agents cannot feel arm fatigue.

### Recommended subagents
- `panel-classifier` — sonnet; given content type + persistence requirements, recommends world/head/body/hand-locked anchor and rationale.
- `comfort-checker` — haiku; deterministic checks (FOV ≤ 30° eccentric, panel distance 0.5-2 m, eye-line ±15°) against a spec.
- `xr-input-mapper` — sonnet; suggests gestures/voice/gaze for a given affordance, per platform.
- `xr-flow-author` — sonnet; writes step-by-step user flows including head/hand state transitions.

### Prompt pattern
```
You are panel-classifier. Inputs: {content_type, persistence, interaction_freq,
collaborative}. Choose anchor in {world, head, body, hand} and justify in <=25
words. Output JSON: {anchor, rationale, comfort_warnings:[...], platform_notes:{visionos, horizon_os, android_xr}}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `xcrun simctl` (visionOS Sim) | Boot/run visionOS simulator from CLI | developer.apple.com/visionos |
| `unity hub` CLI | Build XR projects (XR Interaction Toolkit) | docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit |
| `meta-spatial-sdk` CLI | Build/deploy to Quest devices | developer.oculus.com/documentation/spatial-sdk |
| `adb` | Sideload + log Quest/Android XR apps | developer.android.com/tools/adb |
| `openxr-runtime` (Monado) | OSS XR runtime for testing | monado.freedesktop.org |
| `wave` (HTC Vive Wave SDK CLI) | Multi-device XR builds | developer.vive.com/resources/vive-wave |
| `usdz-tools` / `usdpython` | Author/inspect USDZ assets for visionOS panels | github.com/PixarAnimationStudios/USD |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apple Reality Composer Pro | SaaS (Apple-only) | Limited — file format scriptable | Authoring USDZ; agents can mutate USD via usdpython |
| Unity XR Interaction Toolkit | OSS (Unity license) | Yes — C# + CLI builds | De facto cross-platform XR layer |
| Unreal OpenXR | OSS (Unreal license) | Yes — Python scripting | Heavier weight, fewer mobile XR options |
| Meta Spatial SDK (Android-based) | SaaS | Yes — Gradle/CLI | Android XR + Horizon OS targets |
| Microsoft MRTK3 | OSS | Yes — Unity packages | HoloLens + cross-platform spatial UI primitives |
| ShapesXR | SaaS | Limited — collaborative authoring | Useful for spatial mockups before code |
| Bezi / Gravity Sketch | SaaS | Limited — export to GLTF/USD | 3D wireframing |

## Templates & scripts
See `templates.md` for panel anchor decision matrix. Comfort check (TS):

```ts
// comfort_check.ts — flag spatial panels outside ergonomic envelope
type Panel = { id: string; distance_m: number; eccentricity_deg: number; size_m: [number, number]; anchor: "world"|"head"|"body"|"hand" };

const RULES = {
  distance_m: [0.5, 2.0],
  eccentricity_deg: 30,        // off-center from forward gaze
  min_size_m: 0.04,            // ~4 cm — touch target floor in spatial
  hand_distance_m: [0.25, 0.5] // hand-attached safe range
};

export function checkComfort(p: Panel): string[] {
  const issues: string[] = [];
  const [lo, hi] = RULES.distance_m;
  if (p.anchor !== "hand" && (p.distance_m < lo || p.distance_m > hi)) issues.push(`distance:${p.distance_m}`);
  if (p.eccentricity_deg > RULES.eccentricity_deg) issues.push(`fov-edge:${p.eccentricity_deg}`);
  if (Math.min(...p.size_m) < RULES.min_size_m) issues.push(`too-small:${p.size_m}`);
  if (p.anchor === "hand") {
    const [hl, hh] = RULES.hand_distance_m;
    if (p.distance_m < hl || p.distance_m > hh) issues.push(`hand-range:${p.distance_m}`);
  }
  return issues;
}
```

## Best practices
- Default to body-locked menus for tools used while moving and world-locked for reference content; head-locked is reserved for transient notifications, never for primary nav.
- Reserve hand-attached UI for one or two high-frequency actions (mode toggle, undo). More than that and the hand becomes a busy toolbar.
- Test panel placement with at least 5 users including short and tall — methodology's "ergonomic" defaults are based on a 50th-percentile adult.
- Animate panel summon/dismiss with a spatial "from-source" anchor (origin point on the body or hand) — instant pop-in disorients.
- Use depth as a secondary hierarchy after color/typography, not a primary one — many users have reduced stereo acuity.
- Provide a "recenter" gesture/voice command that returns body-locked UI to a comfortable default — users drift, content should not.
- Preserve spatial memory across sessions: persist anchor positions per-user, not per-app-launch.

## AI-agent gotchas
- LLMs producing Unity/visionOS code often emit deprecated APIs (e.g., `OVRPlugin` calls renamed in 2024+). Pin SDK versions in the prompt and require API references.
- Coordinate systems differ (visionOS Y-up right-handed meters, Unity Y-up left-handed meters, Unreal Z-up cm). Agents must declare assumptions; converting at the wrong layer breaks panel placement.
- "Respect personal space" is hard to verify from a static spec — agents need access to a runtime distance probe; without it they will pass clearly invalid layouts.
- Voice + gaze + pinch is a common visionOS combo, but availability is hardware-gated. Check capability flags before proposing modalities.
- Multi-window layouts on Quest/Android XR have OS-level limits (window count, GPU memory). Agents must consult platform manifests, not invent caps.
- USD/USDZ authoring is finicky — agents that mutate scenes must validate via `usdcat` or similar before shipping.
- Spatial UI accessibility (color blindness, low vision, motor impairments, vestibular sensitivity) is under-served by the methodology; lean on accessibility-specialist methodologies in parallel.

## References
- Apple Human Interface Guidelines — visionOS, "Designing for visionOS" (developer.apple.com/design/human-interface-guidelines/designing-for-visionos).
- Meta XR Design Guidelines — developer.oculus.com/resources/oculus-design-guidelines.
- Microsoft MRTK3 docs — learn.microsoft.com/windows/mixed-reality/mrtk-unity.
- "3D User Interfaces: Theory and Practice" — Bowman et al.
- OpenXR specification — khronos.org/openxr.
- Nielsen Norman Group — "Spatial UI" articles (nngroup.com).
