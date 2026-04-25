# Agent Integration — VR Design Patterns

## When to use
- Designing fully-immersive VR experiences (Quest 2/3/Pro, PSVR2, Valve Index, PICO 4, Vision Pro full-immersion mode).
- Choosing locomotion (teleport, smooth, room-scale, vehicle, arm-swing) and UI placement strategy.
- Implementing comfort settings: vignette, snap turn, FOV cap, seated mode, height calibration.
- Auditing an existing VR title for accessibility (vision, hearing, mobility, cognitive) and motion-sickness risk.

## When NOT to use
- AR / passthrough / MR — use `ar-design-patterns` and `immersive-design-principles` instead.
- 360° video on a phone in a Cardboard-style viewer — those have constrained interaction; this skill assumes 6DoF.
- Mixed-reality productivity (virtual monitors with passthrough) — that is `immersive-design-principles` blended-mode territory.
- WebXR mobile sessions where 90 FPS is unreachable — separate perf strategy required.

## Where it fails / limitations
- Patterns assume 90 FPS @ <20 ms motion-to-photon — mobile/standalone may not hit that and recommendations break.
- "Comfort" framings are population-level; ~5–10 % of users get sick on rated-comfortable experiences.
- Hand tracking guidance lags devices — Quest 3 hand tracking is more capable than Quest 2 and patterns conflate them.
- Screen-reader story is still experimental in VR — recommendations here are aspirational.
- Multi-user social VR adds harassment + safety patterns this methodology does not cover.

## Agentic workflow
Treat this as a structured-review skill: agents convert a design doc into a checklist of locomotion options, UI placement, comfort settings, and accessibility coverage; a critic agent flags gaps and motion-sickness risk; a human XR designer + at least one wheelchair-using or motion-sensitive tester gate sign-off. Implementation-level work (XR Interaction Toolkit, Unreal VR template, OpenXR) is delegated to engine-specific subagents — this skill stays at the design layer.

### Recommended subagents
- `faion-ux-ui-designer-agent` — UI panel layout (1.5–3 m, eye level, curved), diegetic vs. non-diegetic split.
- `faion-accessibility-specialist-agent` — disability-coverage matrix, captions, voice command parity.
- `faion-multimodal-ai-agent` — spatial audio, haptic + audio sync, audio descriptions.
- Engine-implementation agent (Unity XRI, Unreal VR Template, Godot XR) — verify code matches design.

### Prompt pattern
```
Role: VR design auditor.
Input: experience description + target devices.
For each axis, return {status, evidence, fix}:
  locomotion options ≥2 (must include teleport and seated)
  turning options (snap default; smooth optional with speed cap)
  UI placement (no head-lock; 1.5–3 m; eye level; ≥14 pt text)
  grounding (floor + horizon visible)
  comfort (vignette, FOV cap, reduce motion, reduce particles)
  accessibility (captions, color blind, voice, hand-free)
  performance floor (90 FPS, <20 ms latency)
```

