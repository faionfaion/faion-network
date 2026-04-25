# Agent Integration — Spatial Design Tools

## When to use
- Choosing a spatial-design tool for a Vision Pro / Quest / WebXR project before any code is written.
- Mapping a 2D Figma flow to a 3D prototype that must be tested in a headset.
- Pipelining hand-authored XR content (USDZ, glTF, Reality Composer scenes) into Unity or Unreal builds.
- Producing storyboards / annotated wireframes that a coding agent can later translate into XR scene code.

## When NOT to use
- A flat 2D web/mobile project — Figma alone is sufficient, no spatial layer needed.
- Pure text-only voice or chatbot UX (no spatial layer).
- Quick stakeholder demos that can be done with screen-recordings of an existing app.
- Hardware not yet decided — agent will pick wrong tool; lock target headset first.

## Where it fails / limitations
- LLMs cannot author 3D scenes directly; they can only generate scene-graph descriptors (USD, glTF JSON, Unity prefab YAML) for a human to import.
- ShapesXR and Gravity Sketch have no public REST API; agents cannot drive them headlessly.
- Reality Composer Pro is macOS-only and GUI-driven — no CI integration.
- File-format drift between Figma 3D plugins and headset runtimes silently breaks materials, scale, and anchors.
- Performance budgets (draw calls, polycount) are invisible at design time and only surface in headset profiling.

## Agentic workflow
Use Claude as a "spatial pipeline librarian" — it picks the right tool per stage (concept → low-fi → high-fi → production), generates scaffolding (Unity C# MonoBehaviours, USDA scene files, glTF transforms), and writes the headset test plan. The headset-bound creative work (hand-sketching in ShapesXR, sculpting in Gravity Sketch) stays human; the agent prepares import scripts, file conventions, and review checklists around it. Always pair agent output with a human in-headset validation pass — pixel-perfect 2D ≠ comfortable 3D.

### Recommended subagents
- `general-purpose` Claude subagent — pipeline scaffolding, tool selection memo, USD/glTF templates.
- `faion-sdd-executor-agent` — execute spatial-feature SDD tasks (e.g. "build hand-tracked menu") once design assets exist.
- Custom `xr-scene-builder` subagent (if introduced) — Unity/Unreal C++/C# code emission from scene descriptions.

### Prompt pattern
```
Target: Vision Pro, hand + eye tracking, RoomPlan anchored.
Stage: low-fi prototype.
Constraint: must export to USDZ for Reality Composer Pro.
Output: tool recommendation + 1-screen scene graph in USDA + import checklist.
```

```
Given Figma frames at <url>, produce a Unity prefab YAML stub
with one CanvasGroup per frame, world-space scaled to 0.6 m wide,
positioned on a 1.5 m radius arc at user eye height.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `usdpython` / `usdcat` | Convert / inspect USD scenes | https://openusd.org/release/install.html |
| `gltf-pipeline` | glTF optimization, Draco compression | `npm i -g gltf-pipeline` |
| `gltf-validator` | Validate glTF before headset import | `npm i -g gltf-validator` |
| Unity `-batchmode` CLI | Headless Unity build for XR | https://docs.unity3d.com/Manual/CommandLineArguments.html |
| Unreal `RunUAT.bat BuildCookRun` | Headless Unreal XR packaging | https://docs.unrealengine.com/automation/ |
| `xcrun reality-composer-pro` | macOS Reality Composer Pro CLI | https://developer.apple.com/documentation/realitykit |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ShapesXR | SaaS | No public API | Human-in-headset only; agent prepares import notes |
| Gravity Sketch | SaaS | Limited (LandingPad cloud) | Export FBX/OBJ, agent converts downstream |
| Unity Cloud Build | SaaS | Yes (REST API) | Trigger XR builds from agents |
| Unreal Horde | OSS | Yes (REST + CLI) | CI for Unreal projects |
| Reality Composer Pro | macOS app | No | GUI-only, USDZ pipeline only |
| Spark AR Studio | SaaS (sunset 2025) | No | Avoid for new projects |
| Adobe Aero | SaaS | No public API | Export-only |
| Bezi | SaaS | Limited (Figma plugin) | 2D→3D bridge; no agent API yet |

## Templates & scripts
See `templates.md` for handoff document format. Inline glTF→Unity prefab path validator:

```bash
#!/usr/bin/env bash
# validate-xr-handoff.sh — gate before opening in Unity
set -euo pipefail
SCENE="${1:?path to .gltf or .glb required}"
gltf-validator "$SCENE" --json | jq -e '.issues.numErrors == 0' >/dev/null \
  || { echo "FAIL: glTF errors"; exit 1; }
gltf-pipeline -i "$SCENE" -o "${SCENE%.glb}.draco.glb" --draco.compressionLevel=7
echo "OK: validated + draco-compressed"
```

## Best practices
- Pin one tool per stage in the project README; agent should not switch mid-feature.
- Scale all assets to real-world meters at export, never "design units".
- Bake lighting in the design tool; runtime baking blows perf budgets on Quest 3 / Vision Pro.
- Ship a `xr-handoff/` folder with USDZ + glTF + screenshots; agents read the manifest, not the binaries.
- Version 3D assets via Git LFS, not raw Git — diffs are useless and bloat the repo.
- Test on actual hardware every sprint; emulator comfort never matches headset comfort.

## AI-agent gotchas
- Claude can hallucinate Unity APIs that exist only in older XR Toolkit versions — pin the target version in the prompt.
- USDA/USDZ JSON-like syntax fools LLMs into emitting almost-valid files; always run `usdchecker` before import.
- Token-cheap output: ask for scene graphs as JSON, not prose; saves 60–80% tokens vs. natural-language scene descriptions.
- Human checkpoint required before headset upload — comfort, occlusion, and anchor drift cannot be predicted from text.
- Don't let the agent author shaders; ShaderGraph / Material X visual tooling is the source of truth.
- IP risk: Gravity Sketch / ShapesXR cloud may store proprietary models; agent should warn before any cloud upload.

## References
- https://openusd.org/release/index.html
- https://developer.apple.com/visionos/
- https://developers.meta.com/horizon/
- https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/index.html
- https://www.khronos.org/gltf/
- Mike Alger, "VR Interface Design Pre-Visualisation Methods" (2015)
