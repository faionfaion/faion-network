# Agent Integration — Spatial UX Fundamentals

## When to use
- Drafting first-pass UX requirements for an Apple Vision Pro, Meta Quest, or Microsoft HoloLens app.
- Re-mapping a 2D mobile/desktop flow into near/mid/far field zones.
- Reviewing a spatial layout for reach, occlusion, sight-line, and orientation issues.
- Establishing a spatial design vocabulary across cross-functional teams (PM/eng/3D).

## When NOT to use
- Phone-AR snap-on features (banner overlays) where world-scale and reach don't apply meaningfully.
- Desktop 3D viewers (CAD, Blender) — different ergonomic constraints than head-mounted spatial.
- 360° video lean-back content — viewer is passive, no reach/occlusion design needed.

## Where it fails / limitations
- Field guidance (0-1m / 1-3m / 3m+) assumes seated/standing immersive use; doesn't fit pass-through desk work or walking AR.
- Anthropometric averages mask huge variance — children, wheelchair users, short-arm reach all break "comfortable arm reach".
- Fundamentals are device-agnostic; they don't compensate for FoV (Quest 3 ≈ 110°, Vision Pro ≈ 100°) or eye-tracking presence.
- Static field zones don't account for moving users, vehicles, or multi-room layouts.
- Pure principles, no validation method — must be paired with usability testing in HMD.

## Agentic workflow
Drive Claude to translate a 2D wireframe into a spatial spec: place each surface in near/mid/far field, annotate world-scale, and flag occlusion risks. A second agent runs a heuristic checklist (reach, peripheral content, anchoring) against the spec. Use Reality Composer Pro / Unity scene exports as the source-of-truth artifact, not screenshots.

### Recommended subagents
- `faion-ux-researcher-agent` — synthesize HMD usability sessions into spatial-specific findings.
- `faion-usability-agent` — heuristic eval against spatial principles.
- A custom `spatial-spec-linter` — parse USDZ/glTF scene metadata, flag elements >3m or <0.4m from head anchor.

### Prompt pattern
```
Given <2D wireframe> for <task>, produce a spatial spec:
- For each panel/control, assign field (near/mid/far) and rationale.
- World-scale (cm) for primary/secondary content.
- Sight-line and occlusion risks.
- Anchoring (head-locked vs. world-locked vs. hand-attached).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `xcrun usdz` | Inspect/convert USDZ scenes for Vision Pro | bundled with Xcode |
| `usdview` (Pixar) | Inspect USD scene graph, world units | github.com/PixarAnimationStudios/OpenUSD |
| `gltf-validator` | Validate glTF assets used in WebXR | `npm i -g gltf-validator` |
| `unity-cli` (`UnityEditor.exe -batchmode`) | Headless build of XR scenes from CI | docs.unity3d.com/Manual/CommandLineArguments.html |
| `meta-quest-developer-hub` | Sideload + capture metrics on Quest | developer.oculus.com/downloads |
| `apple-vision-simulator` (xcrun simctl) | Drive Vision Pro simulator from CLI | developer.apple.com/visionos |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reality Composer Pro | Free (Apple) | Limited (file-based) | Author Vision Pro scenes; agent edits via USDA text |
| Unity 6 + XR Interaction Toolkit | Commercial | Yes (CLI build) | Standard XR engine, batch builds via CLI |
| Unreal Engine 5 + OpenXR | Commercial | Partial | Heavier, less agent-friendly than Unity |
| Bezi | SaaS | Yes (REST) | Spatial wireframing; export to JSON |
| ShapesXR | SaaS | Limited | Multi-user spatial sketching |
| Spatial.io | SaaS | No | End-user spatial collab, not authoring |
| WebXR / Three.js | OSS | Yes | Procedural scene gen from agent, run in browser |

## Templates & scripts
See `templates.md`. Inline spec-linter stub (≤50 lines):

```python
import json, sys
NEAR_MIN, NEAR_MAX = 0.30, 1.00
MID_MAX, FAR_MIN = 3.00, 3.00
def lint(spec):
    issues = []
    for el in spec["elements"]:
        d = el["distance_m"]; field = el["field"]
        if field == "near" and not (NEAR_MIN <= d <= NEAR_MAX):
            issues.append(f"{el['id']}: near field expects 0.3-1m, got {d}m")
        if field == "mid" and not (NEAR_MAX < d <= MID_MAX):
            issues.append(f"{el['id']}: mid field expects 1-3m, got {d}m")
        if field == "far" and d < FAR_MIN:
            issues.append(f"{el['id']}: far field expects >3m, got {d}m")
        if el.get("interactive") and field == "far":
            issues.append(f"{el['id']}: interactive content placed in far field (reach issue)")
        if el.get("text") and d > 3 and el.get("font_pt", 0) < 60:
            issues.append(f"{el['id']}: text in far field needs ≥60pt for legibility")
    return issues
if __name__ == "__main__":
    for i in lint(json.load(open(sys.argv[1]))): print(i)
```

## Best practices
- Anchor primary controls hand-attached or head-locked-with-decay; pure world-locked controls force users to walk.
- Reserve far field for ambient/contextual content; never put primary CTAs there.
- Use 1.5-2.0m as default content distance — comfortable for sustained viewing on Quest/Vision Pro.
- Provide a "recenter" affordance (button or voice) — users drift, and snapping to home pose recovers fast.
- Test seated AND standing — comfortable reach changes by ~15° and breaks bottom-edge controls.
- Avoid placing critical UI in the lower 30° of FoV (chin region) — fatiguing to look down repeatedly.

## AI-agent gotchas
- Claude defaults to thinking in pixels/dp; force unit normalization to meters in every prompt or it produces nonsense scales.
- Generated USD/glTF from LLMs often has incorrect Y-up vs. Z-up — always validate before opening in engine.
- LLMs over-recommend "skeuomorphic" 3D buttons; remind to follow platform Human Interface Guidelines (Vision Pro vibrancy, hover states).
- Human-in-loop checkpoint: any layout >2m away or <0.4m needs a designer with HMD-on review — agents cannot judge eye fatigue.
- Don't let agents auto-generate 3D assets from text-to-3D for production; quality, scale, and licensing all break.

## References
- Apple Human Interface Guidelines — Vision Pro / Spatial Design — developer.apple.com/design/human-interface-guidelines/spatial-design
- Meta Quest VR Design Guidelines — developer.oculus.com/resources/bp-vrcomfort
- Microsoft Mixed Reality Design — learn.microsoft.com/windows/mixed-reality/design
- *Designing for Mixed Reality* — Kharis O'Connell
- Unity XR Interaction Toolkit docs — docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit
