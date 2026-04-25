# Agent Integration — Immersive Design Principles

## When to use
- Designing for AR/VR/MR headsets (Vision Pro, Quest 3, Pico 4, HoloLens 2) where immersion level must be deliberate.
- Mixed-reality enterprise tools (training, remote assistance, surgery planning) where over-immersion is a safety risk.
- Spatial gaming and entertainment where immersion-comfort tradeoff drives session length.
- Designing transitions between passthrough and fully-immersive states (the moment most discomfort happens).

## When NOT to use
- 2D mobile / web flows without spatial component.
- Simple AR effects (face filters, product try-on snippets) — overkill for one-shot interactions.
- Marketing-only "VR demo" projects with no real user-research budget; principles are wasted without testing.

## Where it fails / limitations
- Comfort guidelines are population averages; ~10% of users get sick regardless of "best practice" defaults.
- Hardware drift: principles tuned for Quest 2 fail on Vision Pro (eye-tracking, EyeSight) and vice versa.
- Static documentation can't capture motion-physics nuance; you need in-headset playtests, not figmas.
- "Immersion" is conflated with "presence" in vendor docs — design for presence, not visual fidelity.
- Long sessions (>20 min) reveal arm fatigue and eye strain that short heuristic reviews miss entirely.

## Agentic workflow
Use agents to draft immersion-level decisions, comfort checklists, and transition state-machines, but verify every motion/locomotion decision in a real headset with at least 3 testers across 30+ minutes. LLMs do not feel motion sickness; they will confidently approve a vection pattern that ships nausea.

### Recommended subagents
- `faion-ux-researcher-agent` — generates spatial usability test scripts, comfort-rating questionnaires (SSQ, VRSQ).
- `faion-usability-agent` — heuristic walkthrough against Oculus / Apple HIG checklists.

### Prompt pattern
```
You are reviewing an XR scene description for immersion-comfort balance.
Inputs: {scene_summary, locomotion_method, session_length_min, target_device}.
Output JSON: {
  immersion_level: passthrough|blended|immersive|portal,
  comfort_risks: [{risk, severity, mitigation}],
  transition_smoothness: 0-5,
  ssq_red_flags: [...]
}
Cite the Oculus VRC or Apple visionOS HIG section per finding. No invented citations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `oculus-cli` (ovrplatformutil) | Build/upload Quest builds, fetch perf metrics | https://developer.oculus.com/downloads/package/oculus-platform-utility/ |
| `xrgears` / `OpenXR` validation layers | Runtime conformance checks | https://github.com/KhronosGroup/OpenXR-SDK |
| `realitytool` (Xcode) | Validate visionOS scene assets, USDZ packaging | Xcode 15+ |
| `adb logcat -s VrApi,XrApi` | Pull comfort-related runtime warnings on Quest | Android SDK |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Horizon OS dashboard | SaaS | Limited | Comfort/perf dashboards behind auth; manual export. |
| Apple App Store Connect | SaaS | Limited | visionOS analytics; no public agent API. |
| Unity Cloud Build | SaaS | Yes | CLI + REST; automate immersion-test build pipelines. |
| Unreal Horde | OSS | Yes | Self-host CI/CD for high-fidelity XR. |
| ShapesXR | SaaS | Partial | Collaborative spatial review; export to Unity. |
| Reality Composer Pro | macOS app | No | Manual workflow for visionOS USDZ scenes. |

## Templates & scripts
See `templates.md` for immersion-level decision matrix. Inline checklist generator:

```bash
#!/usr/bin/env bash
# gen-comfort-checklist.sh — emit per-scene comfort review file
SCENE="${1:?scene name}"
mkdir -p "review/$SCENE"
cat > "review/$SCENE/comfort.md" <<MD
# $SCENE — Comfort Review
- [ ] Ground plane present and stable
- [ ] Horizon line within 5° of expected
- [ ] No head-locked UI elements
- [ ] Locomotion method declared: ____
- [ ] Vection events <3s, with comfort vignette
- [ ] Frame rate ≥72 Hz (Quest), ≥90 Hz (Vision Pro)
- [ ] Transition fade ≥0.2s on immersion changes
- [ ] Arm-rest poses for sessions >10 min
- [ ] Subtitle/voice option present
- [ ] SSQ pre/post measurement plan
MD
```

## Best practices
- Pick one immersion level per scene, transition deliberately. Mixed signals (head-locked + world-locked together) cause disorientation.
- Default to passthrough-first for productivity apps; opt into full immersion only when the task demands it.
- Comfort vignette during locomotion (snap turn or smooth) is non-negotiable below 90 Hz.
- Treat the first 10 seconds of any scene as orientation budget — no required interaction, no narrative-critical content.
- Provide seated-mode for any experience >5 min; arm fatigue is the silent churn killer.
- Test with people who wear glasses, are over 50, and have never used an HMD — your team's tolerance is unrepresentative.

## AI-agent gotchas
- LLMs default to "more immersive = better" framing. Pin the prompt to the four immersion levels and force a tradeoff justification.
- Motion physics descriptions sound plausible in text and feel terrible in headset. Never ship without playtest.
- Inclusive-design checks for spatial UI are weak in current models; cross-reference `spatial-accessibility` methodology explicitly.
- Vendor HIGs (Apple visionOS vs. Meta vs. Pico) contradict each other on hand-tracking gestures; agents will average and produce nonsense — pick one platform per prompt.
- Latency budgets (motion-to-photon) cannot be verified by LLM; they need on-device profiling. Don't accept agent claims like "this should run at 90 Hz."

## References
- Apple, *Human Interface Guidelines — visionOS / Spatial Design*. https://developer.apple.com/design/human-interface-guidelines/spatial-layout
- Meta, *Oculus VRCs (Virtual Reality Checks) and Comfort Best Practices*. https://developer.oculus.com/resources/bp-vrc-quest/
- Jerald, *The VR Book: Human-Centered Design for Virtual Reality* (2015).
- LaViola et al., *3D User Interfaces: Theory and Practice* (2nd ed., 2017).
- Kennedy et al., *Simulator Sickness Questionnaire* (1993) — still the standard SSQ instrument.
