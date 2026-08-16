# Figma vs Adobe Strategy 2026

## Summary

**One-sentence:** Decision record comparing Figma vs Adobe (XD/Firefly/Creative Cloud) for a design org in 2026 — feature parity, AI integration, total cost, lock-in risk.

**One-paragraph:** Decision record comparing Figma vs Adobe (XD/Firefly/Creative Cloud) for a design org in 2026 — feature parity, AI integration, total cost, lock-in risk. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a decision-record produced by an agent applying figma vs adobe strategy 2026. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible decision-record for figma vs adobe strategy 2026 across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- design org is at a renewal / consolidation decision point (Figma seat block expanding or Adobe ELA renewing)
- decision must account for 2026 AI feature parity (Firefly vs Figma Make, AI tools, code-connect equivalent)
- stakeholders include design leadership + finance + engineering hand-off

## Skip If (ANY kills it)

- team is single-tool already with no friction — wait for the natural renewal trigger
- team uses a third tool exclusively (Sketch, Penpot) — write a separate three-way comparison
- decision is purely cost (no AI / feature considerations) — use procurement worksheet, not this methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current contract terms (Figma + Adobe) | billing + procurement | finance |
| Headcount snapshot (designers, devs consuming hand-off) | HR system | design ops |
| AI policy on data flow per vendor | compliance doc | compliance |
| Last 90 days of design throughput metrics | Figma activity logs or equivalent | design ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[figma-ai-ecosystem]] | Figma side of the comparison |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feature_parity_matrix` | sonnet | Side-by-side feature mapping. |
| `cost_modeling` | sonnet | TCO calc with renewal scenarios. |
| `lock_in_risk_assessment` | opus | Strategic risk of migration / consolidation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md.j2` | ADR-style decision record skeleton |
| `templates/decision-record.md` | ADR-style decision record skeleton Generated from `templates/decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/feature-parity-matrix.json` | Feature parity matrix skeleton |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in tool-strategy ADR |
| `templates/_smoke-test.md` | Minimum viable filled-in tool-strategy ADR Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.
| `templates/decision-matrix.md.j2` | Pre-existing template carried into the figma-vs-adobe-strategy-2026 methodology |
| `templates/decision-matrix.md` | Pre-existing template carried into the figma-vs-adobe-strategy-2026 methodology Generated from `templates/decision-matrix.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-figma-vs-adobe-strategy-2026.py` | Validate the decision-record artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[figma-ai-ecosystem]]
- [[ai-plugin-ecosystem]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature-parity-matrix.json`

```json
{
  "artefact_id": "figma-vs-adobe-strategy-2026-template-001",
  "produced_at": "2026-05-23T10:00:00Z",
  "validator_passed": false,
  "fields": "fill per content/02-output-contract.xml schema"
}
```
