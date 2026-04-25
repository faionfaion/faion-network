# Agent Integration — Spatial Accessibility

## When to use
- Designing or shipping for Apple Vision Pro, Meta Quest, HoloLens, Magic Leap, Android XR, or WebXR.
- Adding accessibility features to existing XR app pre-release (motion sickness, seated mode, captions, screen reader).
- Auditing immersive product against W3C XR Accessibility User Requirements (XAUR).
- Enterprise XR (training, remote-assist, digital twins) where ADA / EAA / Section 508 may apply.
- Adding alternative input modalities (gaze + voice + controller) to an existing single-modality XR.

## When NOT to use
- 2D web/mobile a11y — use `a11y-testing` and WCAG 2.2 AA. WCAG only partially covers XR.
- Game-only experiences where motion is core gameplay — apply selectively (menus, comfort settings).
- Internal R&D prototypes never seen by users.
- Where the platform's built-in a11y settings are sufficient and product adds no friction.

## Where it fails / limitations
- WCAG 2.2 doesn't fully cover spatial — XAUR is a Working Draft, not normative; many recommendations are still emerging.
- Screen reader support in XR is fragmented: VoiceOver on visionOS works for native UI but not all WebXR or Unity content.
- Eye-tracking dwell selection requires hardware (Vision Pro yes, Quest 2 no, Quest Pro/3 limited).
- Voice control quality drops in noisy environments and for diverse accents (see `vui-accessibility-inclusivity`).
- Spatial audio + haptics specs vary per platform — no single "alt text" for 3D objects yet.
- Real testing requires diverse user panels with XR experience; rare and expensive to recruit.

## Agentic workflow
Agents help with: a11y settings menu generation, captions placement logic, comfort-setting presets, voice-command vocabulary expansion, content audit against XAUR checklist, alt-text/object-description generation for visible 3D objects. Agents cannot: validate motion-sickness comfort, assess haptic feedback strength, run real-user testing. Pipeline: scene-graph audit (find interactive objects without alt-description, missing voice commands, no seated-mode equivalent) → settings-menu generator → human XR tester validates per device.

### Recommended subagents
- `faion-sdd-executor-agent` — track each XAUR criterion as a task; require platform-specific evidence (visionOS, Quest, HoloLens).
- Scene-audit subagent — given Unity/Unreal/visionOS scene description, list interactive entities and verify each has voice + gaze + controller path.
- Object-description generator — given object metadata (type, position, label) emit screen-reader announcement and 3D caption text.
- See also: `vui-accessibility-inclusivity`, `vr-design-patterns`, `ar-design-patterns`, `immersive-design-principles`.

### Prompt pattern
```
You are an XR accessibility auditor. For each interactive object in this
scene manifest, verify:
  1) Has voice-command alias.
  2) Has gaze-dwell support OR explicit non-supported reason.
  3) Has controller-button mapping.
  4) Has accessible-description (string ≤80 chars).
  5) Comfort: works from seated position (no overhead/floor reach).
Output a table with PASS/FAIL per object + which XAUR section.
```

