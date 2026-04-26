# Agent Integration — AR Design Patterns

## When to use
- Designing handheld AR (ARKit/ARCore) or headset AR (Vision Pro, Quest passthrough, HoloLens) experiences.
- Use cases: navigation overlays, product visualization (e-commerce), training/maintenance, shared annotations, contextual data labels.
- Defining placement strategies (surface detection, object recognition, world anchoring) and content scale rules.
- Authoring guardrails for "respect reality": occlusion, lighting integration, safe boundaries.

## When NOT to use
- 2D mobile features that only need a camera (QR scanning, barcode lookup) — AR overhead is unjustified.
- Marketing one-shots without a follow-up plan — AR demos rot when SDK versions change.
- Fully immersive VR — different ergonomic rules; use vr-design-patterns or spatial-design-tools.
- Public unsupervised contexts where safety / occlusion of real hazards (stairs, traffic) is unmanageable.

## Where it fails / limitations
- Outdoor lighting variability breaks plane detection and color matching (especially Quest passthrough).
- "Object recognition" is brittle outside trained classes — needs custom CoreML / ARCore Augmented Images.
- Battery drain: continuous tracking + render at 60 fps drains a phone in 30-45 minutes.
- Privacy: AR cameras capture bystanders — raise red flags in EU/CA/IL jurisdictions.
- Cross-platform parity (ARKit ↔ ARCore ↔ WebXR) is partial; agents over-promise feature equivalence.
- Cybersickness from misaligned overlays at >70ms latency.

## Agentic workflow
Use a subagent to draft AR placement specs (anchor type, scale, occlusion behavior) from a use-case brief, then generate a USDZ / GLB with the right pivot and bounding box and a Reality Composer Pro / Unity / WebXR scene. A second agent runs an automated checklist on the build (FPS, plane-loss recovery, audio cues, exit affordance). Human design review must clear any feature that occludes safety-critical reality.

### Recommended subagents
- `faion-usability-agent` — drafts AR interaction flows, exit affordances, sensory comfort defaults.
- `faion-ux-researcher-agent` — runs in-environment user tests with comfort + presence questionnaires.
- `faion-sdd-executor-agent` — wires Reality Composer / Unity / WebXR scene with chosen anchors.

### Prompt pattern
```
For use-case <case>, output AR placement spec: anchor type
(plane / image / object / world), default scale, max scale,
occlusion mode, lighting estimation on/off, safe-zone radius.
Flag any value that would obscure walking paths.
```

```
Generate a Reality Composer Pro scene description with one
USDZ asset anchored to a horizontal plane, with audio cue,
re-localization fallback, and a 'tap to dismiss' affordance.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `xcrun reality-tool` (Reality Composer Pro CLI) | Build / inspect Reality files for visionOS/iOS | bundled with Xcode 15+ |
| `usdzconvert` / `usdcat` | Inspect / convert USDZ | github.com/PixarAnimationStudios/OpenUSD |
| `gltf-pipeline` / `gltf-validator` | Validate GLB used in WebXR/ARCore | github.com/CesiumGS/gltf-pipeline |
| `arcore-extensions` (Unity CLI) | ARCore project tooling | developers.google.com/ar |
| Unity `bee` / `unity` CLI | Build AR Foundation projects headlessly | docs.unity3d.com |
| Wonderland Engine CLI | WebXR scene tooling | wonderlandengine.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Reality Composer Pro | OSS+SaaS (Apple) | Partial — scriptable via reality-tool | Targets visionOS / iOS. |
| Unity AR Foundation | SaaS | Yes — CLI builds, scriptable | Cross-platform ARKit/ARCore. |
| 8th Wall | SaaS | Yes — REST + CLI | Best WebAR; agents can deploy via API. |
| Niantic Lightship | SaaS | Yes — Unity SDK + cloud | Persistent AR meshes. |
| Snap Lens Studio | SaaS | Partial — desktop app first | Distribution via Snap network. |
| Adobe Aero | SaaS | No — GUI-only | Avoid for agent workflows. |

## Templates & scripts
See `templates.md` and `examples.md`. Inline minimal WebXR (three.js + AR module) skeleton:

```js
import * as THREE from "three";
import { ARButton } from "three/examples/jsm/webxr/ARButton.js";

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.xr.enabled = true;
document.body.append(renderer.domElement, ARButton.createButton(renderer, {
  requiredFeatures: ["hit-test", "local-floor"],
  optionalFeatures: ["light-estimation", "anchors"],
}));
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera();
const reticle = new THREE.Mesh(
  new THREE.RingGeometry(0.08, 0.10).rotateX(-Math.PI / 2),
  new THREE.MeshBasicMaterial({ color: 0xffffff })
);
reticle.matrixAutoUpdate = false;
reticle.visible = false;
scene.add(reticle);
renderer.setAnimationLoop(() => renderer.render(scene, camera));
```

## Best practices
- Always show a reticle / surface preview before placement — never auto-place on first hit.
- Provide a clear exit affordance reachable by a single tap or controller button.
- Cap content scale to avoid eye-vergence conflict (>2 m closer than 0.5 m focus is uncomfortable).
- Use lighting estimation on phones; on Quest passthrough, prefer matte unlit shaders.
- Render shadows/contact shadows under placed objects — biggest single perceived-realism win.
- Audio cues are AR's primary feedback channel — never ship silent placement.

## AI-agent gotchas
- Agents conflate ARKit world tracking with ARCore — features like "scene mesh" are not equivalent.
- LLMs hallucinate Reality Composer Pro APIs; ground via current Apple sample code.
- Agents underestimate device thermal throttling — ship with low-poly + LOD by default.
- Camera + microphone permissions are PII gates; agents must produce a privacy disclosure string.
- Bystander capture: agent must include a "do not record" affordance in shared sessions.
- Never let an agent auto-publish AR content for kids without COPPA/GDPR-K review.

## References
- ARKit Human Interface Guidelines — developer.apple.com/design/human-interface-guidelines/augmented-reality
- Google AR Design Guidelines — developers.google.com/ar/design
- WebXR Device API — www.w3.org/TR/webxr/
- Mike Alger, "VR Interface Design Pre-Visualisation Methods" (still applies to AR comfort) — vimeo.com/141330081
- 8th Wall AR best practices — 8thwall.com/blog/category/best-practices/
- Unity XR Interaction Toolkit docs — docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit
