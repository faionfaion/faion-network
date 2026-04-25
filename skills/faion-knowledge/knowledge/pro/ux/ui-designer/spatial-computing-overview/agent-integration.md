# Agent Integration — Spatial Computing Overview

## When to use
- Early scoping conversations: deciding whether a project belongs in 2D, AR, VR, or MR.
- Onboarding designers/engineers new to XR — start here for vocabulary and platform map.
- Strategy decks for stakeholders explaining 2026 spatial-computing landscape.
- Choosing between Vision Pro / Quest / HoloLens / Android XR / Magic Leap for a use case.
- Ground-truth orientation before going deeper into `spatial-interaction-patterns`, `vr-design-patterns`, `ar-design-patterns`, `immersive-design-principles`.

## When NOT to use
- Building a real product — this README is intentionally a one-page overview, not a design spec.
- Detailed interaction or comfort design — use the dedicated methodologies.
- Web/mobile-only product — irrelevant.
- Already established XR product team — likely too high-level.

## Where it fails / limitations
- Overview-only: ≈40 lines, no implementation detail.
- Market figures (87% growth) age fast; verify before quoting.
- Platform list is incomplete — Pico, Lynx, Varjo (industrial), Bigscreen Beyond, Samsung's headset all relevant in 2026.
- Doesn't cover WebXR, smart glasses (Ray-Ban Meta, Halliday, Brilliant Labs Frame), or mobile AR.
- "Spatial computing" is contested terminology — Apple's framing vs. Meta's "MR" vs. Microsoft's "MR" differ.

## Agentic workflow
Use this overview to seed a scoping conversation, then route to specific methodologies. Agents help with: platform-comparison matrix, market-context-2026 fact-check, AR-vs-VR-vs-MR decision tree from a use case, deck/document drafts. Agents do NOT replace: hands-on device evaluation, user interviews, ergonomic testing.

### Recommended subagents
- `faion-sdd-executor-agent` — translate scoping decisions into SDD spec/design tasks per platform target.
- Platform-decision subagent — given use case + constraints (mobile/seated/social/industrial), recommend AR / VR / MR + specific device.
- Market-fact subagent — when README cites figures, verify against current sources and replace stale data; flag when sources older than 6 months.
- See also: `enterprise-xr-applications`, `spatial-interaction-patterns`, `spatial-design-tools`, `vr-design-patterns`, `ar-design-patterns`.

### Prompt pattern
```
Given this use case: "{{description}}", recommend AR vs VR vs MR plus a
device shortlist (Vision Pro / Quest 3 / Quest 3S / HoloLens / Magic Leap 2 /
Android XR / WebXR / Pico). For each, give one-sentence rationale and one
constraint that could disqualify. End with a single primary recommendation
and a fallback.
```

