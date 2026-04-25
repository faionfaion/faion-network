# Agent Integration — AR Design Patterns

## When to use
- Designing AR experiences on iOS (ARKit / RealityKit), Android (ARCore), WebAR (8th Wall, AR.js, model-viewer), Snap Lens Studio, Meta Spark.
- Choosing surface vs. object vs. image-tracked anchoring for content.
- Auditing AR safety + accessibility — obstacle warning, occlusion, AR-free zones, voice/gaze fallback.
- Building maintenance, retail try-on, museum, navigation, or training overlays.

## When NOT to use
- Fully-immersive VR (occluded headset) — see `vr-design-patterns`.
- Mixed-reality productivity workspaces (passthrough Quest / Vision Pro) — see `immersive-design-principles`.
- Pure 2D mobile UI — overlays a camera but no spatial anchoring? Likely standard mobile UX, not AR.
- Low-power smart-glasses with no spatial tracking — different constraints (display only, voice-first).

## Where it fails / limitations
- AR tracking quality varies dramatically by device, lighting, and texture density — guidelines assume "ideal" conditions.
- Battery + thermal limits cap session length to ~10–20 min on phone AR; design must front-load value.
- Occlusion rendering (real things hide AR) is uneven: ARKit People Occlusion, ARCore Depth API, WebXR all differ.
- "Safety mode" is hand-wavy; no standard exists. Each platform handles obstacle warnings differently.
- WebAR has the worst tracking and feature parity; patterns valid for ARKit may not work in browser.
- Multi-user / shared-anchor AR (Cloud Anchors, Spatial Anchors, ARWorldMap) adds privacy + consent concerns the methodology does not cover.

## Agentic workflow
Agents convert use-case + target devices into an anchoring strategy (horizontal surface, vertical surface, image, object, world, geo), an interaction pattern (tap / drag / pinch / gaze / voice), and a safety/accessibility punch list. A separate agent reviews the design against XAUR (XR Accessibility User Requirements) and platform HIG. Implementation hand-off goes to engine-specific agents (ARKit / ARCore / WebXR / Lens Studio). Human XR designer + at least one mobility-impaired tester + outdoor real-world test gate sign-off.

### Recommended subagents
- `faion-ux-ui-designer-agent` — anchor selection, content density, AR/real visual distinction.
- `faion-accessibility-specialist-agent` — voice/gaze parity, contrast, target sizes (44 × 44 minimum on mobile AR).
- `faion-multimodal-ai-agent` — spatial audio, audio descriptions, real-time captioning.
- iOS / Android implementation agent — ARKit / ARCore code; verify perf budget and tracking-quality UX.
- WebAR-specific agent (8th Wall / model-viewer) — handle browser quirks, fallback to non-AR.

### Prompt pattern
```
Role: AR design reviewer.
Input: use case + target devices (iOS/Android/WebAR/Snap/Meta).
For each axis emit {status, evidence, fix}:
  anchoring (surface/image/object/geo) appropriate for use case
  scanning UX (clear "looking for surfaces", lighting/perf hints)
  occlusion (real objects hide AR where required)
  safety (obstacles, AR-free zones, reduced AR while moving)
  accessibility (voice, gaze, captions, color, large targets, exit AR)
  perf (≥30 FPS, battery + thermal mitigations)
```

