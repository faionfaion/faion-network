# Product Operations (PM-side)

## Summary

**One-sentence:** PM-side RACI contract with an existing Product Ops function: consumes canonical artefacts, hands off scaled-org ceremonies, never duplicates instrumentation Product Ops owns.

**One-paragraph:** Written RACI per artefact (tracking-plan, OKR cascade, voice-of-customer, launch readiness); PM consumes canonical stores rather than rebuilding them; scaled PM-invented ceremonies hand off to Product Ops; explicit escalation path for disputes. Output: pm-ops-contract markdown + RACI YAML.

**Ефективно для:**

- PM onboarding в org з existing Product Ops функцією.
- Кілька PM-ів просять inconsistent artefacts — route через Product Ops canonical store.
- Pre-board prep — consume Product Ops outputs замість re-derive.
- PM пропонує нову ceremony — hand off до Product Ops для scaling.

## Applies If (ALL must hold)

- PM onboarding into an org with an existing Product Ops function — needs explicit RACI.
- Multiple PMs requesting inconsistent artifacts — route through Product Ops canonical store.
- Preparing a board/exec/portfolio review — consume Product Ops outputs.
- PM proposes a new ceremony — hand off to Product Ops to ship org-wide.
- PM receives a Product Ops insight and needs to convert it into a discovery or kill decision.

## Skip If (ANY kills it)

- No Product Ops function exists — use solo product-operations methodology.
- <=2 PM team where overhead exceeds benefit.
- Consultancy / services with no recurring product surface.
- Existing RACI <=90 days old without org change.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product Ops charter | doc | Head of Product Ops |
| Artefact inventory | list of canonical artefacts | Product Ops |
| PM cohort | list of PMs | org chart |
| Escalation path baseline | doc | Head of Product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[stakeholder-management]] | Provides the stakeholder register that informs RACI roles. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: explicit RACI, canonical-store consumption, scaled-ceremony hand-off, no-duplicate instrumentation, named escalation | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for pm-ops-contract | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: parallel store, scaled PM-ceremony, ad-hoc instrumentation, escalation ambiguity | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: charter -> RACI -> canonical map -> ceremony handoff -> escalation | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on Product Ops presence + PM count | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `raci-author` | sonnet | Draft the RACI from PM + ProductOps charters. |
| `contract-audit` | haiku | Mechanical check of canonical-store consumption. |
| `escalation-memo` | sonnet | Write the escalation path with named owners. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pm-ops-contract.md.j2` | PM-ops contract skeleton with RACI + canonical map + escalation. |
| `templates/pm-ops-contract.md` | PM-ops contract skeleton with RACI + canonical map + escalation. Generated from `templates/pm-ops-contract.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pm-ops-contract-check.sh` | Check that PM artefacts use canonical-store outputs (no parallel). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-product-operations.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[stakeholder-management]]
- [[product-analytics]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pm-ops-contract-check.sh`

```bash
set -euo pipefail
#!/usr/bin/env bash
# pm-ops-contract-check.sh — refuse PM-side write attempts to system-of-record.
# Wrap PM agent invocations: if the planned action touches a write surface
# owned by Product Ops, exit non-zero and instruct the agent to use the
# hand-off queue instead.
# Usage: pm-ops-contract-check.sh <planned-action.json>
# planned-action.json format: {"calls": [{"op": "write", "target": "linear"}]}
set -euo pipefail
ACTION="${1:?usage: pm-ops-contract-check.sh <planned-action.json>}"
# Systems where Product Ops owns write access
WRITE_OWNED_BY_OPS='linear|jira|productboard|aha|notion-canonical|dbt-models|kpi-dictionary'

if jq -e --arg p "$WRITE_OWNED_BY_OPS" '
  .calls[] | select(.op == "write") | .target | test($p)
' "$ACTION" >/dev/null 2>&1; then
  echo "BLOCKED: PM agent attempted Product-Ops-owned write."
  echo "Hand-off path: post to #product-ops-intake or open PR in ops/templates."
  echo "Systems owned by Product Ops: linear, jira, productboard, aha, notion-canonical, dbt-models, kpi-dictionary"
  exit 2
fi
echo "OK: PM agent stays within read + narrative scope."
```
