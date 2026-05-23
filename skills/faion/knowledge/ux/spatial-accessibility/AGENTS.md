# Spatial Accessibility

## Summary

**One-sentence:** Produces a spatial-accessibility audit report ensuring every AR/VR/MR interaction has ≥2 independent input modalities, seated-mode parity, configurable comfort options, and a non-spatial fallback.

**One-paragraph:** Spatial UI introduces accessibility barriers WCAG 2.2 does not address: 6-DoF movement, implicit hand-tracking assumptions, FoV constraints, motion sickness. This methodology enforces two-modality coverage per interaction (gaze+pinch, voice, controller, switch), seated-mode parity for every standing-mode interaction, both vignette + teleport locomotion options, head-locked subtitle defaults, and hardware testing with at least one low-vision + one motor-impaired + one motion-sensitive user before declaring compliance. Output is a JSON report consumed by platform-review submission.

**Ефективно для:**

- Designing AR/VR/MR experiences на Vision Pro, Quest, PS VR2, HoloLens, або WebXR.
- Adapting flat UI to spatial platform — seated mode, gaze fallback, motion-comfort settings.
- App Store / Meta Horizon Store submission — accessibility checks blocking approval.
- Enterprise XR (industrial training, medical) — injury risk requires accommodation parity.

## Applies If (ALL must hold)

- Product surface is AR / VR / MR on supported HMD or WebXR.
- Interaction model uses at least one spatial input (hand tracking, controllers, gaze).
- Hardware testing with at least 3 assistive users is feasible before launch.

## Skip If (ANY kills it)

- 2D mobile / desktop app — use WCAG 2.2 + mobile a11y instead.
- Passthrough video with no UI overlay — reduces to video a11y (captions, contrast).
- Internal one-off demo for a single user — full a11y program premature.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interaction inventory | JSON / Markdown | spatial-design team |
| Platform target | enum: visionos / quest / psvr2 / hololens / webxr | PM |
| Comfort options enumerated | list | XR engineering |
| Assistive tester roster | list of users + assistive tech | a11y research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spatial-interaction-patterns]] | Defines the interaction-state-machine vocabulary the report references |
| [[testing-with-assistive-technology]] | Defines AT-user session requirements |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: two-modalities-required, non-spatial-fallback, seated-mode-parity, comfort-options-both, captions-policy, hardware-tester-mix | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for interaction audit + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: controller-only, head-locked-HUD, synthetic-only-testing, head-locked-captions-default-off | 700 |
| `content/04-procedure.xml` | essential | 5-step audit procedure | 900 |
| `content/05-examples.xml` | essential | Worked example: Vision Pro productivity app interaction audit | 600 |
| `content/06-decision-tree.xml` | essential | Tree: platform → input-model → comfort-policy → caption-policy | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `enumerate-interactions` | haiku | Mechanical listing from XR design doc. |
| `map-modalities` | sonnet | Judgment on independent-modality definition. |
| `comfort-audit` | sonnet | Reasoning over user-sensitivity profiles. |
| `assistive-user-session` | opus | Human-led; agent assists with transcript synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/alt-input-matrix.ts` | TypeScript auditor: each interaction must have ≥2 modalities and seated-mode flag |
| `templates/spatial-a11y-report.md` | Markdown report skeleton with interaction matrix + comfort options + tester log |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-accessibility.py` | Validate the audit JSON against the schema | Pre-release gate; pre-submission to App Store / Horizon |

## Related

- [[spatial-interaction-patterns]]
- [[vr-design-patterns]]
- [[immersive-design-principles]]
- [[testing-with-assistive-technology]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on platform (visionOS / Quest / WebXR), input model (hand-track-primary / controller-primary), and required comfort policy. Each leaf references a rule in `01-core-rules.xml` and dictates whether seated-mode toggling, captioning defaults, or assistive-tester recruitment must escalate.