```
Build a 2026 spatial-computing landscape brief (≤500 words):
- AR / VR / MR definitions with examples.
- Top 5 platforms with strengths and one weakness each.
- Two trends to watch (e.g., smart glasses, generative content).
- Cite at least three sources from the last 6 months.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity XR Interaction Toolkit | Cross-platform XR | https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit |
| Unreal OpenXR | Cross-platform | https://docs.unrealengine.com/5.0/en-US/openxr-in-unreal-engine/ |
| MRTK3 | Microsoft mixed-reality toolkit | https://github.com/MixedRealityToolkit/MixedRealityToolkit-Unity |
| visionOS SDK / RealityKit / Reality Composer Pro | Vision Pro native | https://developer.apple.com/visionos/ |
| Meta XR SDK + Presence Platform | Quest features | https://developer.oculus.com |
| ARKit / RealityKit (iOS) | Mobile AR | https://developer.apple.com/augmented-reality/ |
| ARCore | Android AR | https://developers.google.com/ar |
| WebXR | Browser XR | https://immersive-web.github.io/webxr/ |
| Babylon.js / Three.js + WebXR | OSS web XR | https://www.babylonjs.com / https://threejs.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apple App Store / Reality Composer | platform | manual | Vision Pro distribution. |
| Meta Quest Store / App Lab / Quest for Business | platform | manual + API | Consumer + enterprise channels. |
| Microsoft Store on HoloLens / Intune | platform | API | Enterprise distribution. |
| Niantic Lightship | SaaS | SDK | Real-world AR (geo, semantic). |
| 8thWall (Niantic) | SaaS | SDK | Web AR, no-app-required. |
| Snap Lens Studio + Spectacles | platform | SDK | AR glasses (Spectacles 5). |
| Sketchfab / Polycam / Luma AI | SaaS | API | 3D asset capture and library. |
| NVIDIA Omniverse / USD | SaaS | API | Industrial 3D collaboration. |

## Templates & scripts
README itself is the template. Inline platform-decision matrix:

```markdown
| Platform | Type | Best for | Worst for | Key SDK |
|----------|------|----------|-----------|---------|
| Apple Vision Pro | Spatial / passthrough MR | Premium consumer, prosumer apps, productivity | High-volume consumer scale | visionOS / RealityKit |
| Meta Quest 3 / 3S | VR + passthrough MR | Consumer adoption, gaming, social | Outdoor, transparent AR | Meta XR SDK |
| Microsoft HoloLens 2 / 3 | Optical see-through MR | Industrial, hands-free work | Consumer, gaming | MRTK3 |
| Magic Leap 2 | Optical see-through MR | Healthcare, defense, industrial | Consumer | Magic Leap SDK |
| Android XR (Samsung headset) | Spatial MR | Mobile-ecosystem integration | Established install base | Android XR SDK |
| WebXR | Browser | Pilots, retail try-on, no-install AR | High-fidelity / persistent XR | WebXR + Three/Babylon |
| Ray-Ban Meta / Halliday | Smart glasses | Hands-free capture, voice | Rich UI, immersion | Meta Wearable / partner SDK |
```

## Best practices
- Start every spatial project with this overview, then immediately go deeper — do not stay at this level for design decisions.
- Pick OpenXR-aligned tooling for forward portability across vendors.
- Validate against actual hardware early — emulators lie about ergonomics, FOV, and tracking quality.
- Match interaction model to platform strengths: hand-eye on Vision Pro, controllers + hands on Quest, hands + voice on HoloLens.
- Cover accessibility (`spatial-accessibility`) from the start — retrofitting is expensive in XR.
- Plan content distribution (App Store, Quest Store, Intune) and revenue/licensing model in scoping, not post-build.
- Beware "spatial computing" hype-claims; ground decisions in measurable user value.

## AI-agent gotchas
- Stale facts: market growth rates, install bases, and platform roadmaps change quarterly. Agents quoting README numbers without verification will mislead stakeholders.
- LLM tends to over-recommend Vision Pro for premium use cases; balance with cost and install-base realities (Vision Pro install base remains small in 2026).
- Confusion between "MR" terms — Apple "passthrough", Meta "MR", Microsoft "MR" are not equivalent. Agent must specify which.
- Agents may suggest WebXR as a universal answer; acknowledge platform-specific limits (no Vision Pro WebXR full feature parity, no advanced hand tracking on iOS Safari).
- Don't let agent design specific interactions from this overview alone — it lacks the depth.
- Agents may forget about smart glasses, treating "spatial" = headsets only; Ray-Ban Meta and similar need consideration in 2026.
- Treat as a router: when an agent reaches a decision point, dispatch to the deeper methodology rather than answering inline.
- Agents may underweight ergonomics and battery — flag both as scoping checks.

## References
- Apple visionOS HIG — https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos
- Meta Oculus developer center — https://developer.oculus.com/
- Android XR developer site — https://developers.google.com/ar (and https://developers.google.com/xr in 2026)
- Microsoft Mixed Reality docs — https://learn.microsoft.com/en-us/windows/mixed-reality/
- Magic Leap developer — https://developer.magicleap.cloud
- IDC AR/VR tracker — https://www.idc.com/getdoc.jsp?containerId=spatial-computing
- Niantic Lightship — https://lightship.dev
- Snap Lens Studio — https://ar.snap.com/lens-studio
