# Spatial Computing Overview: Platform Landscape and Selection Workflow (2026)

## Summary

**One-sentence:** Produces a defensible platform-selection decision record for a spatial product, comparing visionOS / Quest / PSVR2 / HoloLens / Android XR / WebXR on install base, SDK constraints, content type fit, and 2026 platform deltas.

**One-paragraph:** Spatial computing blends digital content with physical space through AR, VR, and MR. Choosing the wrong platform early forces an expensive port or a stalled launch. This methodology drives an agent through a paste-ready decision workflow: classify the use case (productivity / entertainment / training / industrial), score each candidate platform on install base + SDK maturity + audience fit + content-type fit, and emit a versioned `decision-record` JSON listing primary + fallback platforms with cited evidence. 2026 deltas (Vision Pro v2 mass shift, Android XR debut, Quest 3S install-base growth, Pico exits) drive selection.

**Ефективно для:**

- Pre-funding decisions on XR product: which platform first, which second.
- Translating a 2D mobile / web product to a spatial modality where install-base + ecosystem must justify ROI.
- Multi-platform XR strategy with WebXR + native combinations.
- Producing a decision record auditable by an investor or steering committee.

## Applies If (ALL must hold)

- Target use case involves head-mounted displays (HMDs) in 2025/2026.
- No SDK has been committed yet; the decision is still open.
- A stakeholder will read and sign the decision-record artefact.

## Skip If (ANY kills it)

- Existing platform commit already made — use platform-specific patterns instead.
- Internal hack-week prototype with no commercial intent — overhead exceeds value.
- Pre-2024 VR knowledge tasks — platform landscape has changed; consult vendor docs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use-case description | Markdown brief | PM / founder |
| Target audience profile | persona doc | research |
| Content type list | list (3D models / video / dialogue / interactive scene) | design |
| Budget + team skills | spreadsheet | engineering manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[spatial-ux-fundamentals]] | Provides the field-zone vocabulary referenced by content-type fit |
| [[spatial-design-tools]] | Tool-chain implications of the platform choice |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: cite-2026-data, score-on-evidence, primary-plus-fallback, content-type-fit, audience-fit | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision-record + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: stale-data, founder-fanboy, single-platform-lock, ignoring-content-fit | 700 |
| `content/04-procedure.xml` | essential | 5-step decision procedure | 900 |
| `content/05-examples.xml` | essential | Worked example: productivity tool selecting visionOS primary + WebXR fallback | 600 |
| `content/06-decision-tree.xml` | essential | Tree: use-case → audience → content-type → platform shortlist | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-use-case` | haiku | Bucket from a small enum. |
| `score-platforms` | sonnet | Multi-criteria reasoning with cited evidence. |
| `draft-decision-record` | sonnet | Structured output with justification. |
| `red-team-decision` | opus | Adversarial review by a second agent. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Decision-record skeleton with platform-scoring table + rationale + risks |
| `templates/platform-comparison-matrix.csv` | 2026 platform snapshot CSV for scoring |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-spatial-computing-overview.py` | Validate decision-record JSON against the schema | Before committing the decision record |

## Related

- [[spatial-design-tools]]
- [[spatial-ux-fundamentals]]
- [[enterprise-xr-applications]]
- [[immersive-design-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on use-case category (productivity / entertainment / training / industrial) → audience scale (consumer / prosumer / enterprise) → content type (3D models / cinematic / dialogue / interactive) and emits a primary + fallback platform pair with required SDK and tooling. Each leaf references a rule from `01-core-rules.xml` so the decision-record carries cited justifications.
