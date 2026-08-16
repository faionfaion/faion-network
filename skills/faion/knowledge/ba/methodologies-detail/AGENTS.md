# BA Methodologies Detail

## Summary

**One-sentence:** Catalog of 12 enterprise BA frameworks across KA-1..KA-6 with per-framework usage notes, deliverable templates, and trigger conditions for choosing each over its peers.

**One-paragraph:** Per-KA catalog of enterprise BA frameworks: governance, communication planning, elicitation preparation, requirements maintenance, change impact analysis, current state analysis, future state definition, risk analysis, change strategy planning, requirements architecture, solution options analysis, solution limitation assessment. Each entry has a usage note, expected deliverable, and a trigger condition mapping the ask to the framework.

**Ефективно для:**

- Enterprise programmes з governance + comms + risk + change strategy.
- Procurement: solution-options analysis перед вибором постачальника.
- Compliance: requirements-architecture як evidence.
- Steerco prep для KA-4 (current / future / change strategy).

## Applies If (ALL must hold)

- Enterprise programme requiring governance + communication plan + risk + change strategy artifacts.
- Procurement / vendor selection requiring solution-options analysis.
- Compliance work requiring requirements-architecture documentation.
- Steerco preparing for KA-4 strategy analysis (current/future/change strategy).
- Audit prep requiring per-framework deliverable mapping.

## Skip If (ANY kills it)

- Small / agile team with no governance layer.
- Single fix / hot patch.
- When elicitation-techniques / requirements-documentation already covers the ask.
- Greenfield startup where frameworks are overhead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Engagement context | Markdown | BA |
| KA routing record | JSON | knowledge-areas-detail |
| Methodology registry | JSON | this skill |
| Deliverable templates | templates/ | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `pro/ba/business-analyst/knowledge-areas-detail` | Provides KA routing to pick frameworks. |
| `pro/ba/business-analyst/modern-ba-framework` | Perspective routing wrapper. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with rationale + source citations | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `framework-trigger-check` | sonnet | Map ask + KA to the right framework. |
| `deliverable-templating` | haiku | Emit the matching template skeleton. |
| `per-framework-usage-guidance` | sonnet | Compose usage notes for the deliverable. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-route.sh` | Shell helper to print framework list for KA + context. |
| `templates/change-impact.md.j2` | Change impact analysis template. |
| `templates/change-impact.md` | Change impact analysis template. Generated from `templates/change-impact.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/change-strategy.md.j2` | Change strategy planning template. |
| `templates/change-strategy.md` | Change strategy planning template. Generated from `templates/change-strategy.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/communication-plan.md.j2` | Communication plan template. |
| `templates/communication-plan.md` | Communication plan template. Generated from `templates/communication-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/current-state.md.j2` | Current state analysis template. |
| `templates/current-state.md` | Current state analysis template. Generated from `templates/current-state.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/future-state.md.j2` | Future state definition template. |
| `templates/future-state.md` | Future state definition template. Generated from `templates/future-state.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/governance-framework.md.j2` | Governance framework template. |
| `templates/governance-framework.md` | Governance framework template. Generated from `templates/governance-framework.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/requirements-architecture.md.j2` | Requirements architecture template. |
| `templates/requirements-architecture.md` | Requirements architecture template. Generated from `templates/requirements-architecture.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/risk-register.md.j2` | Risk register template. |
| `templates/risk-register.md` | Risk register template. Generated from `templates/risk-register.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/solution-limitations.md.j2` | Solution limitation assessment template. |
| `templates/solution-limitations.md` | Solution limitation assessment template. Generated from `templates/solution-limitations.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/solution-options.md.j2` | Solution options analysis template. |
| `templates/solution-options.md` | Solution options analysis template. Generated from `templates/solution-options.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum filled-in decision record + one deliverable. |
| `templates/_smoke-test.md` | Minimum filled-in decision record + one deliverable. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodologies-detail.py` | Validate the produced artefact against the output-contract schema. | Pre-commit; CI on each artefact change. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[knowledge-areas-detail]]
- [[knowledge-areas-overview]]
- [[modern-ba-framework]]
- [[decision-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The mandatory tree maps observable signals (engagement type, perspective set, scope, audit needs, baseline presence) to a single rule from `01-core-rules.xml`; every leaf references either a numbered core rule or the `skip-this-methodology` conclusion that routes the agent to a different methodology when this one does not apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ba-route.sh`

```bash
set -euo pipefail

echo "[methodologies-detail] skeleton helper — replace with real logic."

# Example: list candidate frameworks for the current KA.
KA="${1:-KA-1}"
echo "KA: $KA"
```
