# Success Metrics Definition

## Summary

**One-sentence:** Produces a success-metrics spec (1 north-star + ≤5 AARRR KPIs + targets + baselines + vanity-flagged exclusions) so the team measures what drives business outcomes, not what's easy to count.

**Ефективно для:** Solo PMs whose dashboard fills with vanity metrics (pageviews, signups) that don't move the revenue needle.

**One-paragraph:** Teams measure the wrong things or too many things. This methodology pins one north-star metric to a business goal, partitions ≤5 supporting KPIs across the AARRR funnel (acquisition / activation / retention / referral / revenue), sets actionable targets with baselines, and explicitly flags vanity metrics for exclusion. Output is consumed by mvp-instrumentation-checklist and outcome-based-roadmaps.

## Applies If (ALL must hold)

- New product or feature launch needs measurement baseline.
- Existing dashboards are crowded with metrics nobody acts on.
- Team disagrees on which metric should drive prioritisation.
- Quarterly OKR cycle needs measurable key results.

## Skip If (ANY kills it)

- Pre-product: no traffic to measure.
- Compliance-only metrics (uptime SLA, regulatory) — outside AARRR scope.
- Team smaller than one — no need for shared dashboards.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| business goal statement | string | founder |
| current funnel data | csv/dashboard export | analytics |
| instrumentation status | checklist | engineer |
| prior quarter targets | spec | previous run |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/mvp-instrumentation-checklist` | Downstream — consumes metric definitions to instrument. |
| `solo/product/product-manager/okr-setting` | Downstream — KPIs feed into OKR key results. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/success-metrics-definition.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/success-metrics-definition.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-success-metrics-definition.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[mvp-instrumentation-checklist]] — related methodology.
- [[okr-setting]] — related methodology.
- [[outcome-based-roadmaps]] — related methodology.
- [[use-case-mapping]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/success-metrics-definition.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/success-metrics-definition.json",
  "title": "Success Metrics Definition Output Contract",
  "type": "object",
  "required": [
    "north_star",
    "aarrr_kpis",
    "baselines",
    "targets",
    "vanity_excluded",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "north_star": {
      "type": "object",
      "description": "metric + business outcome link + owner"
    },
    "aarrr_kpis": {
      "type": "array",
      "description": "\u22645 KPIs partitioned across acquisition/activation/retention/referral/revenue",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "baselines": {
      "type": "object",
      "description": "current value per KPI"
    },
    "targets": {
      "type": "object",
      "description": "target value + window per KPI"
    },
    "vanity_excluded": {
      "type": "array",
      "description": "vanity metrics explicitly excluded",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "owner": {
      "type": "string",
      "description": "named owner"
    },
    "version": {
      "type": "string",
      "description": "semver"
    },
    "last_reviewed": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    }
  },
  "additionalProperties": true
}
```

### `templates/_smoke-test.json`

```json
{
  "north_star": {
    "k": "v"
  },
  "aarrr_kpis": [
    {
      "k": "v"
    }
  ],
  "baselines": {
    "k": "v"
  },
  "targets": {
    "k": "v"
  },
  "vanity_excluded": [
    {
      "k": "v"
    }
  ],
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "__sample__": true
}
```