```
Role: anchoring strategy generator.
Given use case <indoor furniture try-on>, target <iOS+Android>, output anchor
type, fallback chain, and content scale rules. Include "exit AR" affordance,
"AR-free" toggle, and minimum lighting requirement.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Apple ARKit + RealityKit | iOS AR with image / world / object anchors | Xcode 15+ |
| Apple Reality Composer Pro | Spatial layout previewing | Xcode bundled |
| Google ARCore | Android AR; Depth API; geospatial | https://developers.google.com/ar |
| ARCore Geospatial API | Outdoor world-anchored AR via VPS | Same |
| WebXR Device API | Browser AR (Android Chrome, limited iOS) | https://immersiveweb.dev |
| `<model-viewer>` | Open-source AR Quick Look + Scene Viewer | https://modelviewer.dev |
| 8th Wall CLI | WebAR build + deploy | https://www.8thwall.com |
| Niantic Lightship ARDK | World-scale AR + meshing | https://lightship.dev |
| Snap Lens Studio CLI | Snap AR Lenses | https://ar.snap.com/lens-studio |
| Meta Spark Studio | Instagram / Facebook AR effects (legacy; sunsetting 2025) | Verify status before use |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| 8th Wall | SaaS WebAR | Yes — REST + CLI | Cross-browser; commercial license |
| Niantic Lightship | SaaS | Yes — SDK | Cloud anchors, VPS, meshing |
| Apple App Store Connect | SaaS | Partial — REST | Required for ARKit app distribution |
| Google Play Console | SaaS | Partial — REST | Required for ARCore apps |
| Adobe Aero | SaaS | Limited | Designer-led AR prototyping |
| Sketchfab | SaaS | Yes — REST | 3D model hosting + AR delivery |
| Mapbox / Cesium | SaaS | Yes — REST | Geospatial AR base layers |
| Wwise / FMOD | Licensed | Yes — runtime APIs | Spatial audio for AR cues |

## Templates & scripts
See `templates.md` for anchoring matrix and AR safety patterns. Inline anchoring decision schema agents can codegen against:

```json
{
  "use_case": "indoor furniture try-on",
  "primary_anchor": "horizontal_plane",
  "fallback_chain": ["vertical_plane", "image_marker", "manual_placement"],
  "scale": {"unit": "real_world_meters", "user_resize": true, "max_scale_factor": 1.0},
  "tracking": {"min_lux": 200, "perf_target_fps": 30, "perf_min_fps": 24},
  "lifecycle": {
    "scan_phase": {"timeout_s": 8, "user_hint": "Move device slowly across the floor"},
    "place_phase": {"requires_confirmation": true, "preview_translucent": true},
    "interact_phase": {"gestures": ["tap","drag","pinch","two_finger_rotate"], "voice_alts": true}
  },
  "exit": {"always_visible": true, "single_tap": true},
  "ar_free_toggle": true,
  "occlusion": {"people": true, "world_depth": "if_supported"},
  "accessibility": {"voice_commands": true, "min_target_dp": 44, "high_contrast": true, "captions": true}
}
```

## Best practices
- Always provide a non-AR alternative path; some users cannot or will not enter AR (motion, vision, battery, low-end device).
- Surface-detection should give clear "we are looking" feedback within 2 seconds; longer than 8 seconds → fall back.
- Keep AR overlays minimal — every additional layer raises cognitive load and obscures real-world hazards.
- Use light estimation so AR shadows match real lighting; without it, "AR feel" collapses.
- Treat outdoor AR as a different design problem — geospatial accuracy, GPS drift, sunlight contrast, safety.
- Mobile AR target sizes 44 × 44 dp minimum; thumbs are imprecise while holding a phone.
- Every AR session needs a one-tap exit; never trap the user in AR.
- For shared AR, require explicit consent before world-scan data leaves the device.

## AI-agent gotchas
- LLMs default to "place a 3D model on the floor" without specifying surface size or fallback when scanning fails.
- Agents conflate ARKit and ARCore feature sets — image tracking, occlusion, and anchors differ; pin platform.
- WebAR generated samples often skip the iOS-Safari constraints (must use Quick Look, not WebXR for iPhone).
- Agents under-spec lighting requirements — say "good lighting" instead of providing a lux floor or runtime check.
- Voice-command coverage is forgotten unless explicitly required; force agent to list voice equivalents.
- Privacy of camera + spatial-mesh data is rarely flagged; require a privacy note in any shared-anchor design.
- Agents propose smooth dolly-zoom transitions that cause AR motion sickness — clamp camera-driven motion.
- Human-in-loop checkpoints: outdoor real-environment test, low-light test, motion-sensitive tester, accessibility partner review, privacy review for any cloud-anchor / world-mesh upload.

## References
- Apple HIG: Augmented Reality — https://developer.apple.com/design/human-interface-guidelines/augmented-reality
- Google ARCore Best Practices — https://developers.google.com/ar/develop/best-practices
- W3C XR Accessibility User Requirements (XAUR) — https://www.w3.org/TR/xaur/
- NN/g AR UX research — https://www.nngroup.com/articles/ar-ux/
- 8th Wall WebAR docs — https://www.8thwall.com/docs/web/
- Niantic Lightship — https://lightship.dev/docs/
- Snap Lens Studio guidelines — https://docs.snap.com/lens-studio/
