# Agent Integration — Spatial Accessibility

## When to use
- Designing AR/VR/MR experiences on Vision Pro, Quest, PS VR2, HoloLens, or WebXR.
- Adapting an existing flat UI for a spatial platform — need seated mode, gaze fallback, motion-comfort settings.
- Submitting an app to App Store / Meta Horizon Store — accessibility is a review criterion (Apple HIG, Meta VRC.PC.UX guidelines).
- Designing for enterprise XR (industrial training, medical) where injury risk is non-zero and a11y becomes safety.

## When NOT to use
- 2D mobile/desktop apps — use standard WCAG 2.2 / mobile a11y; spatial-specific tradeoffs do not apply.
- Pure passthrough video apps with no UI overlay — most spatial-a11y items reduce to standard video accessibility (captions, contrast).
- Throwaway VR demos for a single internal user — full spatial-a11y program is overkill before validation.

## Where it fails / limitations
- WCAG does not yet cover spatial UI completely; W3C XAUR (XR Accessibility User Requirements) is informative, not normative — checklists must be authored by hand.
- Multimodal alternatives (gaze, voice, controller, hand) multiply test surface; coverage on real assistive hardware is rare.
- Motion-comfort is highly individual; "vignette + teleport" doesn't fix nausea for everyone.
- Captions in 3D have unsolved placement problems — head-locked is readable but breaks immersion; world-locked is immersive but unreadable in motion.
- Screen readers don't exist for spatial yet; VoiceOver on visionOS is partial. Hand-authored audio descriptions are still required.

## Agentic workflow
Use one subagent to map every interaction to the alternative-input matrix (gaze, voice, hand, controller, switch), a second to audit comfort settings and seated-mode coverage, and a third to generate audio descriptions and caption placement specs. Always validate on hardware with users — synthetic testing misses motion sickness and field-of-view blind spots.

### Recommended subagents
- `spatial-a11y-auditor` — checks each interaction has at least two input modalities and a non-spatial fallback.
- `motion-comfort-checker` — flags forced-camera moves, fast translations, missing vignette/teleport options.
- `caption-placement-planner` — recommends head-locked vs object-locked vs subtitle-track per scene.
- `audio-description-writer` — drafts AD scripts for cinematic and interactive XR moments.

### Prompt pattern
```
For each spatial interaction, return JSON:
{ name, primary_input, alternatives[], requires_motion: bool, comfort_options[], seated_compatible: bool, blockers[] }
Required alternatives: at least one of {gaze+dwell, voice, single-hand, controller, switch}.
If requires_motion, comfort_options must include vignette, teleport, snap-turn, FOV-reduce, or seated.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `Unity XR Interaction Toolkit` | Built-in alt-input + comfort modules | https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest |
| `OpenXR Validation Layers` | Validate XR runtime calls | https://www.khronos.org/openxr/ |
| `Reality Composer Pro` | Vision Pro scene tooling, accessibility traits | Xcode 15+ |
| `WebXR Emulator` (Chrome ext) | Quick desktop XR testing | https://github.com/MozillaReality/WebXR-emulator-extension |
| `axe DevTools for XR` (in beta) | Heuristic XR a11y scanning | https://www.deque.com/axe/ |
| `OVR Metrics Tool` | Comfort/perf telemetry on Quest | sideloaded APK |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apple Accessibility (visionOS) | Platform | Yes (APIs) | VoiceOver, AssistiveTouch, Pointer Control, Eye-only nav. |
| Meta Quest Accessibility | Platform | Partial | Color filters, reduced motion, hand-tracking calibration. |
| Microsoft Mesh / HoloLens a11y | Platform | Partial | Eye/voice fallback, inclusive design toolkit. |
| Equal Entry | Consultancy | N/A | XR a11y audits — useful for human-loop validation. |
| XR Access Initiative | Community | N/A | Standards, research, and tester pool. |

## Templates & scripts
Inline alt-input matrix generator (≤30 lines).

```ts
// alt-input-matrix.ts
type Modality = "gaze" | "voice" | "hand" | "controller" | "switch";
type Interaction = { name: string; primary: Modality; supports: Modality[] };

const REQUIRED_PER_INTERACTION = 2;

export function audit(interactions: Interaction[]) {
  const gaps: { name: string; missing: number }[] = [];
  for (const i of interactions) {
    const total = new Set([i.primary, ...i.supports]).size;
    if (total < REQUIRED_PER_INTERACTION) {
      gaps.push({ name: i.name, missing: REQUIRED_PER_INTERACTION - total });
    }
  }
  return { passing: interactions.length - gaps.length, gaps };
}
```

## Best practices
- Default seated-mode parity: every interaction must work seated; if not, document an explicit alternative.
- Provide both vignette and teleport for any locomotion; let the user pick — no single solution fixes nausea universally.
- Treat hand size, dominance, and tremor as first-class input variables, not edge cases — interaction zones must scale.
- Caption styles per platform: head-locked subtitles default ON; world-locked optional with size/contrast slider.
- Recruit testers with motion sensitivity, low vision, and motor differences early — comfort tuning that "feels fine" to designers fails real users.

## AI-agent gotchas
- LLMs default to controller-only assumptions; force them to enumerate alternatives explicitly.
- Models conflate VR (fully immersive) and AR (passthrough overlay); accessibility tradeoffs differ — AR has less motion sickness but more contrast issues against real-world backgrounds.
- Caption placement reasoning is poor in current LLMs; agents recommend "head-locked" universally — use heuristics + human review.
- Audio description scripts from LLMs over-narrate; trim aggressively and review with blind testers.
- Synthetic XR a11y testing tools are immature; do not declare compliance without hardware testing with real assistive users.
- Human checkpoint: device testing with 5+ users including at least one each of low-vision, motor-impaired, and motion-sensitive. No agent can substitute.

## References
- W3C XAUR (XR Accessibility User Requirements): https://www.w3.org/TR/xaur/
- Apple HIG visionOS accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Meta VRC.PC.UX accessibility checks: https://developers.meta.com/horizon/resources/vrcs/
- Microsoft Inclusive Design for XR: https://inclusive.microsoft.design/
- XR Access Initiative: https://xraccess.org/
- Equal Entry XR a11y blog: https://equalentry.com/
