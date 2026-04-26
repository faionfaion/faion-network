# Agent Integration — Enterprise XR Applications

## When to use
- Scoping or designing XR for training, remote-assist, digital twins, design review, or 3D analytics in B2B/industrial contexts.
- Translating consumer-XR design patterns into enterprise constraints (security, deployment, ROI metrics).
- Long-session, multi-user collaboration apps (e.g., manufacturing floor digital twin).
- Selecting platform (HoloLens vs Quest for Business vs Vision Pro Enterprise) based on use-case requirements.
- Drafting XR pilot programs with measurable success criteria.

## When NOT to use
- Consumer-facing XR (games, social) — different KPIs, different platforms; use `vr-design-patterns` and `ar-design-patterns`.
- Quick marketing demos — overkill for short sessions; use 360 video or WebXR teaser.
- Tasks already solved by 2D — adding XR purely for novelty fails the ROI test.
- Mobile-only AR for retail product viz — use ARKit/ARCore web flows, not enterprise stack.

## Where it fails / limitations
- README content is thin (≈40 lines) — this is an overview, not a deep methodology. Treat as scoping checklist.
- Hardware costs and IT-deployment complexity are major blockers; pilots stall at procurement.
- Long-session ergonomics are still hard: 30-60 min sessions cause fatigue on most headsets except newer pancake-lens devices.
- Integration with enterprise SSO, MDM, data systems varies wildly per platform — vendor lock-in risk.
- ROI measurement is subjective for soft outcomes (training retention, design-review quality).
- Accessibility (`spatial-accessibility`) often deferred — must be included from spec.

## Agentic workflow
Agents are useful for: use-case assessment scoring, platform-selection matrices, ROI hypothesis drafting, training-flow scriptwriting, integration-requirement gathering, accessibility checklist application. Agents cannot: validate ergonomics, run user studies, judge real ROI. Pipeline: stakeholder interview notes → agent extracts use-case fit → platform matrix → pilot plan with metrics → handoff to design + integration teams.

### Recommended subagents
- `faion-sdd-executor-agent` — turn each enterprise requirement (security, accessibility, integration) into an SDD task with explicit acceptance criteria.
- Use-case scoring subagent — score candidate XR ideas against the enterprise requirements list and known limitations.
- Training-script subagent — generate step-by-step XR training flows with highlighted current step, branching, completion tracking.
- Platform-matrix subagent — given requirements, output a comparison of HoloLens 2/3, Quest 3 for Business, Vision Pro Enterprise, Magic Leap 2.
- See also: `spatial-computing-overview`, `spatial-accessibility`, `vr-design-patterns`, `ar-design-patterns`, `immersive-design-principles`.

### Prompt pattern
```
Score this XR enterprise idea against:
  1) Long-session comfort feasible?
  2) Integrates with existing tools?
  3) Security/data-protection achievable on chosen device?
  4) Deployment-management story (MDM, content distribution)?
  5) Accessibility coverage plan?
  6) Measurable ROI hypothesis with leading + lagging indicators?
For each, rate 1-5 and justify in 1 sentence. End with a Go/No-Go recommendation.
```

```
Design a training XR flow for {{procedure}}:
- Steps with highlight, voice-over, and visible next-action.
- Failure recovery: retry, hint escalation.
- Completion tracking suitable for LMS export (xAPI / SCORM).
- Accessibility: seated mode, captions, voice-command equivalents.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Unity XR Interaction Toolkit | Cross-platform XR interactions | https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit |
| Unreal OpenXR | Cross-platform XR | https://docs.unrealengine.com/5.0/en-US/openxr-in-unreal-engine/ |
| MRTK3 (Microsoft Mixed Reality Toolkit) | HoloLens-first toolkit, also Quest | https://github.com/MixedRealityToolkit/MixedRealityToolkit-Unity |
| visionOS SDK / RealityKit | Apple Vision Pro native | https://developer.apple.com/visionos/ |
| Meta XR SDK / Presence Platform | Quest features | https://developer.oculus.com/documentation/ |
| Microsoft Intune / Quest for Business | MDM for headset fleet | https://www.meta.com/quest/business/ |
| `xapi-validator` / `scorm-cloud-cli` | LMS-export validation for training | https://rusticisoftware.com |
| WebXR Device API | Browser-based enterprise pilots | https://immersive-web.github.io/webxr/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Mesh | SaaS | API/SDK | Collaborative immersive meetings, M365 integrated. |
| Meta Horizon Workrooms | SaaS | API limited | Quest-only collaboration. |
| Strivr / Mursion | SaaS | manual | Enterprise XR training services. |
| PTC Vuforia Studio + ThingWorx | SaaS | API | Industrial AR with IoT. |
| Unity Industry / Unity Cloud | SaaS | API | Build + deploy enterprise XR apps. |
| ScopeAR / Vuforia Engine | SaaS | API | Remote-assist + work instructions. |
| NVIDIA Omniverse | SaaS | API | Industrial digital twins, USD-based. |
| Apple Vision Pro Enterprise + Mobile Device Management | platform | API | MDM for visionOS in 2026 expanded. |

## Templates & scripts
README is thin; rely on `vr-design-patterns`/`ar-design-patterns` for interaction details. Inline pilot-scoring template:

```markdown
# Enterprise XR Pilot — {{name}}

