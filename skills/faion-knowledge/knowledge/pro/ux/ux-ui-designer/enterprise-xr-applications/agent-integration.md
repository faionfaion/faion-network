# Agent Integration — Enterprise XR Applications

## When to use
- Designing training simulations for high-risk procedures (manufacturing, healthcare, energy).
- Building remote-assistance overlays where an expert guides a field tech.
- Visualizing digital twins for plants, facilities, or large equipment fleets.
- Adding 3D analytics dashboards for portfolios that exceed 2D screen real estate.
- Running design-review or virtual-walkthrough sessions for distributed teams.

## When NOT to use
- Consumer-facing one-off experiences (different design constraints, weaker ROI case).
- Tasks that 2D dashboards already solve well — XR adds friction without payoff.
- Audiences with mixed accessibility needs that XR currently underserves (vestibular issues, low vision).
- Pre-validation of headset penetration in the target audience: don't ship XR-only flows to a workforce with <50% headset coverage.

## Where it fails / limitations
- Long-session comfort: most users tolerate ≤30 min before fatigue; training must chunk accordingly.
- Enterprise IT integration is the killer: SSO, MDM, content-management for headsets is immature.
- ROI is hard to attribute — training XR competes with video + LMS that already report metrics.
- Accessibility (WCAG, ADA) lags 2D apps; legal exposure on internal-use only.
- Headset OS upgrades break content; lifecycle management is non-trivial.

## Agentic workflow
Use Claude subagents to draft training scripts, step graphs, and remote-assist scenarios from SOPs and incident reports. The agent emits a step-graph spec (current step → action → feedback → branch) which a Unity/Unreal designer implements. A second agent loop checks each scenario against safety procedures and accessibility heuristics before sign-off.

### Recommended subagents
- `faion-ux-researcher-agent` — interviews field staff to derive training scenarios.
- `faion-usability-agent` — runs heuristic eval against XR comfort + accessibility patterns.
- General Claude subagent — converts SOP PDFs into step-graphs (current → next → feedback → retry).

### Prompt pattern
```
Convert this SOP <pdf-text> into an XR training step-graph.
Each node: id, instructional text (≤15 words), trigger
condition, success feedback, failure feedback, retry policy.
Flag any step requiring fine motor skill or hazardous proximity.
```

```
Audit this XR scenario for enterprise constraints: session length,
SSO touchpoints, data-classification of any captured media,
WCAG 2.2 conformance gaps. Output PASS/FAIL per constraint with
evidence.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity CLI (`Unity -batchmode`) | Headless XR builds | https://docs.unity3d.com/Manual/CommandLineArguments.html |
| Unreal `UnrealEditor-Cmd` | Headless UE5 builds | https://docs.unrealengine.com/ |
| `adb` | Sideload + log Quest builds | Android SDK Platform-Tools |
| `idevicedebug` | visionOS device logs | `brew install libimobiledevice` |
| OpenXR conformance tool | Validate runtime behavior | https://www.khronos.org/openxr/ |
| Mozilla Hubs CLI | Self-hosted virtual rooms | https://hubs.mozilla.com/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Mesh | SaaS | Limited API | Enterprise meetings, identity-integrated |
| TeamViewer Frontline | SaaS | API | Industrial AR remote assistance |
| PTC Vuforia | SaaS | SDK | Marker / model-based AR for industry |
| NVIDIA Omniverse | SaaS | API | Digital twin pipeline |
| Strivr | SaaS | API | Enterprise immersive training |
| ARway | SaaS | API | Indoor AR navigation |
| Meta Quest for Business | SaaS | MDM API | Headset fleet management |
| Apple Vision Pro MDM | SaaS | API | Enterprise device + content rollout |

## Templates & scripts
See `templates.md` for training scenario, remote-assist flow, and KPI dashboard. Inline step-graph schema:

```yaml
# step-graph.yaml — minimum schema for an XR training step.
steps:
  - id: don-ppe
    instruction: "Put on safety gloves and goggles"
    trigger: "user gaze on PPE shelf"
    success_feedback: "haptic + green chime"
    failure_feedback: "voice prompt: try again"
    retry_max: 3
    next: power-off
    accessibility:
      caption: true
      colorblind_safe_indicator: true
```

## Best practices
- Chunk training to ≤25 min sessions; longer = comfort + retention drops.
- Always provide a 2D fallback path; XR fleets break, content must keep training working.
- Capture every interaction event server-side for ROI metrics (completion %, error rate, time-to-competence).
- Co-design with safety/compliance teams from day 1; their sign-off is the gating criterion.
- Default to seated experiences for office work; room-scale for training only.
- Privacy: hand/eye tracking data is sensitive — define retention + access policy before pilot.

## AI-agent gotchas
- LLMs hallucinate XR APIs frequently (XR SDKs change quickly). Verify every API call against current docs.
- Agents underestimate motion-sickness risk; force a "comfort review" pass on every scenario.
- Generated scenarios skip the "retry/failure" branch — prompt explicitly for both paths.
- Image/3D-asset generation is not yet production-grade for XR; use only for ideation/storyboards.
- SSO/MDM details vary per-vendor; agents conflate Quest vs. Vision Pro management workflows. Keep them separate.
- Accessibility checks are easy to skip; bake them into the agent's required output schema.

## References
- Apple visionOS HIG — https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos.
- Meta Quest for Business — https://www.meta.com/work/quest-for-business/.
- Khronos OpenXR Specification.
- Microsoft Mesh / HoloLens guidance — https://learn.microsoft.com/mesh.
- "Make It So: Interaction Design Lessons from Science Fiction" — Shedroff & Noessel.
- IDC Spatial Computing Market Reports (annual).
