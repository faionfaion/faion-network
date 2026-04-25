# Agent Integration — Spatial Design Tools

## When to use
- Choosing a tool stack for AR/VR/MR projects across concept → prototype → production.
- Setting up a designer–developer handoff path for spatial work (Figma 2D wireframes → ShapesXR → Unity/Unreal).
- Evaluating a one-person solopreneur stack for visionOS, Quest, or WebXR delivery.
- Onboarding designers from 2D backgrounds; tool selection drives the learning curve.

## When NOT to use
- 2D-only projects — pulling spatial tools in adds setup tax with no payoff.
- Teams already locked into a vendor (Unity-only Meta dev shop) — re-evaluating mid-project rarely pays back.
- Marketing-only AR effects — Spark AR / Lens Studio handle the niche; the broader landscape is overkill.

## Where it fails / limitations
- Tool fidelity gaps: ShapesXR concepts look different in Unity; expect re-design at the prototype stage.
- File-format zoo (USDZ, glTF, FBX, USD, custom Unity prefabs) breaks naive automation pipelines.
- Many tools have no public API (Reality Composer Pro, Spark AR Studio) — agentic automation stops at "open in app, click."
- Hardware lock-in: Reality Composer Pro requires macOS + Vision Pro; ShapesXR requires Quest. CI is awkward.
- Performance budgets only become real in target engine; concept-tool exports rarely respect them.

## Agentic workflow
Use agents to (a) recommend the right tool per project phase given device and team constraints, (b) automate format conversions and asset-budget linting, and (c) generate handoff documentation. Tool choice itself remains human; agents help narrow but the team's existing skill stack dominates the decision.

### Recommended subagents
- `faion-ux-researcher-agent` — assembles tool comparison matrix from current vendor docs, refreshed quarterly.
- `faion-sdd-executor-agent` — implements export/conversion scripts and CI hooks once tooling is selected.

### Prompt pattern
```
Recommend a spatial design tool stack for:
  team_size: <N>
  primary_device: VisionPro|Quest|HoloLens|Web
  fidelity_target: concept|hi-fi-prototype|production
  budget_usd_year: <N>
  existing_skills: [Figma, Unity, Blender, ...]

Output JSON:
  concept: {tool, reason}
  prototype: {tool, reason}
  production: {engine, reason}
  asset_pipeline: [tool→tool, format]
  handoff_format: USDZ|glTF|prefab
  estimated_learning_curve_per_role: {role: weeks}
Cite vendor docs only — no invented features.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `usdcat` / `usdview` | Inspect, validate, convert USD/USDZ | https://openusd.org |
| `gltf-validator` | Validate glTF spatial assets | https://github.khronos.org/glTF-Validator/ |
| `realitytool` | Apple visionOS USDZ packaging | Xcode 15+ |
| `Blender --background --python` | Headless asset processing, format conversion | https://www.blender.org |
| `Unity -batchmode -nographics` | Headless build, asset import pipeline | Unity docs |
| `unreal-cli` (UnrealBuildTool) | Headless Unreal builds | UE docs |
| `gltf-pipeline` | glTF compression, Draco, Meshopt | https://github.com/CesiumGS/gltf-pipeline |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma + 3D plugins | SaaS | Partial (REST + plugin API) | Concept stage; export limited. |
| ShapesXR | SaaS | Limited | VR-native concept; manual export to Unity. |
| Gravity Sketch | SaaS | Partial | VR design; export FBX/OBJ/USD. |
| Bezel | SaaS | Yes (REST) | Browser-first spatial tool. |
| Unity | Commercial | Yes (CLI + Cloud Build) | Production VR/AR engine. |
| Unreal Engine | Source-available | Yes (Horde, BuildGraph) | Higher fidelity, MetaHumans. |
| Reality Composer Pro | macOS app | No | visionOS-only; manual workflow. |
| Spark AR / Lens Studio | SaaS | No | Vendor-locked AR effect tools. |
| Adobe Aero | SaaS | No | Sunset-track; avoid for new projects. |
| Polycam / Luma AI | SaaS | Yes (REST) | 3D capture → glTF/USDZ for asset library. |

## Templates & scripts
See `templates.md` for tool-selection matrix. Inline asset-budget lint:

```bash
#!/usr/bin/env bash
# spatial-budget.sh — fail CI if asset exceeds spatial budget
set -euo pipefail
ASSET="${1:?path}"
MAX_TRIS="${MAX_TRIS:-100000}"
MAX_MB="${MAX_MB:-15}"

SIZE_MB=$(du -m "$ASSET" | cut -f1)
TRIS=$(gltf-pipeline -i "$ASSET" --stats 2>/dev/null | awk '/triangles/{print $2}')

[ "$SIZE_MB" -le "$MAX_MB" ] || { echo "FAIL size $SIZE_MB MB > $MAX_MB"; exit 1; }
[ "$TRIS" -le "$MAX_TRIS" ] || { echo "FAIL tris $TRIS > $MAX_TRIS"; exit 1; }
echo "OK $ASSET — ${SIZE_MB}MB / ${TRIS} tris"
```

## Best practices
- Pick tools per phase, not per project. Concept in Figma + ShapesXR, prototype in Unity, production in Unity or Unreal.
- Standardize on USD/USDZ for visionOS handoff; glTF for Web/Quest. Pick one per device and stick to it.
- Set polygon and texture budgets at concept time, not after the artist has spent two weeks on assets.
- Keep a "single source of truth" repo for shared assets; tool-specific copies drift within a sprint.
- Test in target headset by week 2 of any project; concept-tool fidelity hides 80% of the comfort issues.
- Document the export chain step-by-step; a single missing flag (axis swap, scale unit) burns hours per asset.

## AI-agent gotchas
- Vendor feature lists shift fast; LLMs trained months ago miss recent additions and removals. Cite live URLs.
- "Reality Composer" vs. "Reality Composer Pro" are different tools; agents conflate them constantly.
- WebXR vs. native engine confusion: agents will recommend Three.js for a Vision Pro project (wrong runtime).
- Asset pipeline scripts must declare unit (meters), axis (Y-up vs. Z-up), and handedness; LLMs omit these and produce subtly broken assets.
- Performance estimates from agents are folklore. Always benchmark on target hardware.
- Subscription tiers and per-seat pricing change quietly; agent budget recommendations need a manual-confirm gate.

## References
- Apple, *Designing for visionOS — Tools*. https://developer.apple.com/visionos/
- Meta, *Designing for Quest*. https://developer.oculus.com/design/
- Khronos, *glTF 2.0 Specification*. https://www.khronos.org/gltf/
- Pixar / Apple, *Universal Scene Description (USD)*. https://openusd.org
- Unity, *XR Interaction Toolkit Documentation*.
- Unreal Engine, *XR Development Documentation*.