```
Generate seated-mode preset values for {{platform}}:
- Player rig height offset.
- UI canvas distance and elevation.
- Reach-zone bounds.
- Locomotion: enable teleport-only, disable smooth.
- Snap-turn angle (default 30°, min 15°, max 90°).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity Accessibility Plugin (UAP) | Screen reader + a11y for Unity XR | https://www.metalpopgames.com/assetstore/ |
| Unreal Engine Accessibility API | Screen reader, scaling, color-blind | https://docs.unrealengine.com/5.0/en-US/accessibility-in-unreal-engine/ |
| visionOS Accessibility (VoiceOver, Voice Control, Dwell, Eye Tracking) | Apple a11y APIs | https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS |
| Meta Quest Accessibility SDK / a11y settings | Subtitles, color filters, comfort | https://developer.oculus.com/resources/accessibility-design/ |
| Microsoft Mixed Reality Accessibility | HoloLens guidance | https://learn.microsoft.com/en-us/windows/mixed-reality/design/accessibility |
| WebXR Device API + ARIA | Browser-side XR a11y | https://www.w3.org/TR/xaur/ |
| `xr-accessibility-checker` (community) | Static scene audit | https://github.com/xraccess/checklist |
| Whisper / Vosk | Auto-caption pipelines for spatial audio | https://github.com/openai/whisper |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| XR Access (consortium) | OSS resources | n/a | Standards, advocacy, testing pool. |
| Equal Entry | consultancy | manual | XR a11y audits + tester recruitment. |
| Fable | SaaS | human-in-loop | Some testers familiar with XR; recruit specifically. |
| Speechly / Microsoft Speech | SaaS | API | Voice-command grammar + ASR for XR. |
| AssemblyAI / Deepgram | SaaS | API | Real-time captioning of in-world speech. |
| Apple Live Captions (visionOS 2+) | OS feature | n/a | Real-time captions for any audio. |
| Meta Live Captions (Horizon OS) | OS feature | n/a | Subtitles built into headset. |
| ARKit / ARCore semantic understanding | SDK | API | Use for object descriptions + obstacle warnings. |

## Templates & scripts
See README "Accessibility Standards for XR" + checklist. Inline scene-audit example (Unity-like JSON manifest):

```python
#!/usr/bin/env python3
# audit_xr_scene.py manifest.json
import json, sys
required = ["voice_alias", "gaze_supported", "controller_button",
            "description", "seated_compatible"]
m = json.load(open(sys.argv[1]))
fails = []
for obj in m.get("interactables", []):
    missing = [k for k in required if not obj.get(k)]
    if missing:
        fails.append({"id": obj["id"], "missing": missing})
print(json.dumps({"total": len(m.get("interactables", [])),
                  "failed": len(fails), "details": fails}, indent=2))
sys.exit(1 if fails else 0)
```

## Best practices
- Provide ALL inputs simultaneously (gaze + voice + controller + hand) — do not require user to switch modality mid-task.
- Default to seated mode and teleport-only locomotion; promote standing/smooth as opt-ins.
- 3D captions should follow the user (face camera), include speaker direction indicator, sit at constant ~1.5m distance.
- For blind users, attach spatial-audio beacons to landmarks (entrance, exit, key NPCs) with distinct timbres.
- Use vignette during locomotion; expose user-adjustable intensity slider.
- Limit head-tracking interactions (nod/shake) — neck strain risk; always offer voice/controller alternative.
- Align with platform a11y APIs first (visionOS Voice Control, Quest captions); build custom only when needed.
- Test with at least 3 user groups: wheelchair user (seated mode), low-vision user (UI scale, contrast), motion-sensitive user (comfort settings).

## AI-agent gotchas
- LLM-generated 3D-object descriptions hallucinate visual details; clamp to known metadata only or feed vision-model output explicitly.
- Voice command grammars produced by an agent often miss accent variants — see `vui-accessibility-inclusivity`; require diverse voice testing.
- Auto-generated captions from spatial audio drop directional info; the agent must add "[behind-left]" / "[in front]" tags from scene metadata, not from audio alone.
- Agent loops that "fix XR a11y" can introduce flicker/strobe by adding focus highlights — must respect 3-flashes-per-second rule.
- Watch for FOV bugs: putting captions in default visionOS 60° optical center may not reach Quest's wider FOV; agent must adjust per platform.
- Seated-mode preset values from one platform DON'T transfer; agent must keep per-platform tables (Vision Pro vs. Quest 3 vs. HoloLens).
- Don't let agent recommend "remove all motion" by default — some vestibular-OK users prefer smooth locomotion. Always opt-out, not forced.
- Latency requirements differ: voice-command response must feel <500 ms; agent's cloud LLM call can violate that — prefer on-device ASR.

## References
- W3C XR Accessibility User Requirements (XAUR) — https://www.w3.org/TR/xaur/
- Meta accessible VR design — https://developer.oculus.com/resources/accessibility-design/
- Apple visionOS accessibility — https://developer.apple.com/design/human-interface-guidelines/accessibility#visionOS
- Microsoft mixed reality accessibility — https://learn.microsoft.com/en-us/windows/mixed-reality/design/accessibility
- XR Access (consortium) — https://xraccess.org
- Game Accessibility Guidelines — https://gameaccessibilityguidelines.com (relevant for VR games)
- Equal Entry XR research — https://equalentry.com
