---
slug: run-a-quarterly-journey-bottleneck-attack
tier: pro
group: role-product-manager
persona: role-product-manager
goal: optimize-tune
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Instead of a roadmap drift through 'features stakeholders shouted loudest about', PM picks one customer journey, finds the worst bottleneck via funnel plus qualitative data, and runs a one-quarter..."
content_id: 9ae00fdf080c0e85
methodology_refs:
  - continuous-discovery-habits
  - experimentation-at-scale
  - product-analytics
  - feature-prioritization-rice
---

# Run a quarterly journey-bottleneck attack

## Context

Instead of a roadmap drift through 'features stakeholders shouted loudest about', PM picks one customer journey, finds the worst bottleneck via funnel plus qualitative data, and runs a one-quarter focused attack. Faion has no journey-mapping or bottleneck-prioritization methodology — this is a major team-PM gap.

Tier: **pro**. Complexity: **medium**. Group: **role-product-manager**. Persona: **role-product-manager**.

## Outcome

This playbook is done when:

- One journey explicitly chosen; rest deprioritised.
- Quant bottleneck named with rate + absolute loss.
- Qual report converging on the cause.
- Quarter-end verdict on bottleneck conversion change.

## Steps

### 1. Pick the journey

Choose the single journey the quarter will attack.

Tasks:
- List 3-5 candidate journeys (activation, retention, expansion, etc.).
- Pick the one tied to the active OKR.
- Lock the choice for the quarter.

Outputs:
- Chosen journey statement.

Decision gate: Advance when one journey is picked and the rest are explicitly deprioritised.

### 2. Funnel scan

Find the quantitative bottleneck.

Tasks:
- Build the journey funnel with stage-by-stage conversion.
- Identify the lowest-converting stage.
- Confirm the stage matters (size × drop).

Outputs:
- Funnel diagnostic.

Decision gate: Advance when the worst stage is named with both rate + absolute loss.

### 3. Qual layer

Find the qualitative why behind the drop.

Tasks:
- Interview 5+ users who dropped at the bottleneck stage.
- Tag drop-off causes.
- Compare quant drop to qual causes for consistency.

Outputs:
- Qual report at the bottleneck stage.

Decision gate: Advance when 3+ users converge on the same cause.

### 4. Attack design

Design the quarter's experiments.

Tasks:
- List 3-5 candidate interventions for the bottleneck.
- Rank by RICE.
- Schedule them as sequenced experiments across the quarter.

Outputs:
- Attack plan with sequenced experiments.

Decision gate: Advance when the attack plan has 3-5 ranked experiments with start dates.

### 5. Read + decide

End the quarter with a verdict.

Tasks:
- Compare bottleneck conversion before vs after.
- Tag interventions as win / no-op / negative.
- Decide whether the journey gets a second quarter or releases attention.

Outputs:
- Bottleneck attack verdict.

Decision gate: Required: a written verdict at quarter end.

## Decision points

- Activation vs retention bottleneck — pick the one whose absolute loss is larger when both are bad.
- Second quarter vs release attention — release when the bottleneck improved past the diminishing-returns line.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/product/product-manager/continuous-discovery-habits`
- `pro/product/product-manager/experimentation-at-scale`
- `pro/product/product-manager/product-analytics`
- `solo/product/product-manager/feature-prioritization-rice`