## Use case
{{1-paragraph description}}

## Success metrics
| Metric | Baseline | Target | Measurement method |
|--------|----------|--------|---------------------|
| Training completion | | | LMS xAPI |
| Time-to-proficiency | | | Pre/post test |
| Error rate on task | | | Observer rubric |
| User comfort (NPS) | | | Post-session survey |

## Platform
- Device: {{HoloLens 3 / Quest 3 for Business / Vision Pro Enterprise / Magic Leap 2}}
- Rationale: {{why}}
- MDM: {{Intune / Quest for Business / ABM+MDM}}

## Integrations
- SSO: {{Entra ID / Okta}}
- LMS: {{Cornerstone / Workday Learning / SuccessFactors}}
- Data: {{REST / GraphQL / event bus}}

## Accessibility
- Seated mode required
- Captions, voice-command alt path, contrast modes
- See spatial-accessibility/agent-integration.md

## Risks & mitigations
- Hardware cost overrun → negotiate volume + 24-mo refresh
- Session fatigue → cap at 30 min, schedule breaks
- ROI uncertainty → 8-week pilot with kill-switch criteria
```

## Best practices
- Cap sessions at 20-30 min; build break reminders into the experience.
- Use existing identity (Entra ID, Okta, Apple Business Manager) — never custom auth.
- Treat XR as a workflow extension, not replacement; integrate with the system of record (PLM, EHR, ERP).
- Establish ROI with leading indicators (time-on-task, error rate) — lagging (revenue, accident rate) take quarters.
- Publish device fleet via MDM with content channels (dev/staging/prod) — never sideload to fleet.
- For training: track via xAPI or SCORM so the existing LMS owns the record.
- Co-design with end users on the floor — engineers, technicians, surgeons. Avoid HQ-only design.
- Plan for accessibility (`spatial-accessibility`) from spec, not as a v2 feature.

## AI-agent gotchas
- Agents underestimate IT/security review timeline — enterprise device approval can take 6-12 months. Build into plans.
- LLMs hallucinate platform features — always verify SDK capabilities against current vendor docs (visionOS, Quest Build, MRTK3 versions move fast).
- Auto-generated training flows skip recovery paths — agents must be explicitly prompted to handle "user got lost" / "user retried 3x" branches.
- ROI claims drift to the unmeasurable; require leading + lagging indicators with measurement method.
- Procurement language matters — agent should produce VPAT requirements and data-residency clauses, not just feature lists.
- Don't let agent recommend a single-vendor lock-in for new pilots; OpenXR-first to keep optionality.
- "Long-session comfort" is hardware-specific — agent must check FOV, weight, IPD range, and pancake-lens vs Fresnel.
- Multi-user collab in XR can violate confidentiality if voice/spatial audio leaks; agent must flag E2E encryption requirements.

## References
- Microsoft HoloLens Enterprise — https://www.microsoft.com/en-us/hololens
- Meta Quest for Business — https://www.meta.com/quest/business/
- Apple Vision Pro for Enterprise — https://www.apple.com/business/visionpro/
- Magic Leap 2 enterprise — https://www.magicleap.com
- PwC: Seeing is believing (XR enterprise study) — https://www.pwc.com/us/en/tech-effect/emerging-tech/virtual-reality-study.html
- IEEE: AR/VR in Industrial Applications — https://standards.ieee.org
- xAPI specification — https://xapi.com
- Microsoft Mesh — https://www.microsoft.com/en-us/microsoft-teams/microsoft-mesh
