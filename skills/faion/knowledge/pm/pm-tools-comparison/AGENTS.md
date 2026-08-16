# PM Tools Comparison

## Summary

**One-sentence:** Comparison report scoring 2-5 PM tools on a weighted matrix (Core Features 30%, Usability 25%, Integrations 20%, Enterprise 15%, Cost 10%) plus 2-week PoC + TCO + ADR.

**One-paragraph:** PM Tools Comparison defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Teams replacing a PM tool (migration off Jira / Asana / Trello).
- New programs choosing their first PM tool with multi-stakeholder buy-in.
- PMOs needing a defensible record of why tool X was chosen over Y.
- Budget owners requiring TCO over 3 years before approving a tool purchase.

## Applies If (ALL must hold)

- >=2 candidate tools that can be trialled in a 2-week PoC.
- Budget exists for a paid tier of each candidate during PoC.
- Team can dedicate 5-10h/person across 2 weeks for the PoC.
- Named decision owner has authority to ratify the ADR.

## Skip If (ANY kills it)

- Only one tool is feasible (compliance / vendor lock-in) — write a single-choice ADR, skip comparison.
- Team size <5 — overhead exceeds value, pick the cheapest viable.
- PoC budget cannot be secured — comparison without PoC is theoretical and untrustworthy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pm-tools-comparison_template_fill` | haiku | Bounded template fill, no judgement. |
| `pm-tools-comparison_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `pm-tools-comparison_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the PM tools comparison report artefact. |
| `templates/evaluation-scorecard.md.j2` | Markdown skeleton for the per-tool scorecard with criteria + evidence. |
| `templates/evaluation-scorecard.md` | Markdown skeleton for the per-tool scorecard with criteria + evidence. Generated from `templates/evaluation-scorecard.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/tco.yaml` | YAML template for 3-year TCO per tool. |
| `templates/weighted_score.py` | Reference script computing weighted totals from the scorecard. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-tools-comparison.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/pm-tools-comparison.json",
  "type": "object",
  "required": [
    "report_id",
    "tools",
    "criteria_weights",
    "scores",
    "tco",
    "recommendation",
    "decision_owner"
  ],
  "properties": {
    "report_id": {
      "type": "string"
    },
    "tools": {
      "type": "array",
      "minItems": 2,
      "maxItems": 5
    },
    "criteria_weights": {
      "type": "object",
      "required": [
        "core_features",
        "usability",
        "integrations",
        "enterprise",
        "cost"
      ]
    },
    "scores": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": [
          "core_features",
          "usability",
          "integrations",
          "enterprise",
          "cost",
          "evidence"
        ]
      }
    },
    "tco": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": [
          "year_1",
          "year_2",
          "year_3",
          "total"
        ]
      }
    },
    "recommendation": {
      "type": "object",
      "required": [
        "tool",
        "rationale"
      ]
    },
    "decision_owner": {
      "type": "string"
    },
    "dissents": {
      "type": "array"
    }
  }
}
```

### `templates/tco.yaml`

```yaml
# TCO calculation template.
# Replace placeholder values with actuals before presenting to stakeholders.
# All monetary values in USD.

tool: "[Tool Name]"
users: 50
currency: USD

direct_costs:
  license_per_user_per_month: 10
  annual_license: 6000          # license_per_user * users * 12
  add_ons:
    premium_support: 1000
    additional_storage: 500
    sso_integration: 0          # included in license tier
  total_direct_year1: 7500

indirect_costs:
  implementation:
    setup_hours: 40
    hourly_rate: 100
    total: 4000
  migration:
    consultant_days: 5
    daily_rate: 1500
    total: 7500
  training:
    sessions: 4
    cost_per_session: 500
    total: 2000
  ongoing_admin:
    hours_per_month: 10
    hourly_rate: 75
    annual: 9000
  total_indirect: 22500

hidden_costs:
  productivity_loss_during_transition: 5000
  integration_development: 3000
  custom_reporting: 2000
  total_hidden: 10000

summary:
  year_1_tco: 40000   # direct + indirect + hidden
  year_2_tco: 16500   # direct + ongoing_admin only
  year_3_tco: 16500
  three_year_tco: 73000

notes:
  - "Migration cost captured at item level: [N] issues, [N] automations, [N] integrations"
  - Productivity loss estimate based on [N]-week transition at [N]% reduced throughput
  - Mark any estimate older than 12 months as STALE before presenting
```

### `templates/weighted_score.py`

```python
"""


"""Compute weighted scores for PM tool comparison from a YAML scorecard.

Usage:
    python weighted_score.py scorecard.yaml

scorecard.yaml format:
    weights:
      core_features: 30
      usability: 25
      integrations: 20
      enterprise: 15
      cost: 10
    tools:
      Linear:
        core_features: {score: 9.0}
        usability: {score: 9.0}
        integrations: {score: 9.0}
        enterprise: {score: 8.3}
        cost: {score: 7.0}
      Jira:
        core_features: {score: 9.7}
        usability: {score: 6.0}
        integrations: {score: 8.7}
        enterprise: {score: 10.0}
        cost: {score: 6.5}

Output: sorted ranking with weighted totals.
"""
import sys

import yaml

data = yaml.safe_load(open(sys.argv[1]))
weights = data["weights"]
results = []

for tool, cats in data["tools"].items():
    total = sum(cats[c]["score"] * weights[c] / 100 for c in cats if c in weights)
    results.append((total, tool))

results.sort(reverse=True)
print("Ranked results:")
for score, tool in results:
    print(f"  {tool}: {score:.2f}")
```
