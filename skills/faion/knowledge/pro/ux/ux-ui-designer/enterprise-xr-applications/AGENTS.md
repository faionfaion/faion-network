---
slug: enterprise-xr-applications
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Enterprise needs differ from consumer XR experiences.
content_id: "e6085381b21f5667"
tags: [xr, enterprise, immersive-design, training, remote-assistance]
---
# Enterprise XR Applications

## Summary

**One-sentence:** Enterprise needs differ from consumer XR experiences.

**One-paragraph:** Enterprise needs differ from consumer XR experiences. Design XR for training simulations, remote-assistance overlays, digital twins, 3D analytics, and distributed collaboration—balancing long-session comfort, IT integration, security, deployment management, accessibility compliance, and measurable ROI.

## Applies If (ALL must hold)

- Designing training simulations for high-risk procedures in manufacturing, healthcare, or energy.
- Building remote-assistance overlays where an expert guides a field technician in real time.
- Visualizing digital twins for plants, facilities, or large equipment fleets to reduce downtime.
- Adding 3D analytics dashboards for portfolios exceeding 2D screen real estate.
- Running design-review or virtual-walkthrough sessions for distributed teams.

## Skip If (ANY kills it)

- Consumer-facing one-off experiences—different design constraints, weaker ROI case.
- Tasks that 2D dashboards already solve well; XR adds friction without payoff.
- Audiences with mixed accessibility needs that XR currently underserves (vestibular issues, low vision).
- Pre-validation of headset penetration in the target audience—don't ship XR-only flows to a workforce with <50% headset coverage.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ux/ux-ui-designer/`