```
Role: locomotion-options generator.
Given experience type <exploration | combat | seated cockpit | social>,
output prioritized locomotion menu with comfort defaults and which to disable
on lower-end hardware. Include rationale and seated-mode parity.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity XR Interaction Toolkit (XRI) | Locomotion providers, snap turn, teleport, comfort vignette | UPM `com.unity.xr.interaction.toolkit` |
| Unreal VR Template | Teleport, snap turn, hand IK reference | Built into Unreal 5.x |
| OpenXR Toolkit | Per-device XR runtime config | https://github.com/mbucchia/OpenXR-Toolkit |
| OVRMetricsTool | Quest perf overlay (FPS, GPU/CPU, latency) | Meta Developer Hub sideload |
| RenderDoc | Frame capture for VR perf analysis | https://renderdoc.org |
| Substance / Blender | Asset prep with proper scale and pivot | https://www.blender.org |
| `xr-accessibility-checklist` (W3C XAUR) | Disability-coverage requirements list | https://www.w3.org/TR/xaur/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Quest Developer Hub | SaaS + CLI | Yes — `adb` + `ovrgpuprofiler` | Required for Quest deploy + perf |
| Steam VR / OpenVR | OSS-ish | Yes — `vrcmd`/REST | Index, Vive, multi-vendor PCVR |
| Apple App Store Connect | SaaS | Partial | Vision Pro full-immersion approval path |
| PICO Developer Platform | SaaS | Limited | China-heavy; required for PICO 4/Neo |
| Sony PSVR2 Devkit | Closed | No | NDA-only |
| Resonai / Owlchemy patterns lib | OSS examples | Yes for code review | Reference comfort patterns |
| Wwise / FMOD | Licensed audio | Yes — APIs | Spatial audio + audio occlusion |
| AccessibleVR (Microsoft Game Stack) | Docs | Yes — patterns reference | Disability-coverage examples |

## Templates & scripts
See `templates.md` for locomotion matrix, UI placement diagram, and comfort-settings menu schema. Inline reference for a comfort-defaults JSON the design agent can emit:

```json
{
  "locomotion": {
    "teleport": {"enabled": true, "default": true, "blink_or_dash": "blink"},
    "smooth": {"enabled": true, "default": false, "max_speed_mps": 1.4, "vignette": true},
    "seated": {"enabled": true, "all_content_reachable": true},
    "vehicle": {"enabled": false}
  },
  "turn": {"mode_default": "snap", "snap_step_deg": 30, "smooth_speed_dps": 90},
  "comfort": {"fov_cap_during_motion_deg": 80, "reduce_motion": false, "reduce_particles": false, "screen_shake": false},
  "ui": {"panel_distance_m": 2.0, "panel_height_eye_level": true, "min_text_pt": 16, "head_lock": false},
  "accessibility": {"captions": true, "voice_commands": true, "hand_tracking": true, "high_contrast": false, "color_blind_palette": "default"},
  "performance": {"target_fps": 90, "min_fps": 90, "max_motion_to_photon_ms": 20}
}
```

## Best practices
- Default locomotion = teleport + snap turn; smooth options gated behind explicit user opt-in with FOV vignette on.
- Always provide a seated mode that reaches every interaction — wheelchair-user parity, not afterthought.
- Minimum 14–16 pt text in VR (smaller is unreadable even at 4K per eye); test at 2 m viewing distance.
- World-lock or body-lock UI; never head-lock. Diegetic where it makes narrative sense.
- Frame budget is non-negotiable: drop visual fidelity before dropping below 90 FPS.
- Run hardware-IPD calibration step at first launch; a wrong IPD nukes comfort regardless of design.
- Test with first-time VR users — experienced devs underestimate locomotion difficulty.

## AI-agent gotchas
- Agents recommend "smooth locomotion for immersion" as default — pin teleport-as-default in your prompt.
- LLMs forget seated mode in room-scale designs; require explicit seated-parity check on every interaction.
- Generated text sizes default to web/mobile pt — multiply by ~1.5x for VR readability.
- Agents propose head-locked HUDs from gaming experience — explicitly forbid head-lock; require world or body lock.
- Spatial-audio recommendations are often described but not specced — require Wwise/FMOD event names or equivalent.
- Comfort-claim hallucinations ("reduces nausea by X%") — strip unsupported numbers.
- Human-in-loop checkpoints: motion-sensitive tester pass, wheelchair-user parity check, IPD calibration QA, 30-min extended-session test.

## References
- Meta VR Best Practices — https://developer.oculus.com/resources/bp-overview/
- Valve VR Design Guidelines — https://steamcommunity.com/sharedfiles/filedetails/?id=1537149895
- Unity XR Interaction Toolkit — https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest
- W3C XR Accessibility User Requirements (XAUR) — https://www.w3.org/TR/xaur/
- Jerald, *The VR Book* (Morgan & Claypool)
- Microsoft Gaming Accessibility Guidelines — https://gameaccessibilityguidelines.com/
- XBox Accessibility Guidelines (XAGs) — https://learn.microsoft.com/en-us/gaming/accessibility/
