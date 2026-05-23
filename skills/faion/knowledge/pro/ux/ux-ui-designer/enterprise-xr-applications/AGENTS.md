---
slug: enterprise-xr-applications
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an enterprise-XR application spec covering training simulations, remote assistance, digital twins, 3D analytics, distributed collaboration — with comfort, IT integration, security, and ROI gates.
content_id: "82059c06750fca51"
complexity: deep
produces: spec
est_tokens: 4500
tags: [xr, enterprise, immersive-design, training, remote-assistance]
---
# Enterprise XR Applications

## Summary

**One-sentence:** Produces an enterprise-XR application spec covering training simulations, remote assistance, digital twins, 3D analytics, distributed collaboration — with comfort, IT integration, security, and ROI gates.

**One-paragraph:** Enterprise XR differs from consumer: long sessions (30-120 min), IT-managed deployment, security/compliance scrutiny, and ROI accountability. Five primary use cases — training simulations (high-risk procedures), remote-assistance overlays (expert + field tech), digital twins (plants/facilities), 3D analytics (portfolios exceeding 2D), distributed design-review. Each carries headset coverage, comfort budget, IT integration, security review, and measurable ROI gates.

**Ефективно для:**

- Training simulations: high-risk procedures (manufacturing/healthcare/energy).
- Remote-assistance: expert провідник для field technician у real time.
- Digital twins: large facility/equipment fleet — reduce downtime через 3D visual.
- Distributed design review / virtual walkthrough — distributed teams.

## Applies If (ALL must hold)

- Enterprise workflow with >=50% headset coverage in the target population.
- Use case fits one of: training, remote-assistance, digital twin, 3D analytics, distributed collab.
- Security + IT integration review is feasible.

## Skip If (ANY kills it)

- Consumer-facing one-off experience — different constraints + ROI case.
- 2D dashboard already solves it well — XR adds friction without payoff.
- Audience with mixed a11y needs underserved by current XR (vestibular, low vision).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Headset coverage data | % of population | IT inventory |
| Use case selection | 1 of 5 | product brief |
| Security review template | checklist | this methodology |
| ROI baseline | current cost + target reduction | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[immersive-design-principles]] | Comfort + presence baseline |
| [[spatial-accessibility]] | A11y in spatial computing |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 6-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/enterprise-xr-spec.md` | Enterprise XR application spec covering all 6 gates |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-enterprise-xr-applications.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[immersive-design-principles]]
- [[ar-design-patterns]]
- [[vr-design-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
