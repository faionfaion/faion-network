# Agent Integration — Immersive Design Principles

## When to use
- Designing or auditing VR/AR/MR/passthrough experiences across Meta Quest, Apple Vision Pro, PSVR2, PICO, HoloLens.
- Choosing the right immersion level (passthrough → blended → fully immersive → portal) for a use case.
- Reviewing comfort settings, locomotion, grounding, and motion-sickness mitigations before user testing.
- Making spatial UIs accessible — vision, hearing, mobility, and cognitive needs in XR.

## When NOT to use
- Pure 2D web/mobile work — use `wcag-22-compliance` and `a11y-basics` instead.
- Game-feel tuning where intentional motion sickness is part of the design loop (rare; horror, simulation niches).
- Hardware/optics tuning (IPD, lens distortion) — those live in engine/SDK layer, not UX guidelines.
- Conversion-rate optimization for XR storefronts — adjacent topic, not this skill.

## Where it fails / limitations
- Guidelines are platform-vendor consensus; novel XR form factors (smart glasses, AR contact lenses, neural inputs) outpace them.
- Frame-rate / latency floors (90 FPS, <20ms motion-to-photon) are device-class assumptions — mobile AR has different floors.
- "Comfort" is heavily individual: a 5% nausea-prone subgroup will fail experiences that test fine on the rest.
- Accessibility recs here overlap `vr-design-patterns`, `ar-design-patterns`, `spatial-accessibility` — agents must avoid duplicate work.
- Most heuristics are not testable from code alone — require headset + human or in-headset analytics.

## Agentic workflow
Use the methodology as a checklist for design review and a generator for comfort/accessibility settings menus. Agents drive the structured passes (immersion-level fit, locomotion options matrix, grounding/horizon presence, comfort settings completeness) and emit a punch list. Human XR designers and at least one motion-sensitive tester gate any approval. Code-level checks (FPS budget, latency, controller mapping) belong to engine-specific subagents (Unity, Unreal, WebXR), not this one.

### Recommended subagents
- `faion-ux-ui-designer-agent` — translate immersion-level choice into wireframes, panel placement, and diegetic vs. meta UI split.
- `faion-accessibility-specialist-agent` — audit comfort + accessibility coverage matrix per disability type.
- `faion-multimodal-ai-agent` — review spatial-audio cues, haptic + audio sync, audio-description scripting.
- A Unity/Unreal-specific implementation agent (project-local) — verify XR Interaction Toolkit / OpenXR config matches the design.

### Prompt pattern
```
Role: XR design reviewer.
Input: experience description (use case, target devices, session length).
Audit against: immersion-level fit, grounding/horizon, locomotion options ≥2,
comfort settings (vignette, snap turn, seated, FOV cap), accessibility per
WAI XAUR (vision, hearing, mobility, cognitive), perf floor (90 FPS / <20ms).
Output: table {category, status: pass/warn/fail, evidence, fix}.
```

```
Role: comfort-settings generator.
Given device <Quest 3 | Vision Pro | PSVR2 | WebXR mobile>, produce a JSON
settings menu schema with defaults set to highest-comfort (snap turn, teleport,
vignette on, seated). Include reduce-motion, reduce-particles, high-contrast,
caption-size, audio-balance per source.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity XR Interaction Toolkit | Built-in locomotion, comfort vignette, snap turn | `com.unity.xr.interaction.toolkit` (UPM) |
| Unreal OpenXR + VR Template | Unreal equivalent, includes teleport + comfort | https://dev.epicgames.com/documentation/en-us/unreal-engine/vr-template-in-unreal-engine |
| WebXR Device API + three.js | Browser XR experiences | https://immersiveweb.dev |
| OVRMetricsTool | Quest perf overlay (FPS, latency, GPU/CPU) | sideload from Meta Developer Hub |
| Apple Reality Composer Pro | Vision Pro spatial layout previewing | Xcode 15+ |
| `xr-accessibility-checklist` (W3C XAUR) | Reference checklist | https://www.w3.org/TR/xaur/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Horizon Developer Hub | SaaS | Partial — CLI for app deploy | Quest perf + crash data |
| Apple App Store Connect | SaaS | Partial — App Store Connect API | visionOS reviews, crash reports |
| Unity Cloud / DeepLink | SaaS | Yes — REST | XR analytics + remote config for comfort defaults |
| Resolution Games / OWLET (OSS) | OSS | Limited | Open spatial UI patterns library |
| Hurricane VR | Asset Store package | Yes via Unity tooling | Reference physics interaction set |
| AfterNow Prototype | SaaS | No — designer tool | Faster XR prototyping |
| Fmod / Wwise | SaaS/licensed | Yes — runtime APIs | Spatial audio integration; agent can author event banks |

## Templates & scripts
See `templates.md` for the comfort-settings schema and locomotion-options matrix. Inline schema fragment for a comfort menu agents can codegen against:

```json
{
  "comfort": {
    "locomotion": {"type": "enum", "values": ["teleport","smooth","seated"], "default": "teleport"},
    "turning": {"type": "enum", "values": ["snap_30","snap_45","smooth"], "default": "snap_30"},
    "vignette": {"type": "enum", "values": ["off","light","medium","strong"], "default": "medium"},
    "fov_cap_during_motion": {"type": "number", "min": 50, "max": 110, "default": 80},
    "seated_mode": {"type": "boolean", "default": false},
    "height_offset_cm": {"type": "number", "min": -30, "max": 30, "default": 0}
  },
  "visual": {"high_contrast": false, "text_scale": 1.0, "reduce_particles": false, "reduce_screen_shake": true},
  "audio": {"captions": true, "spatial_audio": true, "balance": 0.5, "per_source_volume": true},
  "interaction": {"hand_tracking": true, "voice_commands": true, "dwell_select_ms": 1500}
}
```

## Best practices
- Default every new XR experience to the highest-comfort settings; let users opt into lower comfort, never the other way.
- Always offer at least two locomotion methods (teleport + smooth, or teleport + seated).
- Never head-lock UI; world-locked or body-locked panels at 1.5–3 m, eye-level.
- Run a 30-minute extended-session test before shipping — short demos hide fatigue and drift.
- Couple every visual transition with audio + haptic cue to reduce vestibular surprise.
- Treat WAI XAUR as the requirements floor, not a nice-to-have — it covers cases vendor docs miss.

## AI-agent gotchas
- Agents conflate VR (occluded) and AR (passthrough) — force the agent to name the immersion level explicitly before designing.
- LLMs propose smooth locomotion as the "modern" default and forget teleport — pin teleport-as-default in the prompt.
- Comfort claims like "reduces nausea by 30%" are unsupported; require citation or remove.
- Agents skip seated-mode coverage for room-scale designs — explicit "wheelchair user reaches all controls seated" check.
- Spatial-audio captions are commonly omitted; require a captions story for every voiced/audio-cued event.
- Human-in-loop checkpoints: motion-sensitive tester pass, accessibility partner review, perf-budget sign-off (90 FPS Quest 3, 90 FPS Vision Pro, 60 FPS for AR phone).

## References
- Meta XR Best Practices — https://developer.oculus.com/resources/bp-overview/
- Apple HIG: Designing for visionOS — https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos
- W3C XR Accessibility User Requirements (XAUR) — https://www.w3.org/TR/xaur/
- Unity XR Interaction Toolkit — https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest
- Jerald, *The VR Book: Human-Centered Design for Virtual Reality* (Morgan & Claypool)
- Bowman et al., *3D User Interfaces: Theory and Practice* (Addison-Wesley, 2nd ed.)
