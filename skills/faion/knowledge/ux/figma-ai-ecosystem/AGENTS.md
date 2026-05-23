# Figma AI Ecosystem Map

## Summary

**One-sentence:** Report mapping Figma's first-party AI surfaces (Make, AI tools, code-connect, dev mode) plus the third-party plugin layer, with capability + risk per surface.

**One-paragraph:** Report mapping Figma's first-party AI surfaces (Make, AI tools, code-connect, dev mode) plus the third-party plugin layer, with capability + risk per surface. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a report produced by an agent applying figma ai ecosystem map. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible report for figma ai ecosystem map across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- team is making an adoption or governance decision across multiple Figma AI surfaces
- report needs to cover first-party + plugin layer with current capability + risk
- decision will be reviewed by design leadership and recorded as a one-page report

## Skip If (ANY kills it)

- single-surface decision (only Figma Make, only one plugin) — use the surface-specific methodology
- team has no Figma seat — methodology depends on Figma being the design tool
- report cadence is more than monthly — current state changes too fast for stale reports

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current Figma plan/seats | billing console output | design ops |
| Recent Figma changelog (last 30 days) | Figma blog + release notes | designer |
| Internal AI policy | what data may leave the org | compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-plugin-ecosystem]] | Third-party plugin slice of the ecosystem |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `changelog_diff` | sonnet | Diff last 30 days of Figma releases vs. previous report. |
| `surface_capability_map` | sonnet | Per surface: feature, dependency, data-flow, current GA/beta state. |
| `risk_synthesis` | opus | Cross-surface risk view (data flow, vendor lock, regression). |

## Templates

| File | Purpose |
|------|---------|
| `templates/ecosystem-report.md` | Report skeleton with surface table + risk table + executive summary |
| `templates/surface-matrix.json` | Surface capability matrix skeleton |
| `templates/_smoke-test.md` | Minimum viable filled-in ecosystem report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-figma-ai-ecosystem.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[ai-plugin-ecosystem]]
- [[figma-vs-adobe-strategy-2026]]
- [[ai-generated-layout-review-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
